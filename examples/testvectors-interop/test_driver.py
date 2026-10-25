#!/usr/bin/env python3
"""Regression checks for the local Cedar and signed-receipt example."""

import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

import gdi_driver as gdi

ROOT = Path(__file__).resolve().parents[2]


class DriverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'fixtures', self.root / 'fixtures')
        self.policy = self.root / 'fixtures/policy/autoresearch-safe.cedar'
        self.out = self.root / 'receipts/gdi'
        self.emit()

    def emit(self):
        with contextlib.redirect_stdout(io.StringIO()):
            gdi.emit(self.root)

    def receipts(self):
        return [json.loads(p.read_text()) for p in sorted(self.out.glob('*.json'))]

    def snapshot(self):
        return {p.name: p.read_bytes() for p in self.out.glob('*.json')}

    def test_deterministic_outcomes_signatures_and_result_hash(self):
        before = self.snapshot()
        self.emit()
        self.assertEqual(self.snapshot(), before)
        public = Ed25519PublicKey.from_public_bytes(bytes.fromhex(gdi.PUBKEY_HEX))
        fixtures = sorted((self.root / 'fixtures/inputs').glob('*.json'))
        for path, receipt in zip(fixtures, self.receipts()):
            fixture = json.loads(path.read_text())
            self.assertEqual(receipt['payload']['decision'], fixture['expected_decision'])
            self.assertEqual(receipt['payload']['gdr']['gate_classification'], fixture['expected_gate'])
            self.assertEqual(receipt['payload']['result_hash'],
                             gdi.sha256p(gdi.jcs(receipt['payload']['gdr'])))
            unsigned = copy.deepcopy(receipt)
            signature = bytes.fromhex(unsigned.pop('signature'))
            public.verify(signature, gdi.jcs(unsigned))
            unsigned['payload']['gdr']['confidence_score'] = 0.99
            with self.assertRaises(InvalidSignature):
                public.verify(signature, gdi.jcs(unsigned))

    def test_chain_binds_whole_signed_predecessor_and_omits_genesis_link(self):
        receipts = self.receipts()
        for receipt in receipts:
            for alias in ('parent_receipt_hash', 'prev_hash', 'previous_receipt_hash'):
                self.assertNotIn(alias, receipt)
                self.assertNotIn(alias, receipt['payload'])
        self.assertNotIn('previousReceiptHash', receipts[0]['payload'])
        for previous, current in zip(receipts, receipts[1:]):
            link = current['payload']['previousReceiptHash']
            self.assertEqual(link, gdi.sha256p(gdi.jcs(previous)))
            unsigned = {k: v for k, v in previous.items() if k != 'signature'}
            self.assertNotEqual(link, gdi.sha256p(gdi.jcs(unsigned)))
            changed = dict(previous, signature='00' * 64)
            self.assertNotEqual(link, gdi.sha256p(gdi.jcs(changed)))

    def test_policy_digest_uses_exact_bytes_and_manifest(self):
        # Independently construct this ASCII/integer-free manifest's JCS bytes.
        digest = hashlib.sha256(self.policy.read_bytes()).hexdigest()
        manifest = ('{"construction":"acta-policy-digest-v1","engine":"cedar",'
                    '"files":[{"name":"autoresearch-safe.cedar","sha256":"'
                    + digest + '"}]}').encode()
        expected = 'sha256:' + hashlib.sha256(manifest).hexdigest()
        self.assertEqual({r['payload']['policy_digest'] for r in self.receipts()}, {expected})
        self.policy.write_bytes(self.policy.read_bytes() + b'\n')
        self.emit()
        self.assertNotEqual(self.receipts()[0]['payload']['policy_digest'], expected)

    def test_policy_replacement_changes_decisions(self):
        self.policy.write_text('permit(principal, action, resource);\n')
        self.emit()
        self.assertEqual([r['payload']['decision'] for r in self.receipts()], ['allow'] * 3)

    def test_expected_values_and_policy_label_do_not_drive_evaluation(self):
        before = self.snapshot()
        for path in (self.root / 'fixtures/inputs').glob('*.json'):
            fixture = json.loads(path.read_text())
            fixture.update(expected_decision='wrong', expected_gate='wrong', policy_id='invented')
            path.write_text(json.dumps(fixture))
        self.emit()
        self.assertEqual(self.snapshot(), before)

    def test_cedar_errors_preserve_output(self):
        before = self.snapshot()
        for policy in ('not a Cedar policy',
                       'permit(principal, action, resource) when { context.missing == true };'):
            with self.subTest(policy=policy):
                self.policy.write_text(policy)
                with self.assertRaises((ValueError, RuntimeError)):
                    self.emit()
                self.assertEqual(self.snapshot(), before)

    def test_bad_later_fixture_preserves_output(self):
        before = self.snapshot()
        sorted((self.root / 'fixtures/inputs').glob('*.json'))[-1].write_text('{')
        with self.assertRaises(ValueError):
            self.emit()
        self.assertEqual(self.snapshot(), before)

    def test_empty_fixtures_preserve_output(self):
        before = self.snapshot()
        for path in (self.root / 'fixtures/inputs').glob('*.json'):
            path.unlink()
        with self.assertRaises(ValueError):
            self.emit()
        self.assertEqual(self.snapshot(), before)

    def test_success_removes_stale_receipts(self):
        (self.out / 'stale.json').write_text('{}')
        self.emit()
        self.assertEqual(len(self.receipts()), 3)
        self.assertFalse((self.out / 'stale.json').exists())

    def test_jcs_numbers_and_utf16_key_order(self):
        self.assertEqual(gdi.jcs({'n': [1.0, -0.0, 1e-7]}), b'{"n":[1,0,1e-7]}')
        self.assertEqual(gdi.jcs({'\ue000': 1, '\U00010000': 2}),
                         '{"\U00010000":2,"\ue000":1}'.encode())

    def test_nested_input_changes_signature_and_params_hash(self):
        path = sorted((self.root / 'fixtures/inputs').glob('*.json'))[0]
        before = self.receipts()[0]
        fixture = json.loads(path.read_text())
        fixture['tool_input']['nested'] = {'amount': 10}
        path.write_text(json.dumps(fixture))
        self.emit()
        after = self.receipts()[0]
        self.assertNotEqual(before['signature'], after['signature'])
        self.assertNotEqual(before['payload']['params_hash'], after['payload']['params_hash'])

    def test_sample_matches_deterministic_third_receipt(self):
        sample = ROOT / 'examples/testvectors-interop/sample-receipts/003-deny-bash-destructive.json'
        self.assertEqual(json.loads(sample.read_text()), self.receipts()[2])


if __name__ == '__main__':
    unittest.main(verbosity=2)
