"""Single-allocation supervisor for an immutable external-only request matrix."""

import argparse
import concurrent.futures
import json
import os
import queue
import shutil
import socket
import subprocess
import tarfile
import time
from collections import Counter
from pathlib import Path

from .external_prepare import canonical, identity
from .external_worker import dump
from .sources import digest


def environment(config, model, work):
    runtime = config["runtime"]
    env = os.environ.copy()
    for name in (
        "PYTHONPATH",
        "JULIA_PROJECT",
        "JULIA_LOAD_PATH",
        "JULIA_DEPOT_PATH",
        "PYTHON_JULIACALL_PROJECT",
        "PYTHON_JULIAPKG_PROJECT",
        "PYTHON_JULIACALL_EXE",
        "PYTHON_JULIAPKG_EXE",
    ):
        env.pop(name, None)
    stage_sites = runtime.get("stage_sites", {})
    extra_sites = stage_sites.get("aifeynman" if model == "AI_Feynman" else "main", [])
    env.update(
        PYTHONPATH=os.pathsep.join([config["source_root"], *extra_sites]),
        PYTHONNOUSERSITE="1",
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONUNBUFFERED="1",
        OPENBLAS_NUM_THREADS="1",
        OMP_NUM_THREADS="1",
        OMP_THREAD_LIMIT="1",
        MKL_NUM_THREADS="1",
        NUMEXPR_NUM_THREADS="1",
        NUMEXPR_MAX_THREADS="1",
        VECLIB_MAXIMUM_THREADS="1",
        RAYON_NUM_THREADS="1",
        CUDA_VISIBLE_DEVICES="",
        JULIA_NUM_THREADS="1",
        JULIA_NUM_GC_THREADS="1",
        PYTHON_JULIACALL_THREADS="1",
        PYTHON_JULIACALL_HANDLE_SIGNALS="yes",
        JULIA_PKG_OFFLINE="true",
        JULIA_PKG_PRECOMPILE_AUTO="0",
        PYTHON_JULIACALL_AUTOLOAD_IPYTHON_EXTENSION="no",
        MPLBACKEND="Agg",
        MPLCONFIGDIR=runtime["matplotlib_cache"],
        TMPDIR=str(work),
    )
    env.update(
        PYTHON_JULIACALL_PROJECT=runtime["julia_project"],
        PYTHON_JULIAPKG_PROJECT=runtime["julia_project"],
        JULIA_PROJECT=runtime["julia_project"],
        JULIA_DEPOT_PATH=runtime["julia_depot"],
        PYTHON_JULIACALL_EXE=runtime["julia_executable"],
        PYTHON_JULIAPKG_EXE=runtime["julia_executable"],
    )
    python = runtime["aifeynman_python"] if model == "AI_Feynman" else runtime["main_python"]
    bins = [str(Path(python).parent), runtime["aifeynman_bin"], "/usr/bin", "/bin"]
    env["PATH"] = os.pathsep.join(bins)
    return python, env


def timed(command, cwd, env, label):
    usage = cwd / (label + "-time.txt")
    with (
        (cwd / (label + ".stdout")).open("wb") as out,
        (cwd / (label + ".stderr")).open("wb") as err,
    ):
        result = subprocess.run(
            ["/usr/bin/time", "-o", str(usage), "-f", "%U %S %e %M %x", *command],
            cwd=cwd,
            env=env,
            stdout=out,
            stderr=err,
            check=False,
        )
    fields = usage.read_text().splitlines()[-1].split()
    return result.returncode, {
        "user_seconds": float(fields[0]),
        "system_seconds": float(fields[1]),
        "wall_seconds": float(fields[2]),
        "largest_process_peak_rss_kib": int(fields[3]),
        "exit_status": fields[4],
    }


