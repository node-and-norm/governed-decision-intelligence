# The Bilateral Pattern

Single-receipt architectures answer one question. The bilateral pattern answers two.

A post-execution receipt can authenticate a recorded outcome under a supplied key.
A pre-execution receipt can authenticate a recorded intent. Neither establishes
that the contents are true, the reasoning was sound, or execution matched policy.

The proposed bilateral pattern links those two records so reviewers can compare
intent and outcome. A hash link establishes a commitment to the predecessor's
bytes. Trusted execution evidence, timing, and logging controls are separately
needed to establish that intent was recorded before the action occurred.
This workflow is not implemented by the current interoperability driver.

```
Receipt 1: sha256(JCS(GDR))        ← sealed before execution
     │
     │  previousReceiptHash
     ▼
Receipt 2: sha256(JCS(result))     ← sealed after execution
```

---

## When to Use It

The bilateral pattern applies when all three conditions hold:

1. The deployment is in a regulated vertical (pharmaceuticals, financial services, telecom, healthcare, insurance) where regulators distinguish intent from outcome in audit proceedings.
2. The agent has authority to execute consequential actions autonomously (Gate 2 or Gate 3 decisions).
3. A third party — regulator, counterparty, auditor — needs to verify both sides independently without trusting the operator's infrastructure.

Whether a single receipt is sufficient depends on the deployment evidence requirements. For Gate 4 escalations, execution halts before a second receipt is needed. The bilateral pattern applies most directly to Gate 2 and Gate 3.

---

## How It Composes with the GDR

The GDR is the payload of Receipt 1. It carries pre-decision reasoning state: confidence score, gate classification, evidence completeness, accountability chain, and reasoning reconstruction.

```json
{
  "receipt_1_payload": {
    "result_hash": "sha256(JCS(GDR))",
    "gdr": {
      "gate_classification": "elevated_review",
      "confidence_score": 0.85,
      "reasoning_reconstruction": "...",
      "accountability_chain": []
    },
    "signed": "before execution"
  }
}
```

Receipt 2 carries the execution result: what the tool returned, whether it matched the authorized scope, and any deviation from the pre-execution intent.

```json
{
  "receipt_2_payload": {
    "result_hash": "sha256(JCS(execution_result))",
    "previousReceiptHash": "sha256(JCS(Receipt_1))",
    "execution_matched_intent": true,
    "signed": "after execution"
  }
}
```

The link detects changes to the referenced signed receipt. A signer can construct both receipts later with arbitrary timestamps; the chain alone cannot rule out backdating.

---

## Implementation sketch

The following is conceptual pseudocode, not an API implemented by the local driver.
For the ScopeBlind compatibility envelope, the link is `payload.previousReceiptHash`;
genesis omits it and each later link hashes the whole signed predecessor.

```python
# Pre-execution: seal the GDR into Receipt 1
gdr = build_gdr(tool_name, tool_input, context, decision, policy_id)
receipt_1 = build_receipt(gdr_payload=gdr, prev_hash=None)
receipt_1["signature"] = private_key.sign(jcs(receipt_1)).hex()
receipt_1_canonical = jcs(receipt_1)  # signature included in the chain target
write_to_log(receipt_1)

# Execute the action
result = execute_tool(tool_name, tool_input)

# Post-execution: seal the result into Receipt 2, chained to Receipt 1
receipt_2 = build_receipt(
    result_payload=result,
    prev_hash="sha256:" + sha256(receipt_1_canonical).hexdigest(),
)
receipt_2_canonical = jcs(receipt_2)
receipt_2["signature"] = private_key.sign(receipt_2_canonical).hex()
write_to_log(receipt_2)
```

A concrete implementation must construct valid envelopes, verify each signature with a trusted key, and check each `payload.previousReceiptHash` against the whole signed predecessor. The sketch itself is not a conformance result.

---

## Evidence use

Linked intent and outcome records may support a governance review. They do not
establish that human oversight occurred, controls operated effectively, or a legal
requirement was satisfied. See [Framework evidence mapping](framework-compatibility.md)
for the repository's interpretive mappings and their limits.

---

## Relationship to the Veritas Acta v1.1 Spec

The v1.1 spec introduces a `references` array that makes bilateral composition explicit:

```json
{
  "references": [
    {
      "receipt_id": "rcpt-pre-execution",
      "relationship": "pre_execution_intent"
    }
  ]
}
```

See [VeritasActa/verify#1](https://github.com/VeritasActa/verify/issues/1) and [VeritasActa/verify#8](https://github.com/VeritasActa/verify/issues/8) for the v1.1 deliverables. GDI's pre-execution GDR is the natural payload for the `pre_execution_intent` reference type, and the bilateral pattern is designed to compose with the v1.1 `references` array.

---

*Part of the Governed Decision Intelligence (GDI) specification. Apache 2.0.*
*[https://github.com/mj3b/governed-decision-intelligence](https://github.com/mj3b/governed-decision-intelligence)*
