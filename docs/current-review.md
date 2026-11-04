# Review guide: Governed Decision Intelligence

This guide separates research claims, executable artifacts and historical publication identities. The underlying research record is preserved. [Claim register](../RESEARCH.md), [prior entry](../README-2026-11-03.md).

## Start with the research question

GDI asks whether a record can preserve the authority, evidence and intervention conditions needed to reconstruct an AI-informed decision. Review the [bounded research account](research-summary.md), then compare the [full record schema](../schema/gdr.schema.json), [classifier](../reference-implementation/gate-classifier/gate_classifier.py) and [compact receipt profile](../examples/testvectors-interop/README.md). Each artifact makes a different contribution.

## Versions and publication

| Artifact | Recorded identity | Review boundary |
| :--- | :--- | :--- |
| Cited work | Version 3.0, April 1, 2026, DOI 10.5281/zenodo.20244601. [CFF](../CITATION.cff) | Citation metadata stays unchanged. Record a commit for later development. |
| Core specification | GDI v3 PDF. [Preserved PDF](../spec/GDI_v3_The_Decision_Architecture_for_Governed_AI.pdf) | Read its claims beside the current research limits. |
| Prior README | Repository badge v2.1.0. [Archived entry](../README-2026-11-03.md) | This label differs from the cited work's version. |
| Record schema | The `gdr_version` field accepts 2.0. [JSON](../schema/gdr.schema.json) · [YAML](../schema/gdr.schema.yaml) | Schema identity has a separate scope from the PDF and citation. |
| Applicability proposal | DEAS 0.2.0. [Working specification](../working-specifications/decision-evidence-applicability-v0.2.md) | Working material requires separate validation. |

The repository's version labels describe different artifacts. This guide preserves each recorded identity. [Change history](../CHANGELOG.md).

## Known limits

### Classification and enforcement

The classifier returns a record and review flags. A record writer is optional. The `GATE_RECORD_WRITTEN` event can be emitted without a writer, so that event alone supplies no storage acknowledgement. The host owns persistence, review and execution. [API implementation](../reference-implementation/gate-classifier/gate_classifier.py).

The threshold guide gives a GREEN floor of 0.80. The classifier's default review threshold is 0.70. Its `policy_confidence_threshold` input is recorded but does not control `_classify`. Reviewers must retain this discrepancy when interpreting the examples. [Threshold model](confidence-threshold-model.md), [classifier rules](../reference-implementation/gate-classifier/gate_classifier.py).

### Record integrity and schema checks

The local `GateRecord` hash covers seven fields: record ID, agent ID, tool name, tool arguments, policy permission, gate and classification timestamp. Other recorded fields fall outside that hash. The compact receipt example uses a separate signature and canonicalization contract. [Hash implementation](../reference-implementation/gate-classifier/gate_classifier.py), [receipt profile](../examples/testvectors-interop/README.md).

The test named for gate tampering reassigns a routine gate and includes an alternative assertion that permits that value. Its pass alone cannot demonstrate detection of a changed gate. [Existing test](../reference-implementation/gate-classifier/test_gate_classifier.py).

The schema's conditional-approval branch constrains a present `conditions` array, while leaving that property's presence unenforced in the branch. The repository validator tests an empty array. It also compares top-level JSON/YAML keys rather than complete semantic equivalence. [Schema](../schema/gdr.schema.json), [validator](../scripts/validate_repository.py).

### Evidence and external review

The supplied fixtures support bounded software checks. Model calibration, truthful records, reviewer comprehension, legal applicability and institutional effectiveness require other evidence. [Limits](limitations.md), [claim register](../RESEARCH.md).

The ScopeBlind contribution record is dated October 29, 2026. It identifies original contributions, maintainer corrections and reported checks. Its recorded open status and reported results retain their dates and revisions. The present documentation work performs no new upstream-status assessment. [Dated review record](scopeblind-contribution-review.md).

The independent-study directory contains an incomplete scaffold. Use the current research account and claim register as the review entry points. The scaffold's pending DOI and unfinished links retain their historical status. [Study index](../spec/independent-study/docs/index.md), [research account](research-summary.md).

## Review and disclosure

Read the [project AI-use disclosure](ai-use-disclosure.md) alongside the technical records. It preserves the distinction between author-reported review, AI-assisted preparation and external technical review. A complete retrospective human-check inventory remains unavailable. Research validity and effective control remain open to independent assessment. [Known limits](limitations.md).