def score_request(config, request, work):
    """Called only after immutable selected.json and predictions.csv exist."""
    from .scoring import recover, score

    selected = json.loads((work / "selected.json").read_text())
    result = score(
        Path(config["bank_root"]), request["task"], request["split"], work / "predictions.csv"
    )
    if request["category"] == "expression_recovery":
        recovery = recover(
            Path(config["bank_root"]), request["task"], request["split"], selected["expression"]
        )
        result.update(
            {
                k: recovery[k]
                for k in (
                    "symbolic_status",
                    "numeric_agreement",
                    "numeric_tolerance",
                    "witness_count",
                    "numeric_witness_status",
                    "expression_complexity",
                    "reference_complexity",
                )
            }
        )
        result["expression_metrics"] = {k: recovery[k] for k in ("rmse", "mae", "nrmse_train_std")}
    result.update(
        {k: request[k] for k in ("request_id", "model", "mode", "seed", "noise", "evidence_role")}
    )
    result["expression"] = selected["expression"]
    dump(work / "score.json", result)


def execute(config, request, cpu, scratch):
    os.sched_setaffinity(0, {cpu})  # Linux calling-thread affinity, inherited by its children.
    start, thread_start = time.monotonic(), time.thread_time()
    output = Path(config["output"])
    destination = output / "results" / request["request_id"]
    if destination.exists():
        result = json.loads((destination / "result.json").read_text())
        if (
            result["request_id"] != request["request_id"]
            or result["campaign_sha256"] != config["campaign_sha256"]
        ):
            raise ValueError("Existing result has a different frozen identity")
        return result
    work = scratch / request["request_id"]
    work.mkdir(exist_ok=False)
    dump(work / "request.json", request)
    python, env = environment(config, request["model"], work)
    record = {
        k: request[k]
        for k in (
            "request_id",
            "task",
            "split",
            "mode",
            "noise",
            "seed",
            "model",
            "panel",
            "evidence_role",
            "category",
            "bank_checksums_sha256",
        )
    }
    record.update(
        status="failed",
        campaign_sha256=config["campaign_sha256"],
        source_inventory_sha256=config["source_inventory_sha256"],
        cpu=cpu,
        host=socket.gethostname(),
        slurm_job_id=os.environ.get("SLURM_JOB_ID"),
        profile_sha256=identity(request["profile"]),
        payload_sha256=request["payload_sha256"],
    )
    fit_code, fit_time = timed(
        [python, "-m", "nuclearbench.external_worker", "--request", str(work / "request.json")],
        work,
        env,
        "fit",
    )
    record["fit_resources"] = fit_time
    if fit_code == 0:
        score_python, score_env = environment(config, "Ridge", work)
        score_code, score_time = timed(
            [
                score_python,
                "-m",
                "nuclearbench.external_campaign",
                "--score-config",
                config["config_path"],
                "--score-request",
                str(work / "request.json"),
                "--work",
                str(work),
            ],
            work,
            score_env,
            "score",
        )
        record["score_resources"] = score_time
        if score_code == 0:
            record.update(json.loads((work / "score.json").read_text()))
        else:
            record.update(error_type="ScoringError", error="See preserved score.stderr")
    elif (work / "worker-result.json").exists():
        failure = json.loads((work / "worker-result.json").read_text())
        record.update(error_type=failure.get("error_type"), error=failure.get("error"))
    else:
        record.update(error_type="NativeProcessExit", error=f"Worker exit {fit_code}")
    # Results are staged and atomically promoted once; incomplete directories
    # never masquerade as terminal scientific records.
    stage = output / "results" / (request["request_id"] + ".staging")
    stage.mkdir(exist_ok=False)
    primary = (
        "request.json",
        "predictions.csv",
        "selected.json",
        "candidate-history.json",
        "worker-result.json",
        "worker-resources.json",
        "transform.json",
        "warnings.json",
        "fit-time.txt",
        "score-time.txt",
        "fit.stdout",
        "fit.stderr",
        "score.stdout",
        "score.stderr",
        "score.json",
    )
    for name in primary:
        if (work / name).exists():
            shutil.copy2(work / name, stage / name)
    with tarfile.open(stage / "native-artifacts.tar.gz", "w:gz", compresslevel=1) as archive:
        for path in sorted(work.iterdir()):
            archive.add(path, arcname=path.name, recursive=True)
    record["supervision_thread_cpu_seconds"] = time.thread_time() - thread_start
    record["total_elapsed_seconds"] = time.monotonic() - start
    record["total_cpu_seconds"] = record["supervision_thread_cpu_seconds"] + sum(
        value["user_seconds"] + value["system_seconds"]
        for key, value in record.items()
        if key in {"fit_resources", "score_resources"}
    )
    record["artifacts"] = {p.name: digest(p) for p in stage.iterdir() if p.is_file()}
    dump(stage / "result.json", record)
    stage.rename(destination)
    shutil.rmtree(work)  # Only this completed run's exact owned node-local scratch.
    return record


