# Validation and Reproducibility

This document defines the checks that support the repository's technical claims. Run them from a clean checkout before a release or research use.

## Environment

- Python 3.10 or later
- dependencies in `requirements-dev.txt`
- a POSIX-compatible shell for the examples
- Node.js only for optional external ACTA verification

## Complete validation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py
```

A successful run ends with `repository validation: PASS`.

## Component checks

### Schema and fixtures

```bash
python scripts/validate_repository.py --only schema
```

This checks JSON Schema validity, populated-example validation with date and time format checking, top-level JSON and YAML contract parity, and negative cases for unknown fields, missing required evidence, conditional approval without conditions, and Gate 4 without escalation.

### Gate classifier

```bash
cd reference-implementation/gate-classifier
python test_gate_classifier.py
```

The suite tests gate routing, rule priority, serialization, event emission, escalation, record writing, and modification detection for sealed fields.

### Interoperability fixtures

```bash
python examples/testvectors-interop/test_driver.py
python examples/testvectors-interop/gdi_driver.py
```

Generated receipts are written to `receipts/gdi/`. Fixtures use fixed timestamps and a public test key so repeated runs produce stable outputs. The key is unsuitable for production. The driver evaluates the bundled Cedar policy; its fixed confidence scores and accountability roles are demonstration data. The compact embedded profile is separate from the full GDR schema.

### Citation metadata

```bash
cffconvert --validate
```

## Optional external ACTA verification

With Node.js available:

```bash
for receipt in receipts/gdi/*.json; do
  npx @veritasacta/verify@0.11.0 "$receipt" \
    --key 4cb5abf6ad79fbf5abbccafcc269d85cd2651ed4b885b5869f241aedf0a5ba29 || exit 1
done
```

Individual verifier calls check signatures; local regression tests check chain linkage. Use `--previous PREVIOUS_RECEIPT` to check a non-genesis receipt against its predecessor with the external verifier.

The submitted external driver is tracked at `ScopeBlind/agent-governance-testvectors#7`. Its status remains under review until the external repository accepts it.

## What the tests establish

| Check | Supported conclusion |
|---|---|
| Schema and example validation | The included record conforms to the included schema |
| JSON and YAML top-level parity | The two representations expose the same top-level contract; deeper equivalence remains a release check |
| Gate-classifier tests | The included rules produce expected outputs for tested cases |
| Hash-integrity tests | Modification to included sealed fields changes the hash |
| Signature verification | The included test key signed the canonical receipt payload |
| Chain verification | Each non-genesis receipt links to JCS of the whole preceding signed receipt |
| CFF validation | Citation metadata follows the declared format |

## What the tests do not establish

The tests do not establish factual accuracy of record contents, model calibration, fair outcomes, reviewer comprehension, legal compliance, security against a compromised runtime, or improved deployment outcomes. Those claims require separate methods and evidence.

## Reproduction report

A reproduction report should include the repository commit SHA, operating system, Python and dependency versions, validation command, result, local changes, generated artifacts, and execution date. Independent reproduction should identify itself as external to the project author.
