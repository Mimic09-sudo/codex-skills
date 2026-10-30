# Verified Local Pwn Patterns

Use these playbooks only when target evidence matches the shape. They were distilled from six locally solved and original-target-verified challenges; offsets, flags, and one-off payload bytes are intentionally omitted.

## Seccomp-Limited Injected Code with No PIE Leak

When injected shellcode runs but seccomp allows only a narrow syscall such as `write`:

1. Dump the actual filter and identify the permitted syscall and argument constraints.
2. If the shellcode inherits a stack frame, scan the initial stack for a validated auxiliary-vector entry such as `AT_PHDR`.
3. Derive the PIE base from the program-header address and confirm the ELF magic before using it.
4. Address the in-memory flag or secret relative to that proven base and invoke only the admitted syscall.

This can be shorter and more reliable than constructing a generic ROP chain.

## Shallow Alias UAF into a Typed Callback Object

When a duplicate operation copies only a pointer:

1. Prove that deleting one logical object frees storage still referenced by its alias.
2. Allocate a different object of the same chunk size and inspect the stale alias as the new type.
3. Treat the overlap as a structured leak/write primitive. A callback object can disclose a libc function, self pointer, state fields, and later accept a forged callback plus argument.
4. Preserve fields required by the trigger instead of overwriting the whole object blindly.
5. Trigger through the program's normal callback path and verify the libc base is page-aligned and matches a second invariant.

## Type Confusion before Heap Complexity

When two C++ classes share a compatible prefix but one method interprets a field as a destination pointer:

1. Write the actual layouts and vtable/field offsets.
2. Confirm the confused call yields an exact arbitrary write.
3. Re-check RELRO and PIE. Under partial RELRO and non-PIE, a direct GOT-to-existing-win-function overwrite is cheaper than libc leakage or heap manipulation.
4. Trigger the overwritten import through an existing menu action.

## Reconstruct Safe-Linking from a Truncated Leak

When a UAF or non-NUL print exposes only the high bytes of an encoded tcache forward pointer:

1. Enumerate the missing low byte or other small unknown domain.
2. Iteratively invert `encoded = next ^ (chunk >> 12)` and filter candidates with allocator alignment and known adjacency.
3. Require a unique `(current_chunk, next_chunk)` pair before poisoning.
4. Encode the chosen target with the recovered source chunk address and respect partial-write/NUL limits.
5. If the final target is stack data rather than control flow, use the poisoned allocation to rewrite the program's command or argument buffer and trigger the existing action.

## Stale Linked-List Nodes into a Full Heap Chain

When deleting the tail updates the global tail but leaves the predecessor's `next` pointer intact:

1. Use a full-length non-NUL string beside link pointers to leak an adjacent heap address.
2. Confirm the freed tail remains searchable and editable through the list: this is the UAF primitive.
3. Corrupt the tcache key before a second free, then encode the poisoned forward pointer with the exact freed-chunk address.
4. If libc is still unknown, use the arbitrary allocation to enlarge a legitimate chunk, free it into the unsorted bin, and leak the arena pointer through the stale list.
5. Leak `environ` or an equivalent stack anchor only after libc is proven. Derive the saved-control location from runtime evidence, not a copied delta.
6. Write the minimal final chain and account for deployment libc patch-level drift by deriving gadgets and symbols from the supplied or leaked runtime.

Each step must remain independently reproducible; a long chain is not evidence that any intermediate primitive works.

## Python/ctypes UAF and Cross-Mapping Targets

Also read [Python/ctypes pwnables](python-ctypes-pwnables.md).

1. Check whether `free_array` or an equivalent native function leaves the pointer in the Python-visible array. If so, wrapper `read` and `modify` may remain usable on freed chunks.
2. Model how tcache metadata overwrites the native structure's logical length. A freed object's encoded forward pointer can turn a bounded writer into a much larger stale-object write.
3. Account for Python input conversion, `c_char_p` NUL termination, and hidden allocations while shaping bins.
4. Distinguish the shared library, Python executable, libc, and heap mappings. Derive cross-mapping deltas from live leaks or mappings for the active build.
5. Prefer a narrow relocation overwrite when the loaded native library still has a writable import entry. A call such as `free(pointer)` can become a command trigger if the pointed object begins with attacker-controlled command bytes.
6. Verify through the real Python plus `socat`/socket transport; direct native-library testing alone is insufficient.
