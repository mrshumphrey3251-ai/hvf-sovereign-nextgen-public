"""
Unit Test Suite for CLIN 0033 (WP-7 v7.0): 60-Field Atomic Personnel Dossier (Addresses, Job History, Training),
Zero-Second Emergency ICE Triage, Dual-Compartment Privacy Wall, Employer Notes, & Promotion Shortlist Engine
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
    assert manifest.version == "7.0.0"
    assert manifest.per_node_annual_gov_usd == 95000
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Verify all 60 Atomic Fields (1 response per box: Legal, Contact, Job/I-9, NOK/ICE, Biometrics, Addresses, Prior Jobs, Training)
    assert len(shield.ATOMIC_42_SCHEMA) == 60
    test_raw_ssn = "999-00-1234"
    test_raw_dob = "1975-08-15"
    pii = shield.scan_pii_and_biometric_darkweb_feed(raw_ssn=test_raw_ssn, raw_dob=test_raw_dob)
    assert pii["masked_ssn"] == "XXX-XX-1234"
    assert pii["masked_dob"] == "XXXX-XX-15"
    assert pii["atomic_fields_count"] == 60
    assert pii["attributes_monitored"] == 61  # 60 Atomic Fields + 1 Dark-Web Canary

    # 2. Verify Employer Proof-of-Identity Lock & Cryptographic Approval Unlock State Machine
    artifacts_dir = here / "artifacts"
    state_file = artifacts_dir / "wp7_personnel_vault_state.json"
    if state_file.exists():
        state_file.unlink()
    state_init = shield.load_or_init_vault_lock_state(artifacts_dir)
    assert state_init["is_locked"] is True

    bad_unlock = shield.request_employer_unlock_for_edit(
        artifacts_dir,
        provided_approval_token="FORGED-BAD-TOKEN",
        change_reason="Attempted unauthorized change",
    )
    assert bad_unlock["unlocked"] is False
    assert shield.load_or_init_vault_lock_state(artifacts_dir)["is_locked"] is True

    cur_rev = int(state_init["revision_number"])
    valid_tok = shield.generate_employer_change_approval_token(cur_rev)
    good_unlock = shield.request_employer_unlock_for_edit(
        artifacts_dir,
        provided_approval_token=valid_tok,
        change_reason="APPROVED_NOK_PHONE_AND_PASSPORT_RENEWAL",
    )
    assert good_unlock["unlocked"] is True
    assert shield.load_or_init_vault_lock_state(artifacts_dir)["is_locked"] is False

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

    # 4. Verify Stage 13w (v7.0) Promotion & Evaluation Shortlist Engine (Populates 5th WORM Table)
    promo_all = shield.evaluate_promotion_and_company_shortlist(
        out_dir=artifacts_dir,
        min_experience_years=5,
        min_academy_score_pct=90.0,
        min_eval_rating=4.5,
        required_specialty="ALL",
    )
    assert promo_all["total_personnel_evaluated"] == 4
    assert promo_all["qualified_candidates_count"] == 4
    assert promo_all["top_ranked_candidate"] == "JEFFERY SOVEREIGN HUMPHREY"
    assert promo_all["qualified_shortlist_rows"][0]["Shortlist_Rank"] == "RANK #01"

    promo_sic = shield.evaluate_promotion_and_company_shortlist(
        out_dir=artifacts_dir,
        min_experience_years=9,
        min_academy_score_pct=97.0,
        min_eval_rating=4.9,
        required_specialty="SIC_HARDWARE",
    )
    assert promo_sic["qualified_candidates_count"] == 2

    # 5. Verify Zero-Second Emergency ICE Triage, Dual-Compartment Privacy Wall, & Employer Notes
    db_file = artifacts_dir / "wp7_identity_credit_worm_ledger.db"
    roster_keys = list(shield.PERSONNEL_EMERGENCY_ROSTER.keys())
    assert len(roster_keys) >= 4
    ice_card = shield.get_instant_emergency_triage_card(roster_keys[0])
    assert ice_card["blood_type_clean"] == "O+ (Positive)"
    assert ice_card["medical_alert_clean"] == "No Known Drug Allergies"

    locked_gate = shield.open_compartment_gate(
        roster_key=roster_keys[0],
        viewer_role="EMPLOYEE",
        user_agreement_accepted=False,
        access_key_or_pin="EMP-PIN-1AHA8-001",
        out_dir=artifacts_dir,
    )
    assert locked_gate["gate_open"] is False

    for rk in roster_keys:
        p_pin = shield.PERSONNEL_EMERGENCY_ROSTER[rk]["employee_pin"]
        g_emp = shield.open_compartment_gate(rk, "EMPLOYEE", True, p_pin, artifacts_dir)
        assert g_emp["gate_open"] is True and g_emp["credit_report"] is not None and g_emp["employer_personnel_notes"] is None
        g_empr = shield.open_compartment_gate(rk, "EMPLOYER", True, "EMPLOYER-MASTER-1AHA8", artifacts_dir)
        assert g_empr["gate_open"] is True and g_empr["credit_report"] is None and g_empr["employer_personnel_notes"] is not None

    added_note = shield.append_employer_personnel_note(
        db_path=db_file,
        employee_id="EMP-001",
        employee_name="JEFFERY SOVEREIGN HUMPHREY",
        author_authority="JEFFERY HUMPHREY (CEO)",
        note_category="EXECUTIVE_AUDIT_MEMO",
        confidential_note_text="Sealed Stage 13w Employer Note Verification Test.",
    )
    assert added_note["total_notes_for_employee"] >= 2

    # 6. Verify all 5 WORM SQLite tables (10 triggers) reject UPDATE and DELETE with clean rollback
    conn = sqlite3.connect(str(db_file), timeout=30.0)
    try:
        cur = conn.cursor()
        for tbl in (
            "worm_id_access_log",
            "worm_credit_loan_intercept_log",
            "worm_identity_profile_revisions",
            "worm_employer_personnel_notes",
            "worm_promotion_evaluation_board",
        ):
            try:
                cur.execute(f"DELETE FROM {tbl}")
                raise AssertionError(f"WORM DELETE trigger failed on {tbl}")
            except sqlite3.IntegrityError as exc:
                conn.rollback()
                assert "WORM_IMMUTABILITY_VIOLATION" in str(exc)
    finally:
        conn.close()


if __name__ == "__main__":
    run_clin_0033_tests()
    print("[100% PASS] CLIN 0033 (WP-7 v7.0) 60-Field Dossier, Promotion Shortlist Engine, & 5-Table WORM Vault Passed!")