def available_gib():
    info = dict(line.split(":", 1) for line in Path("/proc/meminfo").read_text().splitlines())
    return int(info["MemAvailable"].split()[0]) / 2**20


def verify_config(config):
    config = dict(config)
    declared = config.pop("campaign_sha256")
    if identity(config) != declared:
        raise ValueError("Campaign configuration changed after registration")
    config["campaign_sha256"] = declared
    if digest(Path(config["requests"])) != config["matrix_sha256"]:
        raise ValueError("Request matrix differs from frozen configuration")
    inventory = Path(config["source_inventory"])
    if digest(inventory) != config["source_inventory_sha256"]:
        raise ValueError("Source inventory identity mismatch")
    for path, expected in json.loads(inventory.read_text()).items():
        if digest(Path(path)) != expected:
            raise ValueError("Source/runtime bytes changed: " + path)
    return config


def supervise(config, require_slurm):
    import psutil

    verify_config(config)
    affinity = sorted(os.sched_getaffinity(0))
    if require_slurm:
        if not os.environ.get("SLURM_JOB_ID") or socket.gethostname().split(".")[0] != "node2":
            raise ValueError("This campaign requires its registered node2 Slurm allocation")
        if int(os.environ.get("SLURM_CPUS_PER_TASK", "0")) != 256 or len(affinity) != 256:
            raise ValueError(
                "Expected exactly 256 bound logical CPUs; refuse unverified allocation"
            )
    cpus = affinity[: config["workers"]]
    if len(cpus) != config["workers"]:
        raise ValueError("Insufficient effective CPU affinity")
    output = Path(config["output"])
    (output / "results").mkdir(exist_ok=True)
    lock = output / "supervisor.lock"
    with lock.open("x") as stream:
        json.dump(
            {
                "pid": os.getpid(),
                "host": socket.gethostname(),
                "job_id": os.environ.get("SLURM_JOB_ID"),
                "campaign_sha256": config["campaign_sha256"],
            },
            stream,
        )
    scratch = Path(os.environ.get("SLURM_TMPDIR", "/tmp")) / (
        "nusr-external-" + str(os.environ.get("SLURM_JOB_ID", os.getpid()))
    )
    scratch.mkdir(exist_ok=False)
    dump(
        output / "allocation.json",
        {
            "affinity": affinity,
            "workers": len(cpus),
            "hostname": socket.gethostname(),
            "memory_available_gib": available_gib(),
            "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
            "scratch": str(scratch),
            "cpu_topology": subprocess.check_output(["lscpu", "-p=CPU,CORE,SOCKET"], text=True),
            "cgroup": Path("/proc/self/cgroup").read_text(),
        },
    )
    items = [json.loads(line) for line in Path(config["requests"]).read_text().splitlines()]
    if any(r["model"] in {"NuSR", "MySR"} for r in items):
        raise ValueError("Product model in an external-only matrix")
    if len({r["request_id"] for r in items}) != len(items):
        raise ValueError("Duplicate request identities")
    free = queue.SimpleQueue()
    for cpu in cpus:
        free.put(cpu)
    counts, active, position, completed = Counter(), {}, 0, 0
    estimates = {
        "PySR": 2.5,
        "AI_Feynman": 1.0,
        "Operon": 0.5,
        "GPR": 1.0,
        "LightGBM": 0.5,
        "MLP_ensemble": 0.5,
        "Ridge": 0.25,
    }
    start, last_observation = time.monotonic(), 0.0
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(cpus)) as executor:
        while position < len(items) or active:
            committed = Counter()
            for process in psutil.Process().children(recursive=True):
                try:
                    binding = process.cpu_affinity()
                    if len(binding) == 1:
                        committed[binding[0]] += process.memory_info().rss / 2**30
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            while position < len(items) and not free.empty():
                item = items[position]
                reserved = sum(
                    max(0, estimates[i[1]["model"]] - committed[i[0]]) for i in active.values()
                )
                if available_gib() - reserved < 8.0 + estimates[item["model"]]:
                    break
                cpu = free.get()
                future = executor.submit(execute, config, item, cpu, scratch)
                active[future] = (cpu, item)
                position += 1
            if active:
                done, _ = concurrent.futures.wait(
                    active, timeout=10, return_when=concurrent.futures.FIRST_COMPLETED
                )
                for future in done:
                    cpu, item = active.pop(future)
                    result = future.result()
                    free.put(cpu)
                    counts[result["model"] + ":" + result["status"]] += 1
                    completed += 1
                    with (output / "events.jsonl").open("a") as stream:
                        stream.write(
                            canonical(
                                {
                                    "request_id": item["request_id"],
                                    "status": result["status"],
                                    "completed": completed,
                                    "elapsed": time.monotonic() - start,
                                }
                            )
                            + "\n"
                        )
            else:
                time.sleep(10)
            if time.monotonic() - last_observation >= 30:
                owned = psutil.Process().children(recursive=True)
                usage = []
                for process in owned:
                    try:
                        cpu_time, memory = process.cpu_times(), process.memory_info()
                        usage.append(
                            {
                                "pid": process.pid,
                                "cpu_user": cpu_time.user,
                                "cpu_system": cpu_time.system,
                                "rss_bytes": memory.rss,
                            }
                        )
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                dump(
                    output / "progress.json",
                    {
                        "total": len(items),
                        "completed": completed,
                        "active": len(active),
                        "not_started": len(items) - position,
                        "counts": counts,
                        "memory_available_gib": available_gib(),
                        "owned_processes": usage,
                        "elapsed_seconds": time.monotonic() - start,
                        "complete": False,
                    },
                )
                last_observation = time.monotonic()
    consolidate(config, items)
    dump(
        output / "completion.json",
        {
            "total": len(items),
            "terminal": completed,
            "counts": counts,
            "elapsed_seconds": time.monotonic() - start,
            "note": "Terminal records include failures; scientific result audit and aggregation remain separate",
        },
    )
    lock.rename(output / "supervisor.completed.json")


