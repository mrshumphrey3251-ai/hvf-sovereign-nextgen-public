"""
Unit Test Suite for WP-8 (CLIN 0034 v8.0):
Enterprise HR, Front-Screen OSHA Muster, HIPAA Medical/ICE Triage,
Zero-Trust Two-Person Integrity (NIST AC-5) 60-Field Dossier & Promotion Board.
"""
from __future__ import annotations

import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.clin_0034_enterprise_hr_muster_hipaa_promotion_engine import EnterpriseHRMusterHipaaPromotionEngine


def run_clin_0034_hr_tests() -> None:
    hr = EnterpriseHRMusterHipaaPromotionEngine()
    assert hr.clin_number == "CLIN 0034"
    assert hr.version == "8.0.0"
    assert hr.per_node_annual_gov_usd == 85000
    assert len(hr.ATOMIC_60_SCHEMA) == 60
    assert hr.ATOMIC_60_SCHEMA[0][1].startswith("[01] ")
    assert hr.ATOMIC_60_SCHEMA[59][1].startswith("[60] ")

    artifacts_dir = ROOT / "artifacts"
    for fname in ("wp8_hr_dossier_vault_state.json", "wp8_enterprise_hr_triage_worm.db"):
        fpath = artifacts_dir / fname
        if fpath.exists():
            fpath.unlink()

    roster_keys = list(hr.PERSONNEL_EMERGENCY_ROSTER.keys())

    # 1. Verify OSHA Muster SOPs are public on front screen while HIPAA Medical/ICE is None when gate is locked!
    locked_gate = hr.open_hr_and_hipaa_gate(roster_keys[0], False, "EMPLOYER-MASTER-1AHA8", artifacts_dir)
    assert locked_gate["gate_open"] is False
    assert locked_gate["emergency_medical_ice_card"] is None
    assert locked_gate["emergency_procedures_muster"] is not None
    assert len(locked_gate["emergency_procedures_muster"]["muster_dispatch_ledger_rows"]) == 5

    # 2. Verify HR Gate unlocks HIPAA Medical/ICE, Notes, & 60-Field Dossier
    open_gate = hr.open_hr_and_hipaa_gate(roster_keys[0], True, "EMPLOYER-MASTER-1AHA8", artifacts_dir)
    assert open_gate["gate_open"] is True
    assert open_gate["emergency_medical_ice_card"] is not None
    assert len(open_gate["emergency_medical_ice_card"]["hipaa_triage_ledger_rows"]) == 6

    # 3. Verify middle name change in 60-field submission propagates to Promotion Shortlist & HIPAA Triage Card!
    saved_60 = hr.get_saved_user_60field_values(artifacts_dir, roster_keys[0])
    saved_60["f02_middle_name"] = "COMMANDER"
    sub_out = hr.submit_dual_custody_60field_dossier(
        out_dir=artifacts_dir,
        roster_key=roster_keys[0],
        profile_60_inputs=saved_60,
        submitted_by_role="HR:EMP-002 + VERIFIED_BY:EMP-003",
    )
    assert sub_out["submitted"] is True and sub_out["is_locked"] is True

    promo_after = hr.evaluate_promotion_and_company_shortlist(artifacts_dir)
    assert promo_after["top_ranked_candidate"] == "JEFFERY COMMANDER HUMPHREY"
    triage_after = hr.get_instant_emergency_triage_card(roster_keys[0], out_dir=artifacts_dir)
    assert triage_after["full_name"] == "JEFFERY COMMANDER HUMPHREY"

    # 4. Verify sealed dossier blocks edits until unlocked via Two-Person Integrity (HR + Independent Verifier)
    blocked = hr.submit_dual_custody_60field_dossier(
        out_dir=artifacts_dir,
        roster_key=roster_keys[0],
        profile_60_inputs=saved_60,
        enforce_dual_custody_lock=True,
    )
    assert blocked["submitted"] is False

    lock_info = hr.get_employee_dossier_lock_status(artifacts_dir, roster_keys[0])

    # Anti-Self-Approval check (same person for Signer #1 and Signer #2 must fail)
    self_app = hr.request_dual_custody_unlock_for_employee(
        out_dir=artifacts_dir,
        roster_key=roster_keys[0],
        hr_custodian_officer="EMP-002 // CAPT. MARCUS VANCE",
        provided_hr_token=lock_info["hr_custodian_token"],
        second_verifier_officer="EMP-002 // CAPT. MARCUS VANCE",
        provided_verifier_token=lock_info["second_verifier_token"],
        change_reason="SELF_APPROVAL_ATTEMPT",
    )
    assert self_app["unlocked"] is False and "SELF_APPROVAL_PROHIBITED" in self_app["status"]

    # Subject Conflict-of-Interest check (EMP-001 cannot verify EMP-001's own dossier)
    subj_app = hr.request_dual_custody_unlock_for_employee(
        out_dir=artifacts_dir,
        roster_key=roster_keys[0],
        hr_custodian_officer="EMP-002 // CAPT. MARCUS VANCE",
        provided_hr_token=lock_info["hr_custodian_token"],
        second_verifier_officer="EMP-001 // JEFFERY HUMPHREY",
        provided_verifier_token=lock_info["second_verifier_token"],
        change_reason="SUBJECT_SELF_VERIFY_ATTEMPT",
    )
    assert subj_app["unlocked"] is False and "CONFLICT_OF_INTEREST" in subj_app["status"]

    # Valid Two-Person Integrity (HR: EMP-002 + Verifier: EMP-003) unlocks for 1 revision, then re-seals back to SOVEREIGN
    valid_dual = hr.request_dual_custody_unlock_for_employee(
        out_dir=artifacts_dir,
        roster_key=roster_keys[0],
        hr_custodian_officer="EMP-002 // CAPT. MARCUS VANCE",
        provided_hr_token=lock_info["hr_custodian_token"],
        second_verifier_officer="EMP-003 // DR. SARAH LIN",
        provided_verifier_token=lock_info["second_verifier_token"],
        change_reason="DUAL_CUSTODY_VERIFIED_RESTORE",
    )
    assert valid_dual["unlocked"] is True

    saved_60["f02_middle_name"] = "SOVEREIGN"
    re_seal = hr.submit_dual_custody_60field_dossier(
        out_dir=artifacts_dir,
        roster_key=roster_keys[0],
        profile_60_inputs=saved_60,
        submitted_by_role=valid_dual["approved_by"],
        enforce_dual_custody_lock=True,
    )
    assert re_seal["submitted"] is True and hr.get_employee_dossier_lock_status(artifacts_dir, roster_keys[0])["is_locked"] is True

    out = hr.generate_wp8_hr_dossier(artifacts_dir)
    pdf_bytes = pathlib.Path(out["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"CLIN 0034 v8.0" in pdf_bytes

    conn = sqlite3.connect(out["sqlite_db_path"])
    try:
        cur = conn.cursor()
        for tbl, col in (
            ("worm_hr_biometric_access_log", "gate_action"),
            ("worm_hr_dossier_revisions", "update_reason"),
            ("worm_employer_personnel_notes", "confidential_note_text"),
            ("worm_promotion_evaluation_board", "qualification_status"),
            ("worm_hipaa_emergency_triage_log", "access_purpose"),
        ):
            try:
                cur.execute(f"UPDATE {tbl} SET {col} = 'TAMPER'")
                raise AssertionError(f"WORM UPDATE trigger failed on {tbl}")
            except sqlite3.IntegrityError:
                pass
            try:
                cur.execute(f"DELETE FROM {tbl}")
                raise AssertionError(f"WORM DELETE trigger failed on {tbl}")
            except sqlite3.IntegrityError:
                pass
    finally:
        conn.close()

    print("[100% PASS] CLIN 0034 (WP-8 v8.0) Enterprise HR, Front-Screen OSHA Muster, HIPAA Triage, Zero-Trust 2-Person 60-Field Dossier & Promotion Board Passed!")


if __name__ == "__main__":
    run_clin_0034_hr_tests()
