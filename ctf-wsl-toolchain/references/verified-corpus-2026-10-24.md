# Verified CTF Corpus Since 2026-10-24

This is a maintenance inventory, not a solve-time checklist. It reconciles the UUID/hash-named archives in Downloads, `Desktop\SWU_CTF`, saved solvers, task evidence, and the two VS Code workspaces. Answers and one-off addresses are intentionally omitted.

## Coverage

| Domain | Challenge | Reusable pattern promoted |
| --- | --- | --- |
| Rev | primary-rev | invert a finite prime table into zero-based input indices |
| Rev | Perm-mission | emulate relocation-backed handlers and invert a complete register-permutation table |
| Rev | Basic Operations | reverse independent fixed-width byte arithmetic with modular inverses |
| Rev | Parent's alarm | statically decode signal framing and alarm-remainder arithmetic instead of waiting |
| Rev | crash_snapshot | satisfy an explicit patch-binary contract with a minimal hook and code cave |
| Rev | Bug | follow overlapping instruction streams and replay the exact xorshift state |
| Crypto | Baby Affine | preserve case/nonletters and round-trip a modular affine inverse |
| Crypto | Baby OTP | enumerate a bounded six-digit SHA-256 preimage domain exactly |
| Crypto | Second Transmission | recover a reused XOR pad from known plaintext and re-encrypt both captures |
| Crypto | Textbook-ECDSA | recover nonce/private key from repeated `r` and forge only after local verification |
| Crypto | Textbook SPN | build and statistically validate a partition-boomerang distinguisher against random permutations |
| Pwn | SCribe | use auxv to recover PIE inside seccomp-limited injected shellcode |
| Pwn | Second Draft | turn a shallow alias UAF into a typed callback leak and overwrite |
| Pwn | cute_recoder | prefer a direct type-confusion arbitrary write into a writable GOT entry |
| Pwn | dog flag | reconstruct a safe-linked tcache pointer from a truncated leak and poison a stack target |
| Pwn | unsafe_ctypes | model Python/ctypes lifetime, stale length, hidden allocations, and cross-mapping relocation targets |
| Pwn | Reservation Manager | chain non-NUL leak, stale-tail UAF, double free, unsorted leak, stack leak, and final control |
| Forensics | The Missing Seventh Cat | combine E01 filesystem metadata, ADS, deleted entries, USN evidence, provenance, and whole-media carving |
| Forensics | Suspicious Files | enumerate a FAT image, render ordered PDFs, and hash-match direct inode extraction to recovered copies |
| Web | Carbon Copy | enforce authorization on the selected child revision and exported attachment graph |
| Web | OpsPortal | distrust client proxy headers and reject absolute paths in internal download endpoints |
| Web | Unfiltered | treat JSON query operators that compile strings as code execution sinks |
| Web | AtlasDocs | compare validator/fetcher URL parsers and track percent-decoding into HTTP headers |
| Web | Systemic | audit framework role routing, template globals, DI access, and database reachability as one chain |

Totals: 6 reversing, 5 crypto, 6 pwn, 2 forensics, and 5 web challenges; 24 verified problems overall.

## Writeback Map

- Reversing patterns live in `rev-sol-bridge/references/local-corpus-patterns.md` and are selected through `rev-sol-bridge`.
- Pwn patterns live in `pwn-general/references/verified-local-patterns.md` with the existing ctypes guide for wrapper-specific details.
- Crypto, forensics, and web patterns live in the dedicated `crypto-ctf`, `forensics-ctf`, and `web-ctf` skills.
