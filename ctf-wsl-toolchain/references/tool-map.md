# CTF Tool Discovery Map

Use this as a routing and discovery guide. It intentionally avoids claiming that every specialist tool is installed.

## Per-Machine Baseline

The desktop and laptop have different WSL registration names, usernames, home paths, and optional tools. Run the bundled check on the active machine and treat its output—not this file—as the current inventory.

Expected baseline candidates include `python3`, `gdb`, `file`, `strings`, `readelf`, `objdump`, `ldd`, and `checksec`. User-local tools may live under `$HOME/.local/bin` or a venv such as `$HOME/pwndbg/.venv/bin/pwndbg`; verify before use.

Run `scripts/check-toolchain.ps1` after a tool failure or environment change to refresh the evidence. Do not run the full check before every challenge.

## Baseline Triage and Build

Resolve as needed with `command -v`:

- `file`, `strings`, `xxd`, `hexdump`, `readelf`, `objdump`, `nm`, `ldd`, `checksec`
- `gcc`, `g++`, `clang`, `nasm`, `make`, `cmake`
- `strace`, `ltrace`, `patchelf`, `pwninit`
- cross-architecture QEMU user targets

## Pwn

Prefer:

- `python3` with pwntools when `import pwn` succeeds
- `gdb`, then the verified pwndbg venv path when pwndbg features are needed
- `ROPgadget`, `ropper`, `one_gadget`, and `seccomp-tools` only after `command -v` succeeds

Discover helper corpora such as how2heap, libc-database, and glibc-all-in-one under the current user's home. Do not assume another user's `/home/.../ctf-tools` tree exists.

## Reversing and Mobile

Check for the narrow tool required by the artifact:

- native: Ghidra `analyzeHeadless`, radare2 `r2`, `objdump`, `gdb`, `lldb`
- managed: Java/.NET decompilers and Mono tooling
- Android: `jadx`, `apktool`, `aapt`, `adb`
- packing/instrumentation: `upx`, Frida, capa, FLOSS

If a command is absent, check `/opt`, `/usr/local/bin`, and the current user's local tool directories before installing anything.

## Crypto and Constraints

Probe only the required runtime:

- `python3 -c "import z3"`
- `python3 -c "import Crypto"`
- `python3 -c "import sympy"`
- `sage`, `pari-gp`, `gap`, or `maxima` for challenges that justify them

## Forensics and Steganography

Common candidates include Volatility, `binwalk`, `foremost`, Sleuth Kit, `exiftool`, `yara`, oletools, `tshark`, `steghide`, `stegseek`, `zsteg`, `pngcheck`, ImageMagick, `hashcat`, and `john`. Verify availability before selecting a workflow.

## Web and Network

Use only against explicit challenge targets. Candidate tools include `tshark`, `tcpdump`, `nmap`, `ffuf`, `gobuster`, `sqlmap`, and proxy runtimes. Prefer the smallest tool that answers the current hypothesis; tool availability never expands authorization.

## Python Environment Rule

Use an existing isolated environment when one is discovered. Do not merge unrelated venvs or install into system Python merely because an older absolute path in a skill is unavailable.
