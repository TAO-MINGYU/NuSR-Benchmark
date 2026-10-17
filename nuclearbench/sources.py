"""Pinned upstream releases. Never import a fitted model or NuSR data bundle."""

import hashlib
from pathlib import Path
from urllib.request import Request, urlopen

AME = "https://www-nds.iaea.org/amdc/ame2020/"
SOURCES = {
    "mass_1.mas20.txt": (
        AME + "mass_1.mas20.txt",
        "e8599c6d7f724fac91934e59f1b9de8fb8f63e820f4b39456b790665ed2a3307",
    ),
    "rct1.mas20.txt": (
        AME + "rct1.mas20.txt",
        "e6ba1d2256f90053464c48e24d44691828dc49820ce64054aa418d834cc18e90",
    ),
    "rct2_1.mas20.txt": (
        AME + "rct2_1.mas20.txt",
        "78765c7b3f3c991ce2b6ff3b5c086a135aad1807d07819f806ab9a9150a4c2c7",
    ),
    "radii.html": (
        "https://www-nds.iaea.org/radii/",
        "2e68fe0277140f32073a7403ee1051bc2d28b3245fd1e89964bb0d50228becf3",
    ),
    "be2-adopted.json": (
        "https://www.nndc.bnl.gov/be2/data/adopted-entries.json",
        "a3f45fcf38f40b6ca3a7ebe03d9a468cc748d3480f3576bb4972ced76c703688",
    ),
    "ensdf_260901.zip": (
        "https://www.nndc.bnl.gov/ensdfarchivals/distributions/dist26/ensdf_260901.zip",
        "cd5ee83ea1b5926bb44eb9c4559f637276d9aadb76d378b888c08c6c07c0ba3b",
    ),
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_raw(raw):
    for name, (_, expected) in SOURCES.items():
        if digest(Path(raw) / name) != expected:
            raise ValueError(f"Source hash mismatch: {name}; do not silently update a release")


def fetch(raw, snapshots=Path("source_snapshots")):
    raw = Path(raw)
    raw.mkdir(parents=True, exist_ok=True)
    for name, (url, expected) in SOURCES.items():
        dest = raw / name
        if dest.exists() and digest(dest) == expected:
            continue
        bundled = Path(snapshots) / name
        if bundled.exists():
            if digest(bundled) != expected:
                raise ValueError(f"Bundled source hash mismatch: {name}")
            data = bundled.read_bytes()
            temporary = dest.with_suffix(dest.suffix + ".tmp")
            temporary.write_bytes(data)
            temporary.replace(dest)
            continue
        request = Request(
            url,
            headers={
                "User-Agent": "NuSR-Benchmark/1.0 (+https://github.com/TAO-MINGYU/NuSR-Benchmark)"
            },
        )
        try:
            with urlopen(request, timeout=90) as response:
                data = response.read()
        except OSError as error:
            raise OSError(f"Cannot retrieve {name} from {url}: {error}") from error
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(
                f"Upstream has changed: {name}. Obtain the locked snapshot, not newer data."
            )
        temporary = dest.with_suffix(dest.suffix + ".tmp")
        temporary.write_bytes(data)
        temporary.replace(dest)
