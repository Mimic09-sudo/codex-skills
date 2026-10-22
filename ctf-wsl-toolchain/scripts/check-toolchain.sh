#!/usr/bin/env bash
set -uo pipefail

export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"

printf 'distro=%s\n' "$(. /etc/os-release && printf '%s %s' "$NAME" "$VERSION_ID")"
printf 'user=%s\n' "$(id -un)"

baseline_missing=0
for command_name in python3 file strings readelf objdump ldd gdb checksec; do
    if command_path="$(command -v "$command_name" 2>/dev/null)"; then
        printf 'baseline %-14s %s\n' "$command_name" "$command_path"
    else
        printf 'baseline %-14s MISSING\n' "$command_name"
        baseline_missing=1
    fi
done

for command_name in ctf-python pwndbg gdb-gef r2 analyzeHeadless sage ROPgadget ropper one_gadget seccomp-tools patchelf pwninit; do
    if command_path="$(command -v "$command_name" 2>/dev/null)"; then
        printf 'optional %-14s %s\n' "$command_name" "$command_path"
    else
        printf 'optional %-14s not found\n' "$command_name"
    fi
done

if python3 -c 'import pwn' >/dev/null 2>&1; then
    printf 'python import pwn           OK\n'
else
    printf 'python import pwn           unavailable\n'
fi

for module_name in angr z3 capstone unicorn Crypto; do
    if python3 -c "import $module_name" >/dev/null 2>&1; then
        printf 'python import %-13s OK\n' "$module_name"
    else
        printf 'python import %-13s unavailable\n' "$module_name"
    fi
done

pwndbg_venv="$HOME/pwndbg/.venv/bin/pwndbg"
if [[ -x "$pwndbg_venv" ]]; then
    printf 'optional pwndbg-venv    %s\n' "$pwndbg_venv"
fi

exit "$baseline_missing"
