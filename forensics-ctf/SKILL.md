---
name: forensics-ctf
description: Solve authorized CTF digital-forensics challenges from disk images, E01 evidence, filesystems, deleted entries, metadata, journals, PDFs, and carved media while preserving originals and proving the final reconstruction with independent evidence.
---

# Forensics CTF

## Mission

Recover the answer from evidence without modifying the source and without treating one parser's view as complete.

Load `ctf-wsl-toolchain` for EWF, Sleuth Kit, metadata, carving, and rendering tools. Work from verified copies and keep original archives/images untouched.

## Evidence Workflow

1. Hash the source archive and evidence image. Validate container integrity and stored media hashes when available.
2. Identify partition and filesystem geometry before extracting files. Mount read-only only when a tool truly requires it; prefer direct parsers.
3. Build one inventory containing live files, deleted entries, alternate data streams, metadata, timestamps, journal records, and file identifiers.
4. Extract relevant objects by inode or metadata address, then hash-compare direct extraction with recovered copies.
5. Render documents and images for visual evidence, but retain text/metadata and native-resolution objects for ambiguous glyphs.
6. Use whole-media carving as an independent completeness check, not as a replacement for filesystem context.
7. Formalize challenge counting, attribution, ordering, and deduplication rules before computing the final answer.

Read [verified patterns](references/verified-patterns.md) when working with an E01/NTFS provenance problem or an ordered document-fragment image.

## Verification Contract

Return the answer only after two independent evidence paths agree where practical: filesystem metadata plus carving, rendered content plus direct object extraction, or provenance metadata plus journal history. Record any unrecoverable region or ambiguity explicitly; do not guess a glyph, filename, or legal/counting classification.
