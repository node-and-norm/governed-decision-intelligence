# Governed Decision Intelligence (GDI)

[Node & Norm research directory](https://github.com/node-and-norm) · General decision-record architecture and reference implementation.

Repository stewardship moved to Node & Norm on 2026-09-15. Published versions, authorship, and research-status claims retain their existing scope.

## A decision-record specification for AI-assisted and agent-mediated actions

[![CI](https://github.com/node-and-norm/governed-decision-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/node-and-norm/governed-decision-intelligence/actions/workflows/ci.yml)
[![Status: Open Specification](https://img.shields.io/badge/status-open%20specification-5b6cff)](#research-status)
[![Specification](https://img.shields.io/badge/specification-v3.0-blue)](spec/GDI_v3_The_Decision_Architecture_for_Governed_AI.pdf)
[![Schema](https://img.shields.io/badge/GDR%20schema-v2.0-4c8bf5)](schema/gdr.schema.json)
[![Repository release](https://img.shields.io/badge/repository-v2.1.0-6f42c1)](CHANGELOG.md)
[![DEAS](https://img.shields.io/badge/DEAS-v0.2.0%20working-orange)](working-specifications/decision-evidence-applicability-v0.2.md)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20244601-blue)](https://doi.org/10.5281/zenodo.20244601)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--8121--2878-brightgreen)](https://orcid.org/0009-0001-8121-2878)

## Abstract

Governed Decision Intelligence is an open specification and Python reference implementation for recording how a consequential AI-assisted decision was framed, authorized, escalated, and preserved before execution. Its primary artifact is the Governed Decision Record (GDR), a schema-validated record of the decision question, system output, evidence, alternatives, risk posture, authority, gate classification, and downstream obligations.

The repository studies a bounded problem: governance programs often retain policies, model inventories, runtime events, and system logs while leaving the individual institutional decision difficult to reconstruct. GDI tests whether a contemporaneous decision record can make authorization, evidence access, uncertainty, intervention, and escalation inspectable at the point where an AI output may become an institutional action.

A literature search completed in May 2026 did not identify an open specification combining these elements in one decision record. That finding is provisional. The search method, adjacent work, limits, and update conditions are documented in [RESEARCH.md](RESEARCH.md).

## Research question

> Can a schema-validated record make the authority, evidence, uncertainty, alternatives, and intervention conditions of an AI-informed decision reconstructable before the resulting action executes?

GDI approaches this question through artifact construction, schema validation, deterministic classification tests, worked examples, and interoperability experiments. It has not yet been validated through an independent field study.

## Research status

| Component | Version or state | Evidence currently available | Boundary |
|---|---:|---|---|
| Core specification | v3.0 | Published PDF and DOI | Independent peer review remains pending |
| GDR schema contract | v2.0 | Draft 2020-12 JSON Schema and validated example | Schema validity does not establish decision quality |
| Gate classifier | Reference implementation | 114 deterministic internal tests | Test coverage does not establish domain calibration |
| Interoperability driver | External PR under review | Local signed-receipt checks and submitted conformance driver | External conformance has not been accepted |
| Framework mappings | Interpretive analysis | Source-linked evidence mapping | No legal compliance or certification claim |
| Decision Evidence Applicability Specification | v0.2.0 working specification | Revised thesis, determination states, adjacent-system boundary, and acceptance conditions | Schema, authoritative mappings, overlays, cases, and reviews remain in development |
| Field validation | Planned | No deployment study published | External validity remains open |

The status table is authoritative for current maturity claims. The [changelog](CHANGELOG.md) records repository releases. The PDF version, schema contract version, repository release, and working-specification version are separate identifiers.

## Contribution

GDI contributes four connected artifacts:

1. The Governed Decision Record, a machine-readable record of one consequential decision.
2. A gate taxonomy that assigns required deliberation before execution.
3. A confidence-assessment input that can route uncertain decisions toward review or escalation.
4. A reference implementation and interoperability pattern for producing tamper-evident records.

The working [Decision Evidence Applicability Specification](working-specifications/decision-evidence-applicability-v0.2.md) extends this program by asking whether a defined evidence artifact is applicable to a specified governance requirement, what bounded assurance proposition it may support, what additional local evidence is required, where it is insufficient, and where apparent equivalence fails.

DEAS does not claim that governance, controls, findings, evidence, or legal conclusions are portable across regimes.

## What GDI records

| GDR object | Question answered |
|---|---|
| Decision question | What exactly was being decided, within what scope and deadline? |
| AI prediction | Which system output influenced the decision, with what stated confidence and limitations? |
| Options considered | Which alternatives, including delay or inaction, entered the decision? |
| Evidence base | What evidence was available, how complete was it, and when was it verified? |
| Risk posture | Which risks remained, who could accept them, and under what conditions? |
| Decision outcome | Did the institution proceed, proceed conditionally, defer, reject, or escalate? |
| Accountability chain | Which human authority owned the decision, review, escalation, and repair obligations? |
| Data provenance | Which structured and unstructured sources shaped the record? |
| Confidence assessment | How did the stated score compare with the institution's policy threshold? |
| Gate classification | What level of deliberation did institutional policy require? |
| Downstream propagation | Which systems, people, or records must change when the decision changes? |
| Integrity record | Which fields were sealed at classification time, and can later modification be detected? |

The automated actor is identified separately from the human decision authority. A Gate 1 or Gate 2 action may execute under prior human delegation. The GDR still records the human role that authorized the delegation and owns its consequences.

## Architecture

```text
external obligation or institutional policy
                    |
                    v
       runtime policy or control event
                    |
                    v
       gate classification before action
                    |
                    v
        Governed Decision Record (GDR)
                    |
                    v
      execution, escalation, or stopping
                    |
                    v
 monitoring, appeal, repair, and reassessment
```

Runtime governors decide whether an action may proceed under configured policy. GDI records the institutional decision evidence surrounding that control event. Signed-receipt systems may seal the GDR or related events. HIT may assess whether the documented human authority retained practical force. DEAS may evaluate what the resulting evidence can support under a specified governance requirement.

The layers can interoperate without collapsing their claims.

## Adjacent-system boundary

| System | Primary layer | Boundary from GDI and DEAS |
|---|---|---|
| Microsoft Agent Governance Toolkit | Runtime action governance | Evaluates policy, identity, capability, approval, sandbox, allow or deny, and audit events. GDI may record those events but does not replace runtime enforcement. |
| ScopeBlind / Acta | Signed-receipt interoperability | Verifies schema, canonicalization, signatures, attribution, ordering, and chain linkage. GDI can supply payload semantics; DEAS can evaluate assurance use. Neither defines the receipt protocol. |
| Credo AI | Governance platform, policy packs, control mapping, evidence workflows, and runtime governance | GDI does not provide policy packs or compliance automation. DEAS does not provide a universal harmonized-control model. |
| Human Influence Telemetry | Documentary human-influence assessment | HIT evaluates whether formal human authority retained practical force. A complete GDR does not prove that result. |
| DEAS | Evidence-to-requirement qualification | Evaluates applicability, local evidence conditions, sufficiency boundaries, and non-equivalence. It does not make evidence portable. |

See [Related work and scope boundary](docs/related-work.md).

## Quick start

Requirements: Python 3.10 or later.

```bash
git clone https://github.com/node-and-norm/governed-decision-intelligence.git
cd governed-decision-intelligence
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py
```

The validation script checks the JSON Schema, populated GDR example, top-level JSON and YAML schema contract parity, gate-classifier test suite, deterministic interoperability fixtures, signed-receipt integrity, and citation metadata.

A successful run ends with:

```text
repository validation: PASS
```

See [Validation and reproducibility](docs/validation-and-reproducibility.md) for the environment, commands, expected results, and limits of each test.

## Minimal Python example

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path("reference-implementation/gate-classifier").resolve()))

from gate_classifier import GateClassifier

classifier = GateClassifier()
record = classifier.evaluate(
    policy_allowed=True,
    policy_confidence_threshold=0.80,
    agent_id="claims-agent-001",
    tool_name="database_write",
    tool_args={"table": "claims_decisions"},
    confidence_score=0.85,
)

print(record.gate.value)
print(record.record_hash)
print(record.verify_integrity())
```

The reference classifier is an executable research artifact. Institutions must supply domain-specific gate rules, authority boundaries, confidence calibration, and review procedures.

## Evidence and claim discipline

The repository separates demonstrated properties from research hypotheses.

| Claim | Current support | Status |
|---|---|---|
| A populated GDR can be validated against the published schema | Schema validation in CI | Demonstrated for included fixtures |
| Gate classification is deterministic for the included rules | 114 internal tests | Demonstrated for the reference implementation |
| Gate records detect modification to sealed fields | Integrity tests | Demonstrated for the current hash profile |
| GDI receipts can interoperate with the external Acta test-vector suite | Local checks and open external PR | External review pending |
| GDR fields can support evidence requests under NIST, ISO, and EU governance instruments | Source-linked interpretive mapping | Requires implementation and qualified review |
| A GDR preserves substantive human judgment | No field study yet | Unresolved; Human Influence Telemetry addresses this test separately |
| DEAS can determine evidence applicability and non-equivalence across defined requirements | Working specification only | Unresolved until schema, mappings, cases, and review exist |
| GDI improves outcomes in deployed institutions | No comparative deployment data | Unresolved |

Full claim definitions, evidence classes, update conditions, and threats to validity appear in [RESEARCH.md](RESEARCH.md).

## Framework evidence mapping

GDI may produce evidence relevant to governance requirements. The repository does not declare conformity, certification, or legal compliance.

| Source | GDI evidence that may be relevant | Mapping status |
|---|---|---|
| NIST AI Risk Management Framework | Named roles, decision context, risk evidence, monitoring, and escalation records | Interpretive mapping |
| ISO/IEC 42001 | Documented AI-management evidence, risk treatment records, role assignment, and operational records | Interpretive mapping; licensed standard review required |
| European Union Artificial Intelligence Act | Logging, human-oversight, information, and explanation-related records where the relevant provisions apply | Interpretive legal mapping |
| OECD AI Principles | Traceability, accountability roles, transparency, and human intervention records | Principle-level mapping |

See [Framework evidence mapping](docs/framework-compatibility.md). Each mapping records its source, legal or normative force, evidentiary relationship, limitation, and confidence. GDI evidence can support an assessment. The responsible institution and qualified reviewers determine whether the evidence is sufficient.

## Related work and scope boundary

GDI sits beside several established and emerging approaches:

- Governance frameworks define organizational duties and risk-management processes.
- Runtime governance systems enforce permissions, approvals, and action boundaries.
- Cryptographic receipt standards establish integrity, attribution, ordering, and chain linkage.
- Governance platforms translate policy into controls, workflows, and evidence requests.
- GDI defines the decision record and evidence needed to reconstruct institutional authorization.
- Human Influence Telemetry evaluates whether formal human authority retained practical force inside the workflow.
- DEAS evaluates the bounded assurance use of a defined evidence artifact under one specified requirement.

The detailed comparison appears in [Related work](docs/related-work.md).

## Limits

GDI does not establish that a model output is true, a confidence score is calibrated, a reviewer understood the evidence, or a decision was lawful. A hash can detect modification to sealed fields; it cannot establish that the original fields were accurate. A complete record can document ceremonial review as easily as substantive review unless the workflow also measures evidence access, override ability, independent reasoning, and repair authority.

DEAS does not establish evidence portability, legal sufficiency, conformity, certification, or admissibility. Applicability means relevance to a bounded requirement, not proof that the requirement has been satisfied.

The specification also does not solve deceptive alignment, reward hacking, compromised telemetry, collusive agents, or failures that remain invisible to the governance layer. See [Limitations and threats to validity](docs/limitations.md).

## Repository map

```text
governed-decision-intelligence/
├── README.md
├── RESEARCH.md
├── CITATION.cff
├── CHANGELOG.md
├── requirements-dev.txt
├── scripts/
│   └── validate_repository.py
├── spec/
│   ├── GDI_v3_The_Decision_Architecture_for_Governed_AI.pdf
│   └── independent-study/
├── schema/
│   ├── gdr.schema.json
│   ├── gdr.schema.yaml
│   └── gdr.example.json
├── reference-implementation/
│   └── gate-classifier/
├── examples/
│   ├── insurance-claims/
│   └── testvectors-interop/
├── fixtures/
│   └── inputs/
├── docs/
│   ├── framework-compatibility.md
│   ├── related-work.md
│   ├── limitations.md
│   ├── validation-and-reproducibility.md
│   ├── gate-taxonomy.md
│   ├── confidence-threshold-model.md
│   └── bilateral-pattern.md
└── working-specifications/
    ├── decision-evidence-applicability-v0.2.md
    └── decision-evidence-portability-v0.1.md  # deprecated migration pointer
```

## Release and review policy

A numbered release requires:

1. passing repository validation on a clean environment;
2. synchronized JSON and YAML schemas;
3. a changelog entry identifying normative and non-normative changes;
4. updated citation metadata;
5. documented limitations and migration effects;
6. a stable archived release with a DOI;
7. external review for any claim presented as independently validated.

Working specifications remain clearly labeled and are excluded from stable conformance claims until their stated acceptance conditions are met.

## Citation

```bibtex
@software{banasihan2026gdi,
  author  = {Banasihan, Mark Julius},
  title   = {Governed Decision Intelligence: The Decision Architecture for Governed AI},
  year    = {2026},
  version = {3.0},
  doi     = {10.5281/zenodo.20244601},
  url     = {https://doi.org/10.5281/zenodo.20244601},
  license = {Apache-2.0}
}
```

Machine-readable metadata is available in [CITATION.cff](CITATION.cff).

## License and author

Copyright 2026 Mark Julius Banasihan. Licensed under the [Apache License 2.0](LICENSE).

Mark Julius Banasihan is an independent applied researcher working on decision authority, human influence, evaluation, and assurance in AI-mediated institutional systems.

[GitHub](https://github.com/mj3b) | [LinkedIn](https://linkedin.com/in/markjuliusbanasihan) | [ORCID](https://orcid.org/0009-0001-8121-2878)
