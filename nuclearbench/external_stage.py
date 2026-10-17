"""Stage the frozen Python package layers once inside the single Slurm step."""

import argparse
import json
import os
import shutil
import socket
import subprocess
import tarfile
import time
from pathlib import Path

from .external_campaign import environment, supervise, verify_config
from .external_prepare import identity
from .external_worker import dump
from .sources import digest


def stage(config_path):
    start, cpu_start = time.monotonic(), time.process_time()
    config = verify_config(json.loads(config_path.read_text()))
    if not os.environ.get("SLURM_JOB_ID") or socket.gethostname().split(".")[0] != "node2":
        raise ValueError("The frozen full campaign must run inside its node2 allocation")
    if len(os.sched_getaffinity(0)) != 256:
        raise ValueError("Slurm step must bind exactly 256 logical CPUs")
    archive = Path(config["runtime_bundle"])
    if digest(archive) != config["runtime_bundle_sha256"]:
        raise ValueError("Runtime package bundle changed")
    candidates = [Path(os.environ.get("SLURM_TMPDIR", "/tmp")), Path("/dev/shm")]
    root = next(
        (
            p
            for p in candidates
            if p.is_dir()
            and os.access(p, os.W_OK)
            and shutil.disk_usage(p).free > max(30 * 2**30, archive.stat().st_size * 5)
        ),
        None,
    )
    if root is None:
        raise RuntimeError("Insufficient node-local scratch; no silent shared-filesystem full run")
    target = root / ("nusr-external-runtime-" + os.environ["SLURM_JOB_ID"])
    target.mkdir(exist_ok=False)
    with tarfile.open(archive) as stream:
        stream.extractall(target, filter="data")
    effective = dict(config)
    effective["registration_sha256"] = config["campaign_sha256"]
    effective["runtime"] = dict(config["runtime"])
    effective["runtime"]["stage_sites"] = {
        "main": [str(target / "main")],
        "aifeynman": [str(target / "aif-overlay"), str(target / "aif-base")],
    }
    effective_path = Path(config["output"]) / "effective-config.json"
    effective["config_path"] = str(effective_path)
    effective.pop("campaign_sha256")
    effective["campaign_sha256"] = identity(effective)
    dump(effective_path, effective)
    for kind, model in [("main", "PySR"), ("aifeynman", "AI_Feynman")]:
        python, env = environment(effective, model, target)
        output = Path(config["output"]) / ("node-runtime-" + kind + ".json")
        with (Path(config["output"]) / ("node-runtime-" + kind + ".log")).open("w") as log:
            subprocess.run(
                [
                    python,
                    "-m",
                    "nuclearbench.external_probe",
                    "--kind",
                    kind,
                    "--output",
                    str(output),
                ],
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=True,
            )
    dump(
        Path(config["output"]) / "staging.json",
        {
            "runtime_bundle_sha256": config["runtime_bundle_sha256"],
            "node_local_path": str(target),
            "wall_seconds": time.monotonic() - start,
            "cpu_seconds": time.process_time() - cpu_start,
            "registration_sha256": config["campaign_sha256"],
            "effective_sha256": effective["campaign_sha256"],
        },
    )
    supervise(effective, require_slurm=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    stage(parser.parse_args().config)
