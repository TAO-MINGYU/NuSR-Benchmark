"""Freeze reviewed source, native runtimes and the complete external-only matrix."""

import argparse
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

from nuclearbench.external_prepare import canonical, identity
from nuclearbench.external_profiles import PROFILES
from nuclearbench.external_worker import dump
from nuclearbench.sources import digest


def bundle(runtime, output):
    archive = output / "runtime-packages.tar.gz"
    if archive.exists():
        raise ValueError("Preserve existing bundle; choose a new output for a new freeze")
    main = Path(runtime["main_python"]).parent.parent / "lib/python3.11/site-packages"
    overlay = Path(runtime["aifeynman_python"]).parent.parent / "lib/python3.10/site-packages"
    base = Path(runtime["aifeynman_bin"]).parent / "lib/python3.10/site-packages"

    def omit_cache(info):
        parts = Path(info.name).parts
        return None if "__pycache__" in parts or info.name.endswith(".pyc") else info

    with tarfile.open(archive, "w:gz", compresslevel=1) as stream:
        for name, source in (("main", main), ("aif-overlay", overlay), ("aif-base", base)):
            print("Bundling " + name, flush=True)
            stream.add(source, arcname=name, filter=omit_cache)
    dump(output / "runtime-bundle.json", {"path": str(archive), "sha256": digest(archive)})


def freeze(source, runtime, matrix, output):
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=source, text=True).strip():
        raise ValueError("Commit and verify the exact source before freezing")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
    snapshot = output / "snapshots" / commit
    snapshot.mkdir(parents=True, exist_ok=False)
    files = subprocess.check_output(["git", "ls-files", "-z"], cwd=source).decode().split("\0")
    for name in filter(None, files):
        destination = snapshot / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / name, destination)
    # Reuse only immutable answer-free payloads. All profile and request identities
    # are rebuilt from the final preregistered recipes, without observing results.
    final = output / "matrix-final"
    final.mkdir(exist_ok=False)
    items = []
    for line in (matrix / "requests.jsonl").read_text().splitlines():
        item = json.loads(line)
        item.pop("request_id")
        item["profile"] = PROFILES[item["model"]]
        item["request_id"] = identity(item)
        items.append(item)
    items.sort(key=lambda item: item["request_id"])
    with (final / "requests.jsonl").open("w") as stream:
        for item in items:
            stream.write(canonical(item) + "\n")
    payloads = json.loads((matrix / "payload-inventory.json").read_text())
    for item in payloads:
        if digest(Path(item["path"])) != item["sha256"]:
            raise ValueError("Previously prepared payload changed: " + item["path"])
    shutil.copy2(matrix / "payload-inventory.json", final / "payload-inventory.json")
    summary = json.loads((matrix / "matrix-summary.json").read_text())
    summary.update(
        matrix_sha256=digest(final / "requests.jsonl"),
        profile_refresh_from=str(matrix),
        source_commit=commit,
    )
    dump(final / "matrix-summary.json", summary)
    archive = json.loads((output / "runtime-bundle.json").read_text())
    if digest(Path(archive["path"])) != archive["sha256"]:
        raise ValueError("Frozen package bundle changed")
    inventory = {str(p): digest(p) for p in snapshot.rglob("*") if p.is_file()}
    for name in ("Project.toml", "Manifest.toml", "LocalPreferences.toml"):
        path = Path(runtime["julia_project"]) / name
        inventory[str(path)] = digest(path)
    for executable in ("main_python", "aifeynman_python", "julia_executable"):
        path = Path(runtime[executable]).resolve()
        inventory[str(path)] = digest(path)
    for path in Path(runtime["aifeynman_bin"]).glob("feynman*"):
        if path.is_file():
            inventory[str(path)] = digest(path)
    inventory[str(final / "payload-inventory.json")] = digest(final / "payload-inventory.json")
    dump(output / "source-inventory.json", inventory)
    config = {
        "source_commit": commit,
        "source_root": str(snapshot),
        "bank_root": str(snapshot),
        "bank_checksums_sha256": digest(snapshot / "checksums.json"),
        "runtime": runtime,
        "runtime_bundle": archive["path"],
        "runtime_bundle_sha256": archive["sha256"],
        "source_inventory": str(output / "source-inventory.json"),
        "source_inventory_sha256": digest(output / "source-inventory.json"),
        "requests": str(final / "requests.jsonl"),
        "matrix_sha256": summary["matrix_sha256"],
        "workers": 256,
        "output": str(output),
        "config_path": str(output / "campaign.json"),
        "protocol": {
            "selection": "validation only; sealed before test prediction; no reselection or refit",
            "work_budget": "method-native practical recipes; not equal CPU or evaluation work",
            "failures": "retain all terminal records and native artifacts; no best retry",
            "products_included": False,
            "task_count": 151,
            "request_count": 79630,
            "development": "run but exclude from confirmatory aggregates",
        },
    }
    config["campaign_sha256"] = identity(config)
    dump(output / "campaign.json", config)
    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["bundle", "freeze"])
    parser.add_argument("--source", type=Path)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--matrix", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    runtime = json.loads(args.runtime.read_text())
    if args.action == "bundle":
        bundle(runtime, args.output)
    else:
        print(
            json.dumps(freeze(args.source.resolve(), runtime, args.matrix, args.output), indent=2)
        )
