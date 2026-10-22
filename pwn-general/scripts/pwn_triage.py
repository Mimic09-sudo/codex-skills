#!/usr/bin/env python3
"""Read-only first-pass triage for ELF pwnable challenge binaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ANCHOR_RE = re.compile(
    r"(?i)(flag|win|shell|success|correct|/bin/sh|system|execve|puts|printf|"
    r"gets|scanf|read|write|malloc|calloc|realloc|free|seccomp|mprotect|"
    r"ptrace|stack_chk|fortify)"
)


def run(command: list[str], timeout: float) -> dict[str, Any]:
    executable = shutil.which(command[0])
    if executable is None:
        return {"command": command[0], "available": False}
    try:
        completed = subprocess.run(
            [executable, *command[1:]],
            check=False,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"command": command[0], "available": True, "timeout": True}
    return {
        "command": command[0],
        "available": True,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def unique_matching_lines(text: str, limit: int) -> list[str]:
    results: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line and ANCHOR_RE.search(line) and line not in seen:
            seen.add(line)
            results.append(line)
            if len(results) >= limit:
                break
    return results


def pwntools_facts(path: Path) -> dict[str, Any]:
    try:
        from pwn import ELF, context  # type: ignore

        context.log_level = "error"
        elf = ELF(str(path), checksec=False)
        symbols = sorted(name for name in elf.symbols if ANCHOR_RE.search(name))[:80]
        return {
            "available": True,
            "arch": elf.arch,
            "bits": elf.bits,
            "endian": elf.endian,
            "entry": hex(elf.entry),
            "pie": bool(elf.pie),
            "nx": bool(elf.nx),
            "canary": bool(elf.canary),
            "relro": str(elf.relro),
            "executable_stack": bool(elf.execstack),
            "interesting_symbols": symbols,
        }
    except Exception as error:
        return {"available": False, "error": f"{type(error).__name__}: {error}"}


def collect(path: Path, timeout: float, max_anchors: int) -> dict[str, Any]:
    raw = path.read_bytes()
    result: dict[str, Any] = {
        "target": str(path.resolve()),
        "size": len(raw),
        "sha256": sha256(path),
        "magic": raw[:16].hex(),
        "is_elf": raw.startswith(b"\x7fELF"),
    }
    result["file"] = run(["file", "-b", str(path)], timeout)
    result["pwntools"] = pwntools_facts(path)
    result["interpreter"] = run(["readelf", "-W", "-l", str(path)], timeout)
    result["dynamic"] = run(["readelf", "-W", "-d", str(path)], timeout)
    strings_result = run(["strings", "-a", "-n", "4", str(path)], timeout)
    result["anchors"] = unique_matching_lines(
        strings_result.get("stdout", ""), max_anchors
    )
    return result


def render_markdown(data: dict[str, Any]) -> str:
    pwntools = data["pwntools"]
    lines = [
        "# Pwn triage",
        "",
        f"- Target: `{data['target']}`",
        f"- Size: `{data['size']}` bytes",
        f"- SHA-256: `{data['sha256']}`",
        f"- ELF: `{data['is_elf']}`",
    ]
    file_out = data["file"].get("stdout")
    if file_out:
        lines.append(f"- File: `{file_out}`")
    if pwntools.get("available"):
        lines.extend(
            [
                f"- Architecture: `{pwntools['arch']}/{pwntools['bits']} {pwntools['endian']}`",
                f"- Mitigations: `PIE={pwntools['pie']} NX={pwntools['nx']} Canary={pwntools['canary']} RELRO={pwntools['relro']}`",
                f"- Entry: `{pwntools['entry']}`",
            ]
        )
    else:
        lines.append(f"- Pwntools: `{pwntools.get('error', 'unavailable')}`")

    interpreter_lines = [
        line.strip()
        for line in data["interpreter"].get("stdout", "").splitlines()
        if "interpreter" in line.lower()
    ]
    if interpreter_lines:
        lines.append(f"- Interpreter: `{interpreter_lines[0]}`")

    dependency_lines = [
        line.strip()
        for line in data["dynamic"].get("stdout", "").splitlines()
        if any(marker in line for marker in ("(NEEDED)", "(RPATH)", "(RUNPATH)"))
    ]
    if dependency_lines:
        lines.extend(["", "## Dependencies", ""])
        lines.extend(f"- `{line}`" for line in dependency_lines[:20])

    symbols = pwntools.get("interesting_symbols", [])
    anchors = data.get("anchors", [])
    lines.extend(["", "## High-signal anchors", ""])
    if symbols:
        lines.append("- Symbols: " + ", ".join(f"`{value}`" for value in symbols))
    if anchors:
        lines.extend(f"- `{value}`" for value in anchors)
    if not symbols and not anchors:
        lines.append("- No high-signal symbol or string found; trace input and compare boundaries next.")

    lines.extend(
        [
            "",
            "## Next discriminating probes",
            "",
            "1. Run once with minimal input and record the exact I/O state machine.",
            "2. Trace attacker-controlled length, index, format, pointer, and lifetime values.",
            "3. Produce one minimal crash/leak/read/write/lifetime proof before choosing a chain.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only, bounded ELF pwnable triage. Does not execute the target."
    )
    parser.add_argument("target", type=Path)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--max-anchors", type=int, default=40)
    args = parser.parse_args()

    if args.timeout <= 0 or args.max_anchors <= 0:
        parser.error("--timeout and --max-anchors must be positive")
    if not args.target.is_file():
        parser.error(f"target is not a file: {args.target}")

    data = collect(args.target, args.timeout, args.max_anchors)
    print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else render_markdown(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
