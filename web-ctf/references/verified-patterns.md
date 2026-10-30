# Verified Web Patterns

## Parent Authorization Does Not Cover a Private Child

When a public template or document exposes a scheduled/private revision identifier:

1. Trace authorization separately for parent, selected revision, copied document, linked attachment, and export.
2. Test whether a duplicate/copy endpoint accepts an attacker-selected child ID while checking only the public parent.
3. Follow the copied object graph into export and verify that attachment authorization is enforced again.

Automate account creation, duplicate, export, and archive inspection as one chain.

## Proxy Header Trust plus File-Path Reachability

An internal-only route that trusts client-supplied forwarding headers has two boundaries to test:

1. Can an external request influence the address used by the internal-IP check?
2. Does the newly reachable download/log endpoint accept absolute paths or escape its intended root?

Prove both. A header bypass without a sensitive sink is not the complete exploit.

## JSON Query Operators that Execute Strings

When a GraphQL or REST filter is passed into a Mongo-like matcher:

1. Identify the exact library/version and whether operators such as string `$where` are enabled.
2. Confirm whether the operator is compiled with `Function` or an equivalent evaluator.
3. Use the smallest expression that reads the challenge secret and moves it into a returned field.
4. Keep alternate runtime-specific module-loading expressions bounded and stop after one succeeds.

## URL Parser Differential into Header Injection

For a preview/fetch service:

1. Compare how the public validator and downstream fetcher handle backslashes, userinfo, the last `@`, ports, redirects, and normalization.
2. Find a URL accepted as allowlisted by the validator but routed to the intended internal service by the fetcher.
3. Track later decoding into headers. If percent-decoding occurs while constructing a header, encoded CR/LF may terminate the first request and append a second request.
4. Calculate the appended request's body length against the fetcher's unavoidable trailing bytes.
5. Retrieve the result through the application's intended cache or job endpoint and verify the entire chain locally first.

## Framework Role Route into Template and DI

When a framework maps an unauthenticated role to privileged `system` routes:

1. Confirm route middleware and role resolution for the exact installed version.
2. Find a reachable template-rendering method and enumerate its globals/functions.
3. Check whether a template global exposes the dependency-injection container.
4. From the container, select the narrowest service that reaches the secret, such as a PDO/database handle.
5. Reproduce against the supplied application/database containers before the remote request.

Treat authentication bypass, template execution, container access, and database read as separate evidence gates.
