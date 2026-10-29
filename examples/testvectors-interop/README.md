# GDI signed-receipt interoperability example

This local example embeds a compact demonstration GDR profile in the
`decision_receipt` compatibility envelope used by
[ScopeBlind/agent-governance-testvectors](https://github.com/ScopeBlind/agent-governance-testvectors).
It is not the full GDR contract in `schema/gdr.schema.json`, nor a claim of
conformity to the published Acta 2.1 envelope.

The upstream adapter lives in `implementations/gdi/` in that separate repository.
[PR #7](https://github.com/ScopeBlind/agent-governance-testvectors/pull/7) remains
open as checked on 29 October 2026. This example follows the receipt corrections reviewed in
[commit f979177](https://github.com/ScopeBlind/agent-governance-testvectors/commit/f9791775bf13021401b6a5529b96334a58b178be).
The upstream adapter runs four suite fixtures. This repository retains its three
local reproducibility fixtures, fixed timestamps, and session identifiers; its
outputs are not a replacement for the upstream suite's expected chain.

## What this demonstrates

The driver evaluates `fixtures/policy/autoresearch-safe.cedar` with `cedarpy`.
That file preserves the exact policy bytes from upstream commit `f979177`.
Cedar parse or evaluation errors stop the run. Expected outcomes in the input
fixtures are test assertions only and never drive the evaluator.

The embedded profile records a fixture confidence score, gate label, deterministic
explanation, input-field presence, and illustrative accountability roles. Scores
and gate labels come from a fixed lookup table. No confidence threshold is applied;
field presence does not establish evidence completeness, and `human:operator`
does not record a person's approval. No tool executes.

The core GDI gate classifier is separate: it applies institutional routing rules
and confidence thresholds to supplied policy results. Its gate taxonomy and
record-hash contract are unchanged by this receipt adapter.

## Receipt integrity

- Canonicalization uses RFC 8785 (`rfc8785`).
- The Ed25519 signature covers JCS of the envelope without `signature`.
- `payload.result_hash` is `"sha256:"` plus SHA-256 hex of JCS of the compact GDR.
- Genesis omits `payload.previousReceiptHash`. Each subsequent link hashes JCS
  of the whole previous signed receipt, including its signature.
- `payload.policy_digest` uses the `acta-policy-digest-v1` manifest over the exact
  Cedar bytes evaluated, with engine `cedar` and file name `autoresearch-safe.cedar`.

Regenerate local receipts after this correction: the link fields, policy digest,
and explanation bytes change, so signatures and downstream hashes also change.

These are adapter conventions. They do not redefine the core GDR schema or its
hash profile. A signature authenticates bytes under the supplied key; it does not
establish reasoning quality, execution, human oversight, or trustworthy timing.
All signing key material in this example is public test material.

The driver evaluates and signs the entire batch before replacing prior output.
Evaluation or malformed-input failures preserve existing receipts. Filesystem
failures during replacement are not covered by an atomic directory transaction.

## Run and verify

From the repository root, using Python 3.10 or later:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python examples/testvectors-interop/gdi_driver.py
python examples/testvectors-interop/test_driver.py
```

Receipts are written to `receipts/gdi/`. The checked-in
[`003-deny-bash-destructive.json`](sample-receipts/003-deny-bash-destructive.json)
is the deterministic third receipt, including its link to the generated second
receipt. It records Cedar's denial of the destructive Bash fixture; no Bash
command is executed.

With Node/npm available, verify each receipt separately:

```bash
for receipt in receipts/gdi/*.json; do
  npx @veritasacta/verify@0.11.0 "$receipt" \
    --key 4cb5abf6ad79fbf5abbccafcc269d85cd2651ed4b885b5869f241aedf0a5ba29 || exit 1
done
```

The public key is supplied independently of the receipt. Individual signature
verification does not walk the chain; the local regression tests check signed
predecessor linkage. The verifier also accepts `--previous PREVIOUS_RECEIPT` for
checking each non-genesis receipt against its predecessor.

## Validation scope

Local tests cover deterministic outcomes, signatures, GDR digest binding, exact
policy-byte digests, changed policies, Cedar errors, chain scope, JCS edge cases,
nested inputs, failed-batch preservation, stale output, and sample reproduction.
The aggregate repository validator runs them alongside the core classifier,
schema, and citation checks.

External acceptance is tracked in PR #7. Passing local tests does not establish
acceptance by ScopeBlind or deployed governance effectiveness.

The [bilateral pattern](../../docs/bilateral-pattern.md) proposes linking intent
and outcome records. This driver emits one receipt per fixture and does not
implement that execution workflow.

*Apache 2.0. Part of Governed Decision Intelligence.*

## Contribution and review acknowledgment

Mark Julius Banasihan contributed the original upstream driver. ScopeBlind maintainer [@tomjwxf](https://github.com/tomjwxf) reviewed and revised it in [f979177](https://github.com/ScopeBlind/agent-governance-testvectors/commit/f9791775bf13021401b6a5529b96334a58b178be), preserving the four original commits. The [maintainer’s account](https://github.com/ScopeBlind/agent-governance-testvectors/pull/7#issuecomment-6390516611) distinguishes those contributions and reports the upstream checks. See the [dated contribution and review record](../../docs/scopeblind-contribution-review.md). The upstream suite’s four fixtures and this repository’s three local fixtures remain distinct.
