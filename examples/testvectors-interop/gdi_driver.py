#!/usr/bin/env python3
"""GDI conformance driver for agent-governance-testvectors.

Produces v2 structured-envelope receipts with a compact GDR profile embedded in
``payload.gdr``. The receipt is canonicalized with RFC 8785 and signed with
Ed25519. The bundled keypair is a public test fixture and must never be used in
production.
"""

from __future__ import annotations

import base64
import hashlib
import json
import sys
import time
from pathlib import Path

import cedarpy
import rfc8785
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

SEED = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000001")
_PRIV = Ed25519PrivateKey.from_private_bytes(SEED)
_PUB = _PRIV.public_key().public_bytes_raw()
PUBKEY_HEX = _PUB.hex()
_KID = base64.urlsafe_b64encode(hashlib.sha256(_PUB).digest()[:16]).rstrip(b"=").decode()
POLICY_PATH = Path(__file__).resolve().parents[2] / "fixtures/policy/autoresearch-safe.cedar"


def evaluate_cedar(tool_name: str, context: dict, policy: str) -> str:
    """Evaluate the fixture policy; Cedar diagnostics are errors, not denials."""
    result = cedarpy.is_authorized({
        "principal": 'User::"agent"',
        "action": 'Action::' + json.dumps(tool_name, ensure_ascii=False),
        "resource": 'Resource::"tool"',
        "context": context,
    }, policy, [])
    errors = list(getattr(result.diagnostics, "errors", []) or [])
    if errors:
        raise ValueError(f"Cedar evaluation failed for {tool_name}: {errors}")
    return "allow" if str(result.decision).endswith("Allow") else "deny"


GATE_MAP = {
    ("allow", "Read"): ("routine", 0.92),
    ("allow", "Glob"): ("routine", 0.90),
    ("allow", "Grep"): ("routine", 0.90),
    ("allow", "WebSearch"): ("routine", 0.88),
    ("allow", "Bash"): ("elevated_review", 0.78),
    ("allow", "Write"): ("elevated_review", 0.75),
    ("allow", "Edit"): ("elevated_review", 0.75),
    ("deny", "Bash"): ("blocked", 0.15),
    ("deny", "Write"): ("mandatory_escalation", 0.22),
    ("deny", "Edit"): ("mandatory_escalation", 0.22),
}


def build_gdr(tool_name: str, tool_input: dict, context: dict, decision: str,
              policy_id: str, session_id: str, sequence: int, timestamp: str) -> dict:
    """Build the compact GDR profile used by this interoperability test."""
    gate_class, confidence = GATE_MAP.get((decision, tool_name), ("deferred", 0.50))
    evidence_sources = []
    if tool_input:
        evidence_sources.append({
            "completeness": "complete",
            "fields_present": sorted(tool_input.keys()),
            "source": "tool_input",
        })
    if context:
        evidence_sources.append({
            "completeness": "complete",
            "fields_present": sorted(context.keys()),
            "source": "context",
        })

    if decision == "allow":
        decision_sentence = f"Fixture confidence {confidence:.2f}. Policy permits the action."
    else:
        decision_sentence = f"Fixture confidence {confidence:.2f}. Forbid matched or no permit applied. Action blocked."

    return {
        "accountability_chain": [
            {
                "identity": f"session:{session_id}",
                "responsibility": "policy_evaluation",
                "role": "agent_runtime",
            },
            {
                "identity": "human:operator",
                "responsibility": "threshold_and_policy_approval",
                "role": "governance_owner",
            },
        ],
        "confidence_score": confidence,
        "decision": decision,
        "evidence_sources": evidence_sources,
        "gate_classification": gate_class,
        "gdr_timestamp": timestamp,
        "gdr_version": "2.0",
        "policy_id": policy_id,
        "reasoning_reconstruction": (
            f"{tool_name} evaluated against {policy_id}. Gate: {gate_class}. {decision_sentence}"
        ),
        "sequence": sequence,
        "session_id": session_id,
        "tool_input": tool_input,
        "tool_name": tool_name,
    }


