"""
Unit Test Suite for WP-7 (CLIN 0033 v8.0):
Standalone Personal Sovereign Identity, 7-Channel Credit/Loan/Deed/SIM Anti-Fraud Shield & B2C Engine.
"""
from __future__ import annotations

import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.clin_0033_sovereign_identity_antifraud_shield import SovereignIdentityAntiFraudShield


def run_clin_0033_tests() -> None:
    shield = SovereignIdentityAntiFraudShield()
                
    # Verify B2C & Enterprise revenue calculator
    rev = shield.calculate_b2c_and_enterprise_revenue(500, 120, 40, 2)
    assert rev["b2c_direct_total_arr_usd"] == (500 * 350) + (120 * 1250) + (40 * 2500)
    assert rev["enterprise_nodes_arr_usd"] == 130000.0
    assert rev["combined_wp7_annual_revenue_usd"] == 555000.0

    # Verify 18-field personal vault & 0% Employer HR visibility
    pv = shield.evaluate_personal_18_vault()
    assert pv["total_personal_fields_locked"] == 18
    assert all(r["Employer_HR_Visibility"].startswith("0%") for r in pv["attribute_rows"])

    # Verify 7-channel credit/loan/deed/SIM-swap intercept
    cred = shield.evaluate_credit_and_loan_activity(credit_freeze_locked=True)
    assert cred["total_inquiries_monitored"] == 7
    assert cred["fraudulent_loans_and_pulls_blocked"] == 6
    assert cred["authorized_inquiries_approved"] == 1

    # Verify personal subscriber gate lock & unlock
    artifacts_dir = ROOT / "artifacts"
    sub_key = list(shield.PERSONAL_SUBSCRIBER_PROFILES.keys())[0]
    locked = shield.open_personal_subscriber_gate(sub_key, False, "PERSONAL-PIN-1AHA8-001", artifacts_dir)
    assert locked["gate_open"] is False and locked["credit_report"] is None

    opened = shield.open_personal_subscriber_gate(sub_key, True, "PERSONAL-PIN-1AHA8-001", artifacts_dir)
    assert opened["gate_open"] is True and opened["credit_report"] is not None

    # Verify saving personal 18 fields & WORM SQLite triggers (3 tables / 6 triggers)
    custom_18 = dict(opened["current_18_values"])
    custom_18["p02_middle_name"] = "SOVEREIGN"
    saved_res = shield.save_personal_subscriber_18_fields(artifacts_dir, sub_key, custom_18)
    assert saved_res["saved"] is True

    out = shield.generate_wp7_antifraud_dossier(artifacts_dir)
    pdf_bytes = pathlib.Path(out["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"CLIN 0033 v8.0" in pdf_bytes

    conn = sqlite3.connect(out["sqlite_db_path"])
    try:
        cur = conn.cursor()
        for tbl, col in (
            ("worm_personal_credit_intercept_log", "intercept_action"),
            ("worm_personal_vault_revisions", "update_reason"),
            ("worm_personal_unfreeze_tokens", "unfreeze_token"),
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

    print("[100% PASS] CLIN 0033 (WP-7 v8.0) Standalone Personal Credit/Loan/Deed/SIM Shield & B2C Revenue Engine Passed!")


if __name__ == "__main__":
    run_clin_0033_tests()
