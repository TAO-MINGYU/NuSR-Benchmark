"""Reproduce upstream pinned dependency recipe with double precision enabled.

Only build locations/compiler/resource settings and USE_SINGLE_PRECISION differ
from the upstream recipe. Algorithm sources are never patched.
"""

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def dependencies(script, prefix):
    tree = ast.parse(script.read_text())
    assignment = next(
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "dependencies" for t in n.targets)
    )
    common = [
        "-DCMAKE_C_COMPILER=clang",
        "-DCMAKE_CXX_COMPILER=clang++",
        "-S",
        ".",
        "-B",
        "build",
        "-DCMAKE_BUILD_TYPE=Release",
        f"-DCMAKE_INSTALL_PREFIX={prefix}",
        "-DBUILD_EXAMPLES=OFF",
        "-DBUILD_TESTING=OFF",
    ]
    names = {"default_cmake_args": common, "operon_build_preset": "build-linux"}

    def value(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return names[node.id]
        if isinstance(node, (ast.List, ast.Tuple)):
            return [value(n) for n in node.elts]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return value(node.left) + value(node.right)
        raise ValueError("Unexpected upstream build-recipe syntax")

    return value(assignment.value)


def checked(command, cwd, env, log):
    with log.open("a") as stream:
        stream.write(json.dumps(command) + "\n")
        stream.flush()
        subprocess.run(
            command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, check=True
        )


def main(args):
    root = args.build.resolve()
    root.mkdir(exist_ok=True, parents=True)
    prefix = root / "prefix"
    prefix.mkdir(exist_ok=True)
    cxx = args.compiler.resolve()
    compiler = cxx / "bin/x86_64-conda-linux-gnu-g++"
    ccompiler = cxx / "bin/x86_64-conda-linux-gnu-gcc"
    assert compiler.exists() and ccompiler.exists()
    env = os.environ.copy()
    env.update(
        PATH=os.pathsep.join(
            [str(Path(sys.executable).parent), str(cxx / "bin"), "/usr/bin", "/bin"]
        ),
        CMAKE_PREFIX_PATH=str(prefix) + ";" + str(cxx),
        PKG_CONFIG_PATH=str(cxx / "lib/pkgconfig"),
        CPATH=str(cxx / "include"),
        LIBRARY_PATH=str(cxx / "lib"),
        CMAKE_BUILD_PARALLEL_LEVEL=str(args.jobs),
        OPENBLAS_NUM_THREADS="1",
        OMP_NUM_THREADS="1",
    )
    recipe = dependencies(args.source / "script/dependencies.py", prefix)
    receipts = []
    for name, url, revision, options in recipe:
        target = root / "sources" / name
        target.parent.mkdir(exist_ok=True)
        build = root / "objects" / name
        log = root / (name + ".log")
        receipt = root / (name + ".receipt.json")
        if receipt.exists():
            saved = json.loads(receipt.read_text())
            assert saved["revision"] == revision and saved["precision"] == "float64"
            receipts.append(saved)
            continue
        if name == "Eigen3" and (cxx / "share/eigen3/cmake/Eigen3Config.cmake").exists():
            version = (cxx / "share/eigen3/cmake/Eigen3ConfigVersion.cmake").read_text()
            assert "3.4.0" in version
            saved = {
                "name": name,
                "revision": revision,
                "precision": "float64",
                "source": "exact Eigen3.4.0 headers from owned conda compiler prefix",
            }
            receipt.write_text(json.dumps(saved, indent=2))
            receipts.append(saved)
            continue
        if not target.exists():
            target.mkdir()
            checked(["git", "init", "-q"], target, env, log)
            if url.startswith("https://github.com/"):
                url = "git@github.com:" + url.split("github.com/", 1)[1] + ".git"
            checked(["git", "remote", "add", "origin", url], target, env, log)
        source_registry = root / "source-revisions.json"
        pinned = json.loads(source_registry.read_text()) if source_registry.exists() else {}
        if name not in pinned:
            checked(["git", "fetch", "--depth", "1", "origin", revision], target, env, log)
            checked(["git", "checkout", "--detach", "FETCH_HEAD"], target, env, log)
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=target, text=True).strip()
        if name in pinned:
            assert pinned[name]["revision"] == revision and pinned[name]["head"] == head
        source = target
        clean = []
        index = 0
        while index < len(options):
            option = options[index]
            if option in {"-S", "-B"}:
                if option == "-S":
                    source = target / options[index + 1]
                index += 2
                continue
            if option.startswith(("-DCMAKE_C_COMPILER=", "-DCMAKE_CXX_COMPILER=")):
                index += 1
                continue
            if option.startswith(("DBUILD_", "DGSL_")):
                option = "-" + option  # Two upstream recipe arguments omit their leading hyphen.
            clean.append(option)
            index += 1
        configure = [
            "cmake",
            *clean,
            "-G",
            "Ninja",
            "-S",
            str(source),
            "-B",
            str(build),
            f"-DCMAKE_C_COMPILER={ccompiler}",
            f"-DCMAKE_CXX_COMPILER={compiler}",
            f"-DCMAKE_PREFIX_PATH={prefix};{cxx}",
            f"-DCMAKE_INSTALL_PREFIX={prefix}",
            f"-DCMAKE_INSTALL_RPATH={prefix}/lib;{cxx}/lib",
            f"-DZLIB_ROOT={cxx}",
            f"-DZLIB_INCLUDE_DIR={cxx}/include",
            f"-DZLIB_LIBRARY={cxx}/lib/libz.so",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DBUILD_TESTING=OFF",
            "-DUSE_SINGLE_PRECISION=OFF",
        ]
        checked(configure, target, env, log)
        checked(["cmake", "--build", str(build), "--parallel", str(args.jobs)], target, env, log)
        checked(["cmake", "--install", str(build)], target, env, log)
        saved = {
            "name": name,
            "revision": revision,
            "head": head,
            "precision": "float64",
            "configure": configure,
            "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
        }
        receipt.write_text(json.dumps(saved, indent=2))
        receipts.append(saved)
        print(json.dumps({"built": name, "head": head}), flush=True)
    wheels = root / "wheels"
    wheels.mkdir(exist_ok=True)
    env["CMAKE_ARGS"] = (
        f"-DCMAKE_PREFIX_PATH={prefix};{cxx} -DCMAKE_CXX_COMPILER={compiler} "
        f"-DCMAKE_INSTALL_RPATH={prefix}/lib;{cxx}/lib -DUSE_SINGLE_PRECISION=OFF"
    )
    checked(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            str(args.source.resolve()),
            "--no-deps",
            "--no-build-isolation",
            "-w",
            str(wheels),
        ],
        root,
        env,
        root / "binding.log",
    )
    (root / "build-receipt.json").write_text(json.dumps(receipts, indent=2))
    print("Double-precision binding wheel ready", wheels, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--compiler", type=Path, required=True)
    parser.add_argument("--build", type=Path, required=True)
    parser.add_argument("--jobs", type=int, required=True)
    main(parser.parse_args())