def jcs(obj: object) -> bytes:
    """Return RFC 8785 JSON Canonicalization Scheme bytes."""
    return rfc8785.dumps(obj)


def sha256p(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def policy_digest(policy_name: str, policy_bytes: bytes) -> str:
    """Bind the exact evaluated bytes using acta-policy-digest-v1."""
    return sha256p(jcs({
        "construction": "acta-policy-digest-v1",
        "engine": "cedar",
        "files": [{"name": policy_name,
                   "sha256": hashlib.sha256(policy_bytes).hexdigest()}],
    }))


def build_receipt(fixture: dict, sequence: int,
                  previous_canonical: bytes | None,
                  policy_bytes: bytes | None = None) -> tuple[dict, bytes]:
    """Build and sign one deterministic receipt from a fixture."""
    tool_name = fixture["tool_name"]
    tool_input = fixture.get("tool_input", {})
    context = fixture.get("context", {})
    session_id = fixture.get("session_id", "testvectors-session-001")
    policy_id = "autoresearch-safe"
    if policy_bytes is None:
        policy_bytes = POLICY_PATH.read_bytes()
    decision = evaluate_cedar(tool_name, context, policy_bytes.decode("utf-8"))
    timestamp = fixture.get("timestamp") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    gdr = build_gdr(
        tool_name, tool_input, context, decision, policy_id, session_id, sequence, timestamp
    )

    receipt = {
        "algorithm": "ed25519",
        "issued_at": timestamp,
        "issuer": "gdi:governed-decision-intelligence",
        "kid": _KID,
        "payload": {
            "action": {"kind": tool_name, "target": session_id},
            "decision": decision,
            "gdr": gdr,
            "params_hash": sha256p(jcs(tool_input)) if tool_input else None,
            "policy_digest": policy_digest(POLICY_PATH.name, policy_bytes),
            "policy_id": policy_id,
            "reason_code": "policy_match" if decision == "allow" else "policy_deny",
            "result_hash": sha256p(jcs(gdr)),
            "sequence": sequence,
            "session_id": session_id,
            "tier": "evidenced",
            "timestamp": timestamp,
            "tool": tool_name,
            "type": "scopeblind.receipt.v2",
        },
        "pubkey": PUBKEY_HEX,
        "sequence": sequence,
        "type": "decision_receipt",
        "v": 2,
    }

    if previous_canonical is not None:
        receipt["payload"]["previousReceiptHash"] = sha256p(previous_canonical)

    canonical = jcs(receipt)
    receipt["signature"] = _PRIV.sign(canonical).hex()
    # Chain links commit to the entire signed envelope, not the signing input.
    return receipt, jcs(receipt)


def emit(repo_root: Path) -> None:
    """Evaluate and sign the full batch before replacing prior output."""
    fixtures_dir = repo_root / "fixtures" / "inputs"
    fixture_paths = sorted(fixtures_dir.glob("*.json"))
    if not fixture_paths:
        raise ValueError(f"No JSON fixtures found in {fixtures_dir}")
    policy_bytes = (repo_root / "fixtures/policy" / POLICY_PATH.name).read_bytes()
    previous_canonical = None
    pending = []
    for count, fixture_path in enumerate(fixture_paths):
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        sequence = fixture.get("sequence", count + 1)
        receipt, canonical = build_receipt(fixture, sequence, previous_canonical, policy_bytes)
        pending.append((fixture_path.name, json.dumps(receipt, indent=2, sort_keys=True) + "\n"))
        previous_canonical = canonical

    output_dir = repo_root / "receipts" / "gdi"
    output_dir.mkdir(parents=True, exist_ok=True)
    for stale in output_dir.glob("*.json"):
        stale.unlink()
    for name, content in pending:
        (output_dir / name).write_text(content, encoding="utf-8")
    print(f"gdi: {len(pending)} receipts in {output_dir}")


def main() -> int:
    try:
        emit(Path(__file__).resolve().parents[2])
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"gdi: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
