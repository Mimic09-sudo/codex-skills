# Verified Crypto Patterns

These patterns were distilled from five verified solves. Apply them only when the supplied construction has the matching evidence.

## Affine Alphabet Transform

For `y = a*x + b mod m`, first prove `gcd(a, m) = 1`, then compute `a^-1 mod m` and recover `x = a^-1*(y-b) mod m`. Apply the transform separately to uppercase and lowercase alphabets and leave punctuation unchanged. The solver must re-encrypt the recovered text byte-for-byte.

## Bounded Formatted Hash Preimage

When the server hashes a fixed-width decimal OTP, the domain is not an open cryptographic preimage problem.

1. Confirm the range and formatting, including leading zeroes.
2. Hash the exact encoded candidate bytes.
3. Build a lookup or stream the million-scale domain once.
4. Test against a local challenge process, then submit only the recovered formatted value.

Do not widen the search beyond the proven domain.

## Reused XOR Pad

For equal-length captures `C1 = P1 xor K` and `C2 = P2 xor K`, recover `K = C1 xor P1`, then `P2 = C2 xor K`. Preserve the challenge's fixed-length space or zero padding. Assert that re-encrypting both plaintexts reproduces both original ciphertexts exactly.

## Reused ECDSA Nonce

If two signatures share the same `r` under the same key and curve order `n`:

1. Compute message integers with the implementation's exact hash conversion.
2. Recover `k = (z1-z2) * (s1-s2)^-1 mod n`.
3. Recover `d = (s1*k-z1) * r^-1 mod n`.
4. Verify the recovered key or both signatures before forging the requested message.
5. Reject zero or non-invertible denominators and do not assume nonce reuse when `r` differs.

## Partition-Boomerang SPN Distinguisher

When a custom SPN plants high-probability S-box boomerang transitions and a compatible linear layer:

1. Recompute relevant DDT/BCT entries and linear-layer propagation from the supplied code.
2. Construct query structures that enumerate the intended input partition while fitting the block budget.
3. Apply the chosen ciphertext difference, decrypt, and count collisions in the predicted output partition or coset.
4. Calibrate the score across many independent SPN keys and lazy random permutations. Choose the decision threshold from observed separation, not intuition.
5. Run a full-size local simulation before the long remote protocol and log progress per outer round.

A single collision or one key is not a calibrated distinguisher.
