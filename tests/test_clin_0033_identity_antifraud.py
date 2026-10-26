"""
Unit Test Suite for CLIN 0033 (WP-7 v2.0): 16-Factor Sovereign Identity, SSN/DOB, Biometric, Credit, Loan, Deed, & ID Access Shield
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

    # 1. Verify 16-Factor Personal, Physical, Biometric, & Asset Identity Matrix (+1 Honeypot = 17 rows)
    test_raw_ssn = "999-00-1234"
    test_raw_dob = "1975-08-15"
    pii = shield.scan_pii_and_biometric_darkweb_feed(raw_ssn=test_raw_ssn, raw_dob=test_raw_dob)
    assert pii["masked_ssn"] == "XXX-XX-1234"
    assert pii["masked_dob"] == "XXXX-XX-15"
    assert pii["core_identifying_features_count"] == 16
    assert pii["attributes_monitored"] == 17
    assert pii["clean_attributes"] == 16
    assert pii["compromised_vectors_quarantined"] == 1

    # 2. Verify 7-Channel Credit Bureau, SBA/Bank Loan, County Deed, ChexSystems/ACH, & SIM-Swap Interceptor
    cred = shield.evaluate_credit_and_loan_activity(credit_freeze_locked=True)
    assert cred["total_inquiries_monitored"] == 7
    assert cred["fraudulent_loans_and_pulls_blocked"] == 6
    assert cred["ceo_authorized_transactions"] == 1

    # 3. Verify Physical ID + 3-Modal Biometric Sign-In, Anti-Replay Fraud Lockout, & Sign-Out
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

    # 4. Export WORM %PDF-1.4 Dossier & Assert Zero Plaintext SSN/DOB Leakage
    artifacts_dir = here / "artifacts"
    exported = shield.generate_wp7_antifraud_dossier(artifacts_dir, raw_ssn=test_raw_ssn, raw_dob=test_raw_dob)
    md_text = pathlib.Path(exported["md_path"]).read_text(encoding="utf-8")
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert test_raw_ssn not in md_text, "CRITICAL: Raw SSN must never appear in Markdown report"
    assert test_raw_dob not in md_text, "CRITICAL: Raw DOB must never appear in Markdown report"
    assert "*--" not in md_text, "CRITICAL: Markdown asterisk collision must never occur"
    assert "MASKED--" not in md_text, "CRITICAL: Double-hyphen mask must never occur"
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"**" not in pdf_bytes, "CRITICAL: Raw Markdown ** must be stripped from PDF text stream"
    assert b"%%EOF" in pdf_bytes

    # 5. Verify WORM SQLite Identity & Credit Ledger Immutability (UPDATE & DELETE must raise IntegrityError)
    import sqlite3
    db_file = artifacts_dir / "wp7_identity_credit_worm_ledger.db"
    assert db_file.exists()
    assert exported["worm_db_stats"]["worm_id_access_rows"] >= 3
    assert exported["worm_db_stats"]["worm_credit_intercept_rows"] >= 7
    conn = sqlite3.connect(str(db_file))
    try:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM worm_id_access_log")
            raise AssertionError("WORM DELETE trigger failed to block deletion!")
        except sqlite3.IntegrityError as exc:
            assert "WORM_IMMUTABILITY_VIOLATION" in str(exc)
        try:
            cur.execute("UPDATE worm_credit_loan_intercept_log SET interception_decision='HACKED'")
            raise AssertionError("WORM UPDATE trigger failed to block modification!")
        except sqlite3.IntegrityError as exc:
            assert "WORM_IMMUTABILITY_VIOLATION" in str(exc)
    finally:
        conn.close()


if __name__ == "__main__":
    run_clin_0033_tests()
    print("[100% PASS] CLIN 0033 (WP-7 v2.0) 16-Factor Identity, Biometric, Credit, Loan, Deed, & ID Access Shield Passed!")
