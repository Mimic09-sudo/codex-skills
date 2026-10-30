---
name: ctf-koth-solver
description: Build and optimize accepted solvers for authorized King-of-the-Hill CTF challenges using the supplied interface, checker, and official Cost model. Use when a challenge grades solver correctness and ranks correct submissions by Cost.
---

# CTF KotH Solver

## Goal

Produce the lowest-Cost reliably accepted solver for the supplied problem. A recovered flag alone is not completion when the challenge requires solver submission.

Load `ctf-wsl-toolchain` for execution and the matching Rev, Pwn, Crypto, Forensics, or Web skill for the solve method. This skill controls only solver construction, measurement, optimization, and final candidate selection.

## Read the Problem Contract

Before optimizing, extract from the supplied files:

- solver input/output format and invocation
- correctness, timeout, and failure conditions
- official Cost formula and aggregation method
- allowed runtime, dependencies, concurrency, and resources
- instance distribution, randomness, and submission packaging

Use the official checker and Cost output as the source of truth. Do not optimize against a guessed proxy when the real metric is available.

## Fast Workflow

1. Build the smallest correct baseline with the applicable domain skill.
2. Run the official checker and record acceptance plus Cost components.
3. Preserve the accepted baseline and profile the dominant Cost component.
4. Optimize in this order: algorithm/search space, solver or oracle calls, repeated target launches, parsing/I/O, allocations/data layout, then micro-optimization.
5. Re-run correctness and Cost regression tests on representative and randomized instances after every material change.
6. Promote a candidate only when it remains accepted and improves the official objective under the same measurement environment.
7. Validate the exact final file/package, record its hash and Cost, and keep it distinct from experimental candidates.

Read [KotH optimization](references/koth-optimization.md) after the baseline works or when the Cost model determines the algorithm.

## Required Gates

- no hardcoded event flag or one-instance answer
- deterministic behavior or an explicit seed and bounded failure probability
- bounded runtime, memory, requests, retries, and output
- exact protocol parsing with useful timeout/EOF failures
- compatibility with the allowed runtime and dependencies
- clean required output and exit status
- acceptance on the supplied or official checker
- repeated official-Cost measurement on representative instances
- preserved accepted baseline and identified final candidate

Report the solver path, exact verification result, official Cost, variance or worst case, final hash, and remaining uncertainty. Actual contest submission is performed only when the user explicitly requests it.
