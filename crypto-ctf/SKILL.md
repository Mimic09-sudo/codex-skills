---
name: crypto-ctf
description: Solve authorized CTF cryptography challenges by identifying the construction flaw, building a minimal exact solver, and verifying with round trips, local implementations, statistical baselines, or the supplied service. Use for classical ciphers, bounded hashes, nonce or keystream reuse, signatures, and custom block-cipher distinguishers.
---

# Crypto CTF

## Mission

Reduce the supplied construction to the smallest exact mathematical weakness, automate it, and verify the result against the original artifacts or authorized service.

Load `ctf-wsl-toolchain` for local runtimes and dependency discovery. Preserve original archives and captures; keep generated solvers in the task workspace.

## Triage

1. Inventory source, ciphertexts, transcripts, public parameters, oracle protocol, message lengths, encodings, padding, and query limits.
2. Rewrite the construction as equations with exact byte order, modulus, hash input, randomness lifecycle, and state reuse.
3. Separate a weak construction from a hard standard primitive. Look first for a bounded domain, repeated pad/nonce, linear or affine layer, deterministic randomness, missing authentication, or a structural distinguisher.
4. Select one lane and implement the smallest solver that proves it.

## Lanes

- Classical or modular transform: compute the inverse only after proving the multiplier or matrix is invertible; preserve case and untouched characters exactly.
- Bounded preimage: enumerate only a proven finite domain with the exact textual formatting and encoding used by the challenge.
- Keystream reuse: derive the shared stream from known plaintext and verify every recovered message by re-encryption.
- Signature failure: derive nonce/private material from the exact signature equations and verify a forged signature locally before remote use.
- Distinguisher: derive the invariant from the supplied S-box/linear layer, measure both target and random baselines, and stay within the query budget.

Read [verified patterns](references/verified-patterns.md) when the evidence matches one of these shapes.

## Solver Contract

Create a deterministic script with explicit inputs, exact widths/moduli, assertions on lengths and inverses, and a forward or independent check. For remote protocols, separate local self-test from transport logic and report the failed round or invariant on timeout/EOF.

A plausible plaintext is not a solve. Require one of:

1. byte-identical re-encryption or round trip against the supplied artifact
2. original local implementation accepts the recovered/forged value
3. statistically calibrated distinguisher separates independent target and random samples
4. the authorized original service accepts and returns its success result

Do not generalize a one-off constant, flag wrapper, or endpoint into the skill.
