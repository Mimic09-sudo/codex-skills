# Verified Forensics Patterns

## E01, NTFS, Provenance, and Counting Rules

For a challenge that mixes an E01 image, photos, deleted documents, alternate streams, and a rule document:

1. Verify the E01 media hash, then enumerate the NTFS image with filesystem-aware tools.
2. Inspect live files, deleted directory entries, ADS, and the USN journal. Renames and deletions can establish original filenames and chronology that current paths hide.
3. Attribute media using multiple fields such as owner name, camera model/serial, source path, and document relationships.
4. Deduplicate alternate names or copies only when metadata or content hashes prove they represent the same exposure.
5. Translate the supplied rule document into explicit predicates before counting categories.
6. Carve the entire media image and compare carved hashes/metadata to the known set. A claim that no additional photo exists needs this negative check.

## Ordered PDF Fragments in a Raw Filesystem

For numbered documents whose rendered pages contain handwritten or graphical fragments:

1. Identify the raw filesystem and enumerate metadata entries rather than trusting archive order.
2. Recover each numbered PDF both through a filesystem recovery tool and direct inode extraction.
3. Hash-compare the two extraction paths.
4. Render every page and extract embedded images at native resolution for ambiguous characters.
5. Reconstruct fragments in evidence-defined filename/number order.
6. Resolve lookalike glyphs from the native object and neighboring stroke shape; never rely on a single low-resolution render.

The final sequence is verified only when ordering metadata and the visual fragments agree.
