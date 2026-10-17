"""Pinned upstream releases. Never import a fitted model or NuSR data bundle."""

import hashlib
from pathlib import Path
from urllib.request import Request, urlopen

AME = "https://www-nds.iaea.org/amdc/ame2020/"
SOURCES = {
    "mass16.txt": (
        "https://www-nds.iaea.org/amdc/ame2016/mass16.txt",
        "2167f57a2a98331e4649b2dd2b658a9006ed4fba1975729ebfe52a42b4b9218a",
    ),
    "rct1-16.txt": (
        "https://www-nds.iaea.org/amdc/ame2016/rct1-16.txt",
        "f0200d338083021d6077f768390f6447f8dc32f4677aef27a23a8ad4a201b853",
    ),
    "rct2-16.txt": (
        "https://www-nds.iaea.org/amdc/ame2016/rct2-16.txt",
        "cd7ff26ccde00659e2101afd8bf731e2e30a0645ac54e4ca402d5e17c49f6f0f",
    ),
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

# Original IAEA/AMDC bytes and the IAEA's immutable official RIPL-4 Git snapshot.
RIPL4_REVISION = "54afc19a4f7c861d28237c1da812d4cf385b528d"
RIPL4_BASE = "https://raw.githubusercontent.com/IAEA-NDS/RIPL-4/" + RIPL4_REVISION + "/"
EXTRA_SOURCES = {
    "magn_mom_recomm.csv": (
        "https://www-nds.iaea.org/nuclearmoments/magn_mom_recomm.csv",
        "07f80b8c525b2cef276064f61644238adea3ae992018de94be971470ebbad9dd",
    ),
    "elec_mom_recomm.csv": (
        "https://www-nds.iaea.org/nuclearmoments/elec_mom_recomm.csv",
        "e5db6757b13062e79e85456e77fbbfa3d2f1adefbd00bda69c738b06ad640c25",
    ),
    "nubase_4.mas20.txt": (
        AME + "nubase_4.mas20.txt",
        "1585a5eea86c5e17e90307c7e6e786d060049c4039e392a261ff6db977df9859",
    ),
    "ripl4-gdr-slo.dat": (
        RIPL4_BASE + "gamma/gdr-parameters_exp%26systematics_slo.dat",
        "aa7953131339d41e7a9ada8486ccca11b730e6b453231d29ae9f70448043d3b8",
    ),
    "ripl4-gdr.readme": (
        RIPL4_BASE + "gamma/gdr-parameters_exp%26systematics_slo%26smlo.readme",
        "3f36b878d74542f24c1fb32f8903588488dfb792a5501886946f1b7a83e35b0f",
    ),
    "ripl4-resonances-L0.dat": (
        RIPL4_BASE + "resonances/resonances_L0.dat",
        "4b9a69a6cb88fc8a9041cbded583aa2b34bfc0cac31054f99fc72a35078fa726",
    ),
    "ripl4-resonances.readme": (
        RIPL4_BASE + "resonances/resonances.readme",
        "8d2cc06020fabbfe25438015ad7df3a68d8194e70ed2bfe49e6f604cbfff88a0",
    ),
    "ripl4-fission.dat": (
        RIPL4_BASE + "fission/empirical-barriers-ripl4.dat",
        "652ee510fde7ffceb8b4a2447dc3352cba53d438d1757990d238b7d1f306a6c7",
    ),
    "ripl4-fission.readme": (
        RIPL4_BASE + "fission/empirical-barriers-ripl4.readme",
        "335640570085c455aa175590b06657f169f3f230461dc5706f01e6e48d5f884c",
    ),
}
SOURCES.update(EXTRA_SOURCES)


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
                "User-Agent": "NuSR-Benchmark/0.2 (+https://github.com/TAO-MINGYU/NuSR-Benchmark)"
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
