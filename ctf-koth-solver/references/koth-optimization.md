# KotH Solver Optimization

Use this only after the solver is correct or when the Cost model directly determines the algorithm.

## Establish the Measurement Contract

Extract the official objective exactly: which resources contribute to Cost, how failures are scored, whether the result is a sum/mean/maximum/percentile, and which limits cause rejection. Fix the runtime, CPU allocation, dependency versions, warm/cold state, seed set, and timeout before comparing versions.

Keep a small measurement record per candidate:

| Candidate | Accepted cases | Cost summary | Variance/worst case | Hash | Decision |
| --- | ---: | ---: | ---: | --- | --- |

Use the official harness output as the source of truth. Wall-clock time is only a proxy when the official metric says so.

## Correctness Corpus

Build a representative local set from supplied samples and generated instances that obey the problem distribution. Include minimum/maximum sizes, empty or degenerate structures, adversarial branch patterns, malformed-but-legal boundaries, and multiple seeds. Do not train only on the public sample or the current live instance.

Every promoted candidate must:

1. match the baseline on all known legal cases
2. pass the official checker
3. avoid hardcoded flags, instance IDs, addresses, or random seeds unless they are part of the specification
4. fail cleanly rather than emitting an invalid answer on an unsupported input

## Optimization Order

Profile first, then optimize the dominant official Cost component.

1. Reduce asymptotic complexity, search dimension, state count, or solver calls.
2. Reduce oracle queries, network round trips, process startups, and repeated parsing.
3. Precompute only instance-invariant data permitted by the rules; cache using a key that proves validity.
4. Replace heavyweight native emulation, symbolic execution, or repeated target launches with a compact model after its contract is verified.
5. Improve data layout, batching, allocation count, serialization, and I/O.
6. Use concurrency or vectorization only when the harness permits it and deterministic correctness is preserved.
7. Apply language-level micro-optimizations last.

An optimization that changes the problem semantics or exploits the benchmark harness instead of solving valid instances is invalid even if measured Cost falls.

## Variance and Failure Risk

Measure multiple seeds/runs. Compare the statistic used by the judge and also inspect the worst legal case. Bound randomized algorithms with a deterministic fallback or a proven failure probability compatible with the round rules. Remove debug output, uncontrolled retries, sleeps, and interactive prompts from the submission artifact.

## Baseline and Candidate Discipline

- Keep one immutable known-good baseline.
- Develop optimization candidates separately and assign each a reproducible hash.
- Promote only after correctness and Cost regression gates pass.
- Near a round boundary, prefer the verified baseline over an incompletely tested lower-Cost candidate.
- Before submission, validate the exact packaged file rather than a neighboring working copy.

## Submission Gate

Confirm the required filename/archive structure, entrypoint, interpreter, dependencies, permissions, output format, timeout, and official Cost. Record the final hash and whether this version is intended to become the last submission. Submission itself is performed only after the user explicitly asks for it.
