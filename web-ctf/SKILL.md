---
name: web-ctf
description: Solve authorized web CTF challenges from supplied source or explicit challenge endpoints by tracing trust and parser boundaries, reproducing the chain locally, automating the minimal request sequence, and verifying the real target. Use for authorization gaps, SSRF/parser differentials, request smuggling, query-language injection, template injection, and framework role flaws.
---

# Web CTF

## Scope

Operate only on source, containers, and endpoints explicitly supplied as CTF targets. Tool availability and a discovered internal hostname do not authorize unrelated scanning.

Load `ctf-wsl-toolchain` for local containers and request tooling. Bind reproduced services to loopback and use unmistakable local sentinel secrets.

## Solve Loop

1. Inventory routes, middleware order, authentication roles, object ownership, parser/decoder stages, internal services, and secret placement.
2. Draw a boundary table: attacker-controlled field, validator interpretation, downstream interpretation, authorization check, and reachable sink.
3. Prefer a source-defined exploit chain over broad fuzzing. Prove each transition with one minimal request.
4. Reproduce the chain locally against the untouched application or supplied containers.
5. Save a standalone solver with bounded timeouts, explicit expected status codes, and flag/success extraction.
6. Apply the same chain to the authorized endpoint and stop after original verification.

Read [verified patterns](references/verified-patterns.md) when evidence matches an authorization graph gap, proxy-header trust, query operator execution, URL parser differential, header decoding, framework role bypass, or template-to-DI chain.

## Correctness

- Test authorization on the exact child object, revision, attachment, or export graph being accessed.
- Model every parser separately; URL validators, fetchers, proxies, and HTTP servers may disagree.
- Track each decoding pass and the context it enters. Percent-decoded CR/LF inside a header is materially different from decoding only the request path.
- Treat JSON query DSLs and template globals as code-capability surfaces when they reach evaluators, modules, containers, or database handles.
- Verify local and remote behavior with the same solver. A local sentinel is not the contest flag.
