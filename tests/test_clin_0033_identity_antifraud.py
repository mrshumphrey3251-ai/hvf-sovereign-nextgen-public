"""
Unit Test Suite for CLIN 0033 (WP-7): Sovereign Anti-Fraud Identity, SSN/DOB, Credit Bureau, & Loan Sentinel
"""
import pathlib, sys

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, SovereignPluginRegistry
from plugins.clin_0033_sovereign_identity_antifraud_shield import SovereignIdentityAntiFraudShield


def run_clin_0033_tests() -> None:
    reg = SovereignPluginRegistry()
    shield = SovereignIdentityAntiFraudShield()
    manifest = reg.register(shield)
    assert manifest.clin_number == "CLIN 0033"
    assert manifest.per_node_annual_gov_usd == 95000
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Verify SSN & DOB Zero-Plaintext Masking & 8-Factor Dark-Web Scan
    test_raw_ssn = "999-00-1234"
    test_raw_dob = "1975-08-15"
    pii = shield.scan_pii_and_biometric_darkweb_feed(raw_ssn=test_raw_ssn, raw_dob=test_raw_dob)
    assert pii["masked_ssn"] == "***-**-1234"
    assert pii["masked_dob"] == "****-**-15"
    assert pii["attributes_monitored"] == 8
    assert pii["clean_attributes"] == 7
    assert pii["compromised_vectors_quarantined"] == 1

    # 2. Verify Credit Bureau, SBA/Bank Loan, & UCC-1 Lien Freeze Interceptor
    cred = shield.evaluate_credit_and_loan_activity(credit_freeze_locked=True)
    assert cred["total_inquiries_monitored"] == 4
    assert cred["fraudulent_loans_and_pulls_blocked"] == 3
    assert cred["ceo_authorized_transactions"] == 1

    # 3. Verify Physical ID Sign-In, Anti-Replay Fraud Lockout, & Sign-Out
    ev_in = shield.record_physical_id_access_event(
        operator_name="JEFFERY HUMPHREY",
        physical_id_serial="OK-REALID-1AHA8-7741",
        raw_ssn=test_raw_ssn,
        raw_dob=test_raw_dob,
        action="SIGN_IN",
        hardware_liveness_nonce="NONCE-001",
    )
    assert ev_in["Access_Decision"] == "AUTHORIZED_SIGN_IN_RECORDED"

    ev_replay = shield.record_physical_id_access_event(
        operator_name="LOAN_FRAUD_IMPOSTOR",
        physical_id_serial="OK-REALID-1AHA8-7741",
        raw_ssn=test_raw_ssn,
        raw_dob=test_raw_dob,
        action="SIGN_IN",
        hardware_liveness_nonce="NONCE-001",
        previous_ledger_hash=ev_in["WORM_Ledger_SHA256"],
    )
    assert ev_replay["Access_Decision"] == "ACCESS_DENIED_FRAUD_INTERLOCK_TRIPPED"

    # 4. Export WORM %PDF-1.4 Dossier & Assert Zero Plaintext SSN Leakage
    artifacts_dir = here / "artifacts"
    exported = shield.generate_wp7_antifraud_dossier(artifacts_dir)
    md_text = pathlib.Path(exported["md_path"]).read_text(encoding="utf-8")
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert test_raw_ssn not in md_text, "CRITICAL: Raw SSN must never appear in Markdown report"
    assert test_raw_dob not in md_text, "CRITICAL: Raw DOB must never appear in Markdown report"
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes


if __name__ == "__main__":
    run_clin_0033_tests()
    print("[100% PASS] CLIN 0033 (WP-7) Identity, SSN/DOB, Credit Bureau, & Loan Fraud Sentinel Test Suite Passed!")
