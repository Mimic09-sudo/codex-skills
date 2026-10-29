# Game-Engine Reversing

Read this only when the winning condition depends on a game engine, scene, asset, save, replay, tick loop, or authoritative game-state check. Keep the shared bridge kernel active: find the success sink, model the minimum state, produce a reproducible artifact, and verify against the untouched target.

## Engine and boundary gate

Identify the engine before choosing tools, then separate game logic from renderer and framework code.

| Evidence | First useful boundary |
| --- | --- |
| Unity Mono: `UnityPlayer`, `Assembly-CSharp.dll`, `.assets` | Decompile game assemblies; locate state manager, scene transition, or flag routine. |
| Unity IL2CPP: `GameAssembly`, `global-metadata.dat` | Recover class/method metadata, then map only referenced logic and serialized assets. |
| Unreal: `.pak`, `.uasset`, `.umap`, Unreal strings | Inspect package index, Blueprint/game-mode state, and referenced assets. |
| Godot: `.pck`, `project.godot`, GDScript artifacts | Extract the project/scripts and trace scene/state transitions. |
| Custom SDL/GLFW/raylib loop | Slice input, update/tick, win predicate, and output; ignore rendering unless it encodes data. |

The first artifact should be one compact state table containing the win predicate, controlling fields, transition point, and source file/class/function or serialized object.

## State and success tracing

1. Start from flag output, congratulations text, hidden scene load, score gate, server acceptance, or terminal win state.
2. Work backward through `GameManager`/level controller/state arrays, input callbacks, collision events, timers, RNG state, and serialization.
3. Convert positions and visuals into a grid, graph, bitmask, glyph stream, or small state tuple when possible.
4. Preserve exact tick/update order, floating-point precision, clamping, cooldowns, and RNG consumption when simulation matters.
5. If a server is authoritative, model the server predicate and protocol rather than patching client visuals.

Do not manually play or render repeatedly once the decisive state can be generated directly.

## Assets and second channels

- Extract only assets referenced by the success slice; avoid full project dumps.
- In Unity, inspect serialized `GameObject`, `Transform`, names, coordinates, scene references, sprites, and textures. Placement or object names may encode a second channel even when the visible sprite is a decoy.
- For animation or video, preserve raw frames, sample stable state changes, collapse duplicate runs, and independently verify ambiguous glyphs.
- Record raw artifact length and hash before cropping, trimming, color conversion, or repair.

## Saves, replays, and integrity

- Identify JSON/XML/binary/protobuf/custom serialization and the smallest fields controlling level, inventory, score, or flags.
- Trace checksum, CRC, HMAC, duplicate-value, or sequence validation before editing.
- For replays, recover frame/timestamp/input ordering and generate the shortest legal sequence reaching the winning state.
- Prefer a save/replay generator that recalculates integrity fields over a one-off hex edit.
- Use a minimal observation patch only when needed; patched success is not an accepted original solve.

## Completion

Produce one of: a verified save, replay, state/path generator, asset extractor, solver, hook, or intended minimal patch. Verify by loading/running the untouched game or by replaying the exact authoritative predicate. If the required graphics/runtime/server is unavailable, preserve the artifact and state the exact blocker rather than upgrading a supporting check to success.
