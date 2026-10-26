"""
Unit Test Suite for CLIN 0033 (WP-7 v5.0): 42-Field Atomic Personnel Application, NOK/ICE, Proof-of-Identity Lock, & Credit Shield
"""
import pathlib, sqlite3, sys

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
    assert manifest.version == "6.2.0"
    assert manifest.per_node_annual_gov_usd == 95000
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Verify all 42 Atomic Fields (1 response per box, including NOK and ICE)
    assert len(shield.ATOMIC_42_SCHEMA) == 42
    test_raw_ssn = "999-00-1234"
    test_raw_dob = "1975-08-15"
    pii = shield.scan_pii_and_biometric_darkweb_feed(raw_ssn=test_raw_ssn, raw_dob=test_raw_dob)
    assert pii["masked_ssn"] == "XXX-XX-1234"
    assert pii["masked_dob"] == "XXXX-XX-15"
    assert pii["atomic_fields_count"] == 42
    assert pii["attributes_monitored"] == 43  # 42 Atomic Fields + 1 Dark-Web Canary

    # 2. Verify Employer Proof-of-Identity Lock & Cryptographic Approval Unlock State Machine
    artifacts_dir = here / "artifacts"
    state_file = artifacts_dir / "wp7_personnel_vault_state.json"
    if state_file.exists():
        state_file.unlink()
    state_init = shield.load_or_init_vault_lock_state(artifacts_dir)
    assert state_init["is_locked"] is True

    # Invalid token must be denied
    bad_unlock = shield.request_employer_unlock_for_edit(
        artifacts_dir,
        provided_approval_token="FORGED-BAD-TOKEN",
        change_reason="Attempted unauthorized change",
    )
    assert bad_unlock["unlocked"] is False
    assert shield.load_or_init_vault_lock_state(artifacts_dir)["is_locked"] is True

    # Valid Employer Approval Token must unlock for edit
    cur_rev = int(state_init["revision_number"])
    valid_tok = shield.generate_employer_change_approval_token(cur_rev)
    good_unlock = shield.request_employer_unlock_for_edit(
        artifacts_dir,
        provided_approval_token=valid_tok,
        change_reason="APPROVED_NOK_PHONE_AND_PASSPORT_RENEWAL",
    )
    assert good_unlock["unlocked"] is True
    assert shield.load_or_init_vault_lock_state(artifacts_dir)["is_locked"] is False

    # Sealing the updated 42-field application must re-lock the vault and increment the revision
    updated_prof = dict(shield.DEFAULT_ATOMIC_42_VALUES)
    updated_prof["f28_nok_full_name"] = "MRS. HUMPHREY (PRIMARY NOK VERIFIED)"
    re_sealed = shield.seal_and_lock_personnel_application(
        artifacts_dir,
        profile_42=updated_prof,
        update_reason="APPROVED_NOK_PHONE_AND_PASSPORT_RENEWAL",
    )
    assert re_sealed["locked"] is True
    assert shield.load_or_init_vault_lock_state(artifacts_dir)["is_locked"] is True

    # 3. Verify 7-Channel Credit/Loan Interceptor & Multi-Page PDF Export
    exported = shield.generate_wp7_antifraud_dossier(
        artifacts_dir,
        raw_ssn=test_raw_ssn,
        raw_dob=test_raw_dob,
        profile_42_overrides=updated_prof,
    )
    md_text = pathlib.Path(exported["md_path"]).read_text(encoding="utf-8")
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert test_raw_ssn not in md_text, "CRITICAL: Raw SSN must never appear in Markdown report"
    assert test_raw_dob not in md_text, "CRITICAL: Raw DOB must never appear in Markdown report"
    assert "Next of Kin (NOK)" in md_text
    assert "In Case of Emergency (ICE)" in md_text
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"**" not in pdf_bytes
    assert b"WORM WP-7 16-Factor Identity" in pdf_bytes
    assert b"%%EOF" in pdf_bytes

    # 4. Verify all 3 WORM SQLite tables (6 triggers) reject UPDATE and DELETE
    db_file = artifacts_dir / "wp7_identity_credit_worm_ledger.db"
    conn = sqlite3.connect(str(db_file))
    try:
        cur = conn.cursor()
        for tbl in ("worm_id_access_log", "worm_credit_loan_intercept_log", "worm_identity_profile_revisions", "worm_employer_personnel_notes"):
            try:
                cur.execute(f"DELETE FROM {tbl}")
                raise AssertionError(f"WORM DELETE trigger failed on {tbl}")
            except sqlite3.IntegrityError as exc:
                assert "WORM_IMMUTABILITY_VIOLATION" in str(exc)
    finally:
        conn.close()



    # 5. Verify Stage 13r (v6.0) Zero-Second Emergency Triage & Dual-Compartment Privacy Wall
    roster_keys = list(shield.PERSONNEL_EMERGENCY_ROSTER.keys())
    assert len(roster_keys) >= 4
    ice_card = shield.get_instant_emergency_triage_card(roster_keys[0])
    assert "nok_phone" in ice_card and "ice_phone" in ice_card and "blood_type_clean" in ice_card
    assert ice_card["blood_type_clean"] == "O+ (Positive)"
    assert ice_card["medical_alert_clean"] == "No Known Drug Allergies"

    # Gate must remain locked if User Agreement is not accepted
    locked_gate = shield.open_compartment_gate(
        roster_key=roster_keys[0],
        viewer_role="EMPLOYEE",
        user_agreement_accepted=False,
        access_key_or_pin="EMP-PIN-1AHA8-001",
        out_dir=artifacts_dir,
    )
    assert locked_gate["gate_open"] is False
    assert locked_gate["credit_report"] is None
    assert locked_gate["employer_internal_records"] is None

    # Employee Gate opens Credit/Loan Shield & Proof-of-ID, but BLOCKS Employer Internal Records
    emp_gate = shield.open_compartment_gate(
        roster_key=roster_keys[0],
        viewer_role="EMPLOYEE",
        user_agreement_accepted=True,
        access_key_or_pin="EMP-PIN-1AHA8-001",
        out_dir=artifacts_dir,
    )
    assert emp_gate["gate_open"] is True
    assert emp_gate["credit_report"] is not None
    assert emp_gate["employer_internal_records"] is None, "CRITICAL: Employee must not see Employer Internal HR records"

    # Employer Gate opens Proof-of-ID & Internal HR Records, but BLOCKS Employee Personal Credit/Loans
    empr_gate = shield.open_compartment_gate(
        roster_key=roster_keys[0],
        viewer_role="EMPLOYER",
        user_agreement_accepted=True,
        access_key_or_pin="EMPLOYER-MASTER-1AHA8",
        out_dir=artifacts_dir,
    )
    assert empr_gate["gate_open"] is True
    assert empr_gate["employer_internal_records"] is not None
    assert empr_gate["credit_report"] is None, "CRITICAL: Employer must NEVER see Employee personal credit or loans"


if __name__ == "__main__":
    run_clin_0033_tests()
    print("[100% PASS] CLIN 0033 (WP-7 v5.0) 42-Field Atomic Personnel Onboarding, NOK/ICE, & Employer Lock Vault Passed!")
