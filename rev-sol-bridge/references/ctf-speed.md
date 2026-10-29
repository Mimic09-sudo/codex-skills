# CTF Throughput Mode

Use this for live contests or a folder of multiple reversing challenges. Optimize verified progress across the queue without abandoning a target solely because an estimate or wall-clock threshold expired.

## Lineup Screenshots

When the user asks for a problem lineup, queue, board, or ranking and a CTF page/browser view is available, capture only the screenshots needed to identify the lineup before deep solving:

- challenge list or scoreboard/filter view
- selected challenge detail/prompt
- visible artifact/download area when it helps prove the exact target
- solved/flag/submission evidence when the user explicitly says flags may be included for the lineup/report

Save screenshots under `work/ctf-screenshots/<event-or-date>/` with names like `00-board.png`, `01-<challenge>-prompt.png`, or `01-<challenge>-files.png`. Add the screenshot paths to `work/ctf-board.json` or the final lineup output.

By default, avoid flag and submitted-answer screenshots. If the user explicitly allows flags for a lineup/report, include them when useful. Always avoid session tokens, personal account details, private team chat, and browser UI that is not needed. If the screenshot tool, contest UI, or permission is unavailable, write `screenshots: unavailable (<reason>)` and continue with solving. Spend at most one quick pass on lineup screenshots unless the user explicitly asks for a writeup/report package.

## Queue Formation

Run deterministic folder ranking when applicable:

```text
python <skill-dir>/scripts/queue_triage.py <event-root> --json
```

Treat the ranking as a first-pass estimate, then correct it using observed sinks and runtime/tool availability.

- `green`: supplied source/verifier/solver, high-level script, obvious compare, small clear transform
- `yellow`: bounded VM, packed but dumpable target, moderate obfuscation, stage/asset clue
- `red`: huge corpus without a recovered grammar, heavy anti-debug, giant unknown runtime, weak remote-only signal
- `blocked`: missing artifact/server/tool/account/policy

Solve greens first. Within a class, prefer the task with the clearest path to original verification. Contest points matter only if the user says to optimize score instead of solve count.

## Board

For two or more targets, create `work/ctf-board.json` or `.md`. Keep only:

```json
{
  "event": "",
  "mode": "ctf-sweep",
  "targets": [
    {
      "name": "",
      "path": "",
      "status": "green|yellow|red|solved|parked|blocked",
      "lane": "",
      "decisive_evidence": "",
      "artifact_or_answer": "",
      "verification": "",
      "screenshots": [],
      "next_action": ""
    }
  ]
}
```

Update only on solve, park, blocker, or lane-changing evidence. Do not turn the board into a diary.

## Per-Task Loop

1. Triage and one safe run.
2. Find the success sink or highest-level verifier.
3. Select one lane and one decisive artifact.
4. Build the smallest extractor/model/hook.
5. Verify on the original and stop.

Use evidence gates, not wall-clock budgets:

- triage: one inventory pass plus one safe run
- continue while each deep action produces a new sink, target buffer, trace, model checkpoint, extracted artifact, candidate, failed invariant, or verifier result
- pivot the observation boundary when work repeats without narrowing the model
- park only for a concrete blocker or an explicit queue-priority decision, and retain the cheapest reproducible next action

Hard targets may require many deep actions. Do not demote or park them while evidence is still accumulating.

## Fast Route Bias

When evidence permits, prefer:

1. supplied source, script, verifier, or permitted existing local solver
2. managed/script decompile over native stepping
3. success sink and cross-references over whole disassembly
4. compare/decrypt operand dump over long static reconstruction
5. forward model plus inverse over broad SMT
6. algebra/MITM over path exploration
7. compact bytecode interpreter over repeated native emulation
8. stage/artifact extraction over loader, renderer, or UI analysis

## Reassess or Pivot When

- repeated deep actions yield no decisive evidence or failed invariant
- the same large file or decompiler region is being reread
- symbolic/path exploration grows before the check is sliced
- repeated hook captures are noisy at the same boundary
- original runtime is unavailable and no stronger supporting verifier can be built
- a required remote, file, secret, account, or policy permission is missing

Change the lane or observation boundary first. If the task is concretely blocked or the user wants another queue item prioritized, save one cheapest next action before parking.

## Verification Budget

One strong check is sufficient for speed:

- original target accepts or returns success/flag
- authorized service accepts
- artifact parser/checksum succeeds and the token is unambiguous
- exact forward replay matches the original target when execution is genuinely unavailable

Run a negative test only for ambiguous, patched, cached, or potentially accidental success. Never submit an unverified guess.

## Parallel Work

Default to one agent. Use parallel agents only when the user explicitly asks, and split by independent challenge. Do not run competing strategies on the same target unless the user requests an experiment.

## Output

```text
[challenge] solved: <answer>
verification: <command/result>
files: <paths>
next: <next target or blocker>
```

Skip writeups until all green tasks are solved or the user asks for one.
