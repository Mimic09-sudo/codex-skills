---
name: pwn-general
description: Solve authorized ELF pwnable and native-memory CTF challenges with evidence-backed primitive selection, reproducible local/remote exploits, and original-target verification. Use for stack, format-string, heap, UAF, OOB, integer, seccomp, race, and Python/ctypes wrapper problems; do not use for unrelated real-world systems.
---

# Pwn General

## Mission

Reach the shortest reliable exploit path without sacrificing a promising deep solve to an arbitrary clock. Progress is measured by stronger evidence, a narrower success condition, a demonstrated primitive, and original-target verification. Elapsed time alone must never end, park, or force a lane change.

Work only on challenge artifacts and services the user owns or is authorized to test.

## Local Execution Base

Load `ctf-wsl-toolchain` before local analysis or tool execution. Use its discovered Python runner, debuggers, and path rules. Preserve the original binary and supplied loader/libc; place solvers and patched copies in the task workspace.

## Evidence-Driven Solve Loop

### Fingerprint

1. Inventory the binary, loader, libc, source, Docker files, and existing solve notes.
2. Run `scripts/pwn_triage.py` with the Python runner whose pwntools import was verified; on this laptop that is currently `python3`. Then run the target once with minimal input when safe.
3. Record architecture, mitigations, linkage, interpreter, runtime/libc version, input shape, and obvious success functions.

Do not install tools or open a decompiler before this pass shows they are needed.

### Fix the Attack Surface

Trace only attacker-controlled data and lifetime:

- stack buffer and copy/read length
- format string sink and argument position
- allocation, edit, show, delete, and index checks
- signed/unsigned or width conversions
- callback, function pointer, vtable, return address, GOT, or writable object
- seccomp allowlist and exit/trigger path

State the suspected vulnerability as one falsifiable sentence and produce the smallest crash, leak, UAF, OOB, or logic mismatch that tests it.

### Build the Primitive Ledger

Record only demonstrated capabilities:

| Primitive | Evidence | Limits |
|---|---|---|
| control | exact input and controlled field/register | offset, width, bad bytes |
| leak/read | leaked object and repeatability | truncation, alignment, count |
| write | target and written bytes | partial/full, count, charset |
| lifetime | alias/UAF/double free state | allocator version and bin state |
| trigger | return/callback/exit/flush action | preconditions and one-shot effects |

Never promote a crash to RIP control, a stale value to a stable leak, or a theoretical heap state to a primitive.

### Select One Lane

Choose the cheapest lane supported by the ledger:

- direct win/logic path before code execution
- ret2win before ret2libc; ret2libc before a long ROP chain
- format-string leak/write before a separate memory-corruption chain
- stack pivot only when the first-stage space is insufficient
- heap exploitation only when ownership or allocator corruption is demonstrated
- ORW/SROP only when seccomp or call constraints require them
- wrapper/ABI mismatch before deep native heap work for Python/ctypes targets

Read [exploit lanes](references/exploit-lanes.md) only for the selected lane. For Python/ctypes services, also read [Python/ctypes pwnables](references/python-ctypes-pwnables.md).

### Produce and Verify

Create `solve.py` immediately with:

- explicit local/remote selection
- supplied binary, loader, and libc paths
- named stages for leak, base calculation, write/control, and trigger
- assertions for every derived address and payload boundary
- timeout/EOF handling and synchronized I/O
- concise diagnostic logging that identifies the failed stage

Verify against the untouched local target. When a deployment wrapper exists, reproduce its transport (`socat`, pipe, socket, Docker, or remote protocol) before claiming success.

## Required Pivot Rules

- Repeated input probes do not produce controlled behavior: trace input length, parser conversions, and error paths instead of extending blind fuzzing.
- Crash without stable control: inspect the exact fault and stack/heap object layout; do not write the final chain.
- A leak path remains unproven after the relevant read surfaces are inspected: re-check direct win, partial overwrite, non-PIE targets, format strings, OOB reads, and protocol echoes.
- Heap path lacks a confirmed ownership bug: return to stack, format, integer, and logic surfaces.
- Local exploit fails under the service wrapper: compare loader/libc, cwd, environment, buffering, allocations, and transport.
- A repeated attempt adds no new fact, stronger primitive, or failed invariant: stop repeating it, state what was disproved, and choose the next discriminating probe. Keep the lane when new evidence still accumulates.

## Non-Negotiable Correctness

- Derive offsets with a cyclic pattern, debugger evidence, or exact layout—not visual guessing.
- Derive PIE/libc/heap bases from a demonstrated leak and matching artifact—not a remembered address.
- Respect ABI stack alignment, calling convention, endianness, integer width, and sign extension.
- Identify the actual glibc version and safe-linking/hook availability before choosing a heap technique.
- Do not assume GOT overwrite under Full RELRO or shell execution under seccomp.
- Treat one-gadget constraints as predicates to prove, not conveniences.
- Keep gadgets and state transitions minimal; reliability outranks chain cleverness.
- Re-run with ASLR across multiple fresh processes when address state matters.

## Completion Contract

Return:

1. vulnerability and root cause
2. primitive ledger with concrete evidence
3. selected lane and why cheaper lanes were rejected
4. reproducible solver/exploit path
5. local verification, deployment-path verification, and remote result when in scope
6. exact blocker and next discriminating probe if the flag is not yet recovered

A crash, debugger-only success, patched-only success, or unverified address calculation is not a solve.
