"""
Unit Test Suite for CLIN 0033 (WP-7 v4.0): Full-Page 16-Factor Sovereign Identity, Profile Revision Updater, Credit, Loan, Deed, & ID Access Shield
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
    assert manifest.version == "4.0.0"
    assert manifest.per_node_annual_gov_usd == 95000
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Verify all 16 Identifying Features can be customized and scanned
    test_raw_ssn = "999-00-1234"
    test_raw_dob = "1975-08-15"
    pii = shield.scan_pii_and_biometric_darkweb_feed(
        raw_ssn=test_raw_ssn,
        raw_dob=test_raw_dob,
        pob_and_maiden_kba="TULSA-OK-MAIDEN-VAULT-77",
        physical_id_number="OK-DL-99887766",
        passport_number="US-PASS-11223344",
        dod_cac_piv_serial="CAC-EDIPI-5566778899",
        physical_smt_features="EYES:BRN|HGT:72IN|SMT:SCAR-LEFT-THUMB",
        fingerprint_minutiae="FINGER-MINUTIAE-V4",
        iris_vascular_hash="IRIS-VASCULAR-V4",
        face_voice_liveness="3DFACE-VOICE-V4",
        home_deed_parcel_apn="APN-OK-990011",
        bank_ach_aba_routing="ABA-103000648-LOCK",
        mobile_sim_imei_lock="IMEI-998877-SIMLOCK",
        medical_npi_beneficiary="MED-ID-445566",
        vehicle_fleet_vin="1HVF2026SOVEREIGN",
        corporate_ein_uei="UEI:S1M4ENLHTDH5|CAGE:1AHA8",
    )
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

    # 3. Export WORM %PDF-1.4 Dossier & Verify Versioned Profile Revision Chaining (Rev #1 -> Rev #2)
    artifacts_dir = here / "artifacts"
    exported1 = shield.generate_wp7_antifraud_dossier(
        artifacts_dir,
        raw_ssn=test_raw_ssn,
        raw_dob=test_raw_dob,
        vehicle_fleet_vin="1HVF2026CHASSIS01",
        update_reason="INITIAL_16FACTOR_ENROLLMENT",
    )
    exported2 = shield.generate_wp7_antifraud_dossier(
        artifacts_dir,
        raw_ssn=test_raw_ssn,
        raw_dob=test_raw_dob,
        vehicle_fleet_vin="1HVF2027CHASSIS02",
        update_reason="UPDATED_FLEET_VIN_AND_PASSPORT",
    )
    assert exported2["worm_db_stats"]["worm_profile_revision_rows"] >= 2
    assert len(exported2["revision_history"]) >= 2

    md_text = pathlib.Path(exported2["md_path"]).read_text(encoding="utf-8")
    pdf_bytes = pathlib.Path(exported2["pdf_path"]).read_bytes()
    assert test_raw_ssn not in md_text, "CRITICAL: Raw SSN must never appear in Markdown report"
    assert test_raw_dob not in md_text, "CRITICAL: Raw DOB must never appear in Markdown report"
    assert "*--" not in md_text, "CRITICAL: Markdown asterisk collision must never occur"
    assert "MASKED--" not in md_text, "CRITICAL: Double-hyphen mask must never occur"
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"**" not in pdf_bytes
    assert b"Event #3" in pdf_bytes
    assert b"WORM WP-7 16-Factor Identity" in pdf_bytes
    assert b"%%EOF" in pdf_bytes

    # 4. Verify all 3 WORM SQLite tables (6 triggers) reject UPDATE and DELETE
    db_file = artifacts_dir / "wp7_identity_credit_worm_ledger.db"
    conn = sqlite3.connect(str(db_file))
    try:
        cur = conn.cursor()
        for tbl in ("worm_id_access_log", "worm_credit_loan_intercept_log", "worm_identity_profile_revisions"):
            try:
                cur.execute(f"DELETE FROM {tbl}")
                raise AssertionError(f"WORM DELETE trigger failed on {tbl}")
            except sqlite3.IntegrityError as exc:
                assert "WORM_IMMUTABILITY_VIOLATION" in str(exc)
    finally:
        conn.close()


if __name__ == "__main__":
    run_clin_0033_tests()
    print("[100% PASS] CLIN 0033 (WP-7 v4.0) Full-Page 16-Factor Identity & WORM Profile Revision Updater Passed!")