def consolidate(config, items):
    from .aggregation import aggregate
    from .bank import load_bank

    bank = load_bank(Path(config["bank_root"]))
    output = Path(config["output"])
    runs = [
        json.loads((output / "results" / r["request_id"] / "result.json").read_text())
        for r in items
    ]
    for mode in sorted({r["mode"] for r in items}):
        selected = [r for r in runs if r["mode"] == mode]
        dump(output / ("runs-" + mode + ".json"), selected)
        conditions = sorted(
            {
                (r["panel"], r["split"], r["noise"])
                for r in selected
                if r["evidence_role"] != "development"
            }
        )
        for panel, split, noise in conditions:
            models = sorted(
                {
                    r["model"]
                    for r in selected
                    if (r["panel"], r["split"], r["noise"]) == (panel, split, noise)
                }
            )
            summary = aggregate(
                bank,
                selected,
                panel,
                split,
                models,
                noise,
                expected_digest=config["bank_checksums_sha256"],
            )
            target = output / "aggregates" / mode / panel
            target.mkdir(parents=True, exist_ok=True)
            dump(target / (split + "-noise" + str(noise) + ".json"), summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    parser.add_argument("--require-slurm", action="store_true")
    parser.add_argument("--score-config", type=Path)
    parser.add_argument("--score-request", type=Path)
    parser.add_argument("--work", type=Path)
    args = parser.parse_args()
    if args.score_config:
        config = json.loads(args.score_config.read_text())
        score_request(config, json.loads(args.score_request.read_text()), args.work)
    else:
        supervise(json.loads(args.config.read_text()), args.require_slurm)


if __name__ == "__main__":
    main()
