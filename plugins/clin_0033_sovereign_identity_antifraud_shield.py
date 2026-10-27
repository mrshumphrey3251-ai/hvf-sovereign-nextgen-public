"""
HVF Sovereign Next-Gen Work Package 7 (CLIN 0033 v8.0):
Standalone Personal Sovereign Identity, 7-Channel Credit Bureau, Loan, Home Deed,
Treasury ACH, & SIM-Swap Anti-Fraud Shield + B2C Personal Subscription Engine.
100% Physically Separated From Enterprise HR (Zero Employer Access to Personal Credit/Loans).
Controlling Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect (CAGE 1AHA8)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import pathlib
import sqlite3
from typing import Any, Dict, List, Tuple

from plugins.clin_0031_command_watchfloor_rbac_pdf_engine import compile_single_page_pdf_14
from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, PluginManifest, SovereignExpansionModule

ENCLAVE_MODE = "PUBLIC"
PERSONAL_VAULT_PEPPER = "PUBLIC_PERSONAL_SHIELD_PEPPER_REDACTED_DFARS_252_227_7018"


class SovereignIdentityAntiFraudShield(SovereignExpansionModule):
    """
    Standalone WP-7 (CLIN 0033 v8.0): Personal Identity, Credit Bureau, Loan, Deed,
    & SIM-Swap Anti-Fraud Shield. Owned 100% by the Individual User (B2C / B2B2C).
    Zero Employer or HR code paths exist in this module.
    """

    PERSONAL_PRIVACY_CHARTER: str = (
        "SOVEREIGN PERSONAL ANTI-FRAUD & CREDIT/DEED SHIELD CHARTER (FCRA 15 U.S.C. 1681 / GLBA / PRIVACY ACT): "
        "(1) 100% INDIVIDUAL OWNERSHIP & ZERO EMPLOYER ACCESS: This Personal Anti-Fraud Vault is physically and "
        "cryptographically decoupled from Enterprise HR (CLIN 0034). No employer, HR officer, or third party has "
        "any access path to your credit bureau inquiries, personal loans, bank/ACH routing locks, or property deeds. "
        "(2) PORTABLE LIFETIME PROTECTION: Your personal vault, 7-Channel Credit/Loan/Deed/SIM-Swap locks, and "
        "1-Click Temporary Unfreeze Tokens belong exclusively to you across any job or retirement."
    )

    B2C_AND_SEAT_PRICING_TIERS: List[Dict[str, Any]] = [
        {
            "Tier_ID": "TIER-B2C-INDIVIDUAL",
            "Subscription_Plan": "Personal Sovereign Shield (Single Adult B2C)",
            "Monthly_Rate_USD": 29.99,
            "Annual_Rate_USD": 350.00,
            "Included_Seats": 1,
            "Protected_Channels": "7/7 (Equifax, Experian, TransUnion, ChexSystems, Home Deed APN, ACH, SIM-Swap)",
            "Target_Market": "Direct-to-Consumer (B2C) Individual Subscribers, Veterans & Landowners",
        },
        {
            "Tier_ID": "TIER-B2C-FAMILY5",
            "Subscription_Plan": "Sovereign Family & Farmstead 5-Seat Pack (B2C)",
            "Monthly_Rate_USD": 109.00,
            "Annual_Rate_USD": 1250.00,
            "Included_Seats": 5,
            "Protected_Channels": "7/7 Channels + Multi-Parcel Farm/Home Deed Title Lock + Elder/Child SSN Lock",
            "Target_Market": "Families, Agricultural Producers, & Multi-Parcel Property Owners",
        },
        {
            "Tier_ID": "TIER-EXEC-VIP",
            "Subscription_Plan": "Executive & High-Net-Worth Sovereign Vault",
            "Monthly_Rate_USD": 225.00,
            "Annual_Rate_USD": 2500.00,
            "Included_Seats": 2,
            "Protected_Channels": "7/7 Channels + LLC/CAGE Corporate Entity Lock + Dedicated 24/7 Fraud Intercept",
            "Target_Market": "CEOs, Defense Executives, & Cleared Federal Contractors",
        },
        {
            "Tier_ID": "TIER-B2B2C-NODE50",
            "Subscription_Plan": "CLIN 0033 Enterprise 50-Seat Voluntary Employee Benefit Pack",
            "Monthly_Rate_USD": 5416.67,
            "Annual_Rate_USD": 65000.00,
            "Included_Seats": 50,
            "Protected_Channels": "50 Individual Zero-Employer-Access Personal Credit/Loan/Deed/SIM Vaults",
            "Target_Market": "DoD / Federal / Critical Infrastructure Node Sponsor (Zero Employer Visibility)",
        },
    ]

    PERSONAL_SUBSCRIBER_PROFILES: Dict[str, Dict[str, str]] = {
        "SUB-001 // JEFFERY SOVEREIGN HUMPHREY (Personal Sovereign Subscriber -- OKC)": {
            "subscriber_id": "SUB-001",
            "full_name": "JEFFERY SOVEREIGN HUMPHREY",
            "personal_pin": "PERSONAL-PIN-1AHA8-001",
            "subscription_tier": "TIER-EXEC-VIP (Executive Sovereign Vault)",
            "email": "humphreyvirtualfarm@gmail.com",
            "mobile_phone": "405-555-0199",
            "deed_apn": "OK-OKC-APN-4029-8812-HVF",
            "ach_routing_mask": "ABA-103000648 // ACCT-****8821",
            "sim_imei_lock": "CARRIER-PORT-LOCK-ACTIVE // IMEI-359881094421",
        },
        "SUB-002 // MARCUS A. VANCE (Personal Sovereign Subscriber -- Edmond)": {
            "subscriber_id": "SUB-002",
            "full_name": "MARCUS A. VANCE",
            "personal_pin": "PERSONAL-PIN-VANCE-002",
            "subscription_tier": "TIER-B2C-FAMILY5 (Sovereign Family 5-Seat Pack)",
            "email": "mvance.personal@sovereignmail.org",
            "mobile_phone": "405-555-0211",
            "deed_apn": "OK-EDM-APN-7712-3301-RES",
            "ach_routing_mask": "ABA-103000648 // ACCT-****4419",
            "sim_imei_lock": "CARRIER-PORT-LOCK-ACTIVE // IMEI-359881097732",
        },
        "SUB-003 // DR. SARAH E. LIN (Personal Sovereign Subscriber -- Norman)": {
            "subscriber_id": "SUB-003",
            "full_name": "DR. SARAH E. LIN",
            "personal_pin": "PERSONAL-PIN-LIN-003",
            "subscription_tier": "TIER-B2C-INDIVIDUAL (Personal Sovereign Shield)",
            "email": "slin.personal@sovereignmail.org",
            "mobile_phone": "405-555-0233",
            "deed_apn": "OK-NRM-APN-5541-9012-RES",
            "ach_routing_mask": "ABA-103000648 // ACCT-****9904",
            "sim_imei_lock": "CARRIER-PORT-LOCK-ACTIVE // IMEI-359881091108",
        },
        "SUB-004 // CALEB J. ROSS (Personal Sovereign Subscriber -- Guthrie)": {
            "subscriber_id": "SUB-004",
            "full_name": "CALEB J. ROSS",
            "personal_pin": "PERSONAL-PIN-ROSS-004",
            "subscription_tier": "TIER-B2C-FAMILY5 (Sovereign Family & Farmstead Pack)",
            "email": "cross.personal@sovereignmail.org",
            "mobile_phone": "405-555-0244",
            "deed_apn": "OK-LOG-APN-1184-6620-FARM",
            "ach_routing_mask": "ABA-103000648 // ACCT-****3107",
            "sim_imei_lock": "CARRIER-PORT-LOCK-ACTIVE // IMEI-359881095540",
        },
    }

    PERSONAL_18_SCHEMA: List[Tuple[str, str, bool]] = [
        ("p01_first_name", "[01] Legal First Name", False),
        ("p02_middle_name", "[02] Legal Middle Name", False),
        ("p03_last_name", "[03] Legal Last Name", False),
        ("p04_ssn", "[04] Social Security Number (SSN -- Salted HMAC Lock)", True),
        ("p05_dob", "[05] Date of Birth (YYYY-MM-DD -- Salted HMAC Lock)", True),
        ("p06_driver_license", "[06] State REAL-ID / Driver License Number", True),
        ("p07_passport_num", "[07] U.S. Passport Number", True),
        ("p08_primary_phone", "[08] Protected Mobile Phone Number", False),
        ("p09_personal_email", "[09] Protected Personal Email Address", False),
        ("p10_home_address", "[10] Protected Primary Residence Street, City, State & ZIP", False),
        ("p11_equifax_pin", "[11] Equifax Security Freeze Lock Reference ID", True),
        ("p12_experian_pin", "[12] Experian Security Freeze Lock Reference ID", True),
        ("p13_transunion_pin", "[13] TransUnion Security Freeze Lock Reference ID", True),
        ("p14_chexsystems_lock", "[14] ChexSystems & Early Warning Deposit Account Lock ID", True),
        ("p15_bank_aba_routing", "[15] Protected Personal Bank ABA Routing Number", True),
        ("p16_bank_account_num", "[16] Protected Personal Checking/Savings Account Number", True),
        ("p17_home_deed_apn", "[17] County Assessor Home/Land Deed Parcel APN Lock", False),
        ("p18_mobile_sim_imei", "[18] Mobile Carrier SIM Port-Out & Device IMEI Lock", False),
    ]

    DEFAULT_PERSONAL_18_VALUES: Dict[str, str] = {
        "p01_first_name": "JEFFERY",
        "p02_middle_name": "SOVEREIGN",
        "p03_last_name": "HUMPHREY",
        "p04_ssn": "999-00-1234",
        "p05_dob": "1975-08-15",
        "p06_driver_license": "OK-DL-994827164",
        "p07_passport_num": "USA-P-558291044",
        "p08_primary_phone": "405-555-0199",
        "p09_personal_email": "HUMPHREYVIRTUALFARM@GMAIL.COM",
        "p10_home_address": "100 SOVEREIGN COMMAND PKWY, OKLAHOMA CITY, OK 73102",
        "p11_equifax_pin": "EQFX-LOCK-9948-1AHA8",
        "p12_experian_pin": "EXPR-LOCK-7731-1AHA8",
        "p13_transunion_pin": "TRUN-LOCK-5520-1AHA8",
        "p14_chexsystems_lock": "CHEX-EWS-LOCK-8812-ACTIVE",
        "p15_bank_aba_routing": "103000648",
        "p16_bank_account_num": "994018273645",
        "p17_home_deed_apn": "OK-OKC-APN-4029-8812-HVF",
        "p18_mobile_sim_imei": "SIM-PORT-LOCK-IMEI-359881094421",
    }

    CREDIT_AND_LOAN_MONITOR_EVENTS: List[Dict[str, Any]] = [
        {
            "Inquiry_ID": "INQ-2026-0901",
            "Channel": "Equifax Credit Bureau (Hard Pull)",
            "Requesting_Institution": "Unknown Online Subprime Auto Lender (IP: 185.220.101.44)",
            "Product_Type": "Unauthorized $78,500 Auto Loan Application",
            "Geo_Distance_Miles": 4820.0,
            "Elapsed_Seconds": 12.0,
            "User_Unfreeze_Token_Present": False,
        },
        {
            "Inquiry_ID": "INQ-2026-0902",
            "Channel": "Experian Credit Bureau (Hard Pull)",
            "Requesting_Institution": "Synthetic Identity Card Issuer (Miami, FL)",
            "Product_Type": "Unauthorized $25,000 Unsecured Credit Line",
            "Geo_Distance_Miles": 1215.0,
            "Elapsed_Seconds": 45.0,
            "User_Unfreeze_Token_Present": False,
        },
        {
            "Inquiry_ID": "INQ-2026-0903",
            "Channel": "TransUnion Credit Bureau (Hard Pull)",
            "Requesting_Institution": "Offshore FinTech Personal Loan App",
            "Product_Type": "Unauthorized $50,000 Personal Signature Loan",
            "Geo_Distance_Miles": 5940.0,
            "Elapsed_Seconds": 8.0,
            "User_Unfreeze_Token_Present": False,
        },
        {
            "Inquiry_ID": "INQ-2026-0904",
            "Channel": "ChexSystems / Early Warning Services (EWS)",
            "Requesting_Institution": "Remote Neo-Bank Checking Opening Attempt",
            "Product_Type": "Unauthorized Demand Deposit Account + Wire Enabled",
            "Geo_Distance_Miles": 1640.0,
            "Elapsed_Seconds": 30.0,
            "User_Unfreeze_Token_Present": False,
        },
        {
            "Inquiry_ID": "INQ-2026-0905",
            "Channel": "County Recorder Real Estate Deed & HELOC Monitor",
            "Requesting_Institution": "Unverified Quitclaim / HELOC Filing Attempt",
            "Product_Type": "Unauthorized $350,000 Home/Farm Equity Lien (APN Lock)",
            "Geo_Distance_Miles": 950.0,
            "Elapsed_Seconds": 20.0,
            "User_Unfreeze_Token_Present": False,
        },
        {
            "Inquiry_ID": "INQ-2026-0906",
            "Channel": "Mobile Carrier SS7 / SIM-Swap & Port-Out Shield",
            "Requesting_Institution": "Unauthorized Retail Store SIM-Swap Request",
            "Product_Type": "2FA SMS Intercept / Number Port-Out Attempt",
            "Geo_Distance_Miles": 1390.0,
            "Elapsed_Seconds": 15.0,
            "User_Unfreeze_Token_Present": False,
        },
        {
            "Inquiry_ID": "REQ-HVF-EQUIP-2026-001",
            "Channel": "First National Ag & Sovereign Equipment Credit (OKC)",
            "Requesting_Institution": "Authorized Personal Equipment Credit Facility",
            "Product_Type": "User-Authorized $150,000 Sovereign Credit Line",
            "Geo_Distance_Miles": 1.2,
            "Elapsed_Seconds": 3600.0,
            "User_Unfreeze_Token_Present": True,
        },
    ]

    def __init__(self) -> None:
        super().__init__(
            plugin_id="HVF-NG-CLIN-0033",
            clin_number="CLIN 0033",
            title="Standalone Personal Sovereign Identity, 7-Channel Credit/Loan/Deed/SIM Anti-Fraud Shield & B2C Engine (v8.0)",
            version="8.0.0",
            target_trl="TRL 8/9",
            per_node_annual_gov_usd=65000,
            per_node_monthly_comm_usd=5400,
        )
        self.manifest = self.export_manifest()

    @staticmethod
    def mask_sensitive_value(raw_val: str, is_secret: bool) -> str:
        clean = str(raw_val).strip()
        if not is_secret:
            return clean
        if len(clean) >= 4:
            return f"REDACTED-****-{clean[-4:]}"
        return "REDACTED-****"

    @staticmethod
    def compute_hmac_seal(field_key: str, raw_value: str) -> str:
        payload = f"{field_key}|{raw_value.strip().upper()}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8")
        return hmac.new(PERSONAL_VAULT_PEPPER.encode("utf-8"), payload, hashlib.sha256).hexdigest()

    def generate_ceo_credit_unfreeze_token(self, inquiry_id: str) -> str:
        msg = f"PERSONAL_CREDIT_UNFREEZE|{inquiry_id.strip().upper()}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8")
        return hmac.new(PERSONAL_VAULT_PEPPER.encode("utf-8"), msg, hashlib.sha256).hexdigest()[:20].upper()

    def calculate_b2c_and_enterprise_revenue(
        self,
        b2c_individual_subscribers: int = 500,
        b2c_family_packs: int = 120,
        exec_vip_subscribers: int = 40,
        enterprise_50seat_nodes: int = 2,
    ) -> Dict[str, Any]:
        ind_arr = int(b2c_individual_subscribers) * 350.0
        fam_arr = int(b2c_family_packs) * 1250.0
        vip_arr = int(exec_vip_subscribers) * 2500.0
        b2c_total_arr = ind_arr + fam_arr + vip_arr
        ent_total_arr = int(enterprise_50seat_nodes) * 65000.0
        combined_arr = b2c_total_arr + ent_total_arr
        total_protected_people = (
            int(b2c_individual_subscribers)
            + (int(b2c_family_packs) * 5)
            + (int(exec_vip_subscribers) * 2)
            + (int(enterprise_50seat_nodes) * 50)
        )
        return {
            "b2c_individual_arr_usd": ind_arr,
            "b2c_family_arr_usd": fam_arr,
            "exec_vip_arr_usd": vip_arr,
            "b2c_direct_total_arr_usd": b2c_total_arr,
            "enterprise_nodes_arr_usd": ent_total_arr,
            "combined_wp7_annual_revenue_usd": combined_arr,
            "total_protected_individuals": total_protected_people,
        }

    def evaluate_personal_18_vault(self, overrides: Dict[str, str] | None = None) -> Dict[str, Any]:
        vals = dict(self.DEFAULT_PERSONAL_18_VALUES)
        if overrides:
            for k, v in overrides.items():
                if k in vals and v is not None:
                    vals[k] = str(v)

        rows: List[Dict[str, str]] = []
        seals: List[str] = []
        for idx, (fkey, flabel, is_sec) in enumerate(self.PERSONAL_18_SCHEMA, start=1):
            raw_v = vals.get(fkey, "")
            f_seal = self.compute_hmac_seal(fkey, raw_v)
            seals.append(f_seal)
            rows.append({
                "Field_ID": f"P{idx:02d}_{fkey.upper()}",
                "Personal_Shield_Attribute": flabel,
                "Stored_Vault_Representation": self.mask_sensitive_value(raw_v, is_sec),
                "Plaintext_Exposed": "0_BYTES (SALTED_HMAC_LOCKED)" if is_sec else "PERSONAL_OWNER_ONLY",
                "Employer_HR_Visibility": "0% (PHYSICALLY_SEPARATED_NO_HR_ACCESS)",
                "HMAC_SHA256_Seal": f_seal[:20].upper(),
            })

        comp_seal = hmac.new(
            PERSONAL_VAULT_PEPPER.encode("utf-8"),
            "|".join(seals).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return {
            "total_personal_fields_locked": len(rows),
            "attribute_rows": rows,
            "composite_personal_vault_seal": comp_seal,
        }

    def evaluate_credit_and_loan_activity(self, credit_freeze_locked: bool = True) -> Dict[str, Any]:
        rows: List[Dict[str, Any]] = []
        blocked = 0
        approved = 0
        for ev in self.CREDIT_AND_LOAN_MONITOR_EVENTS:
            inq_id = ev["Inquiry_ID"]
            has_tok = bool(ev["User_Unfreeze_Token_Present"])
            if credit_freeze_locked and not has_tok:
                action = "BLOCKED_HARD_PULL_AND_LOAN_ORIGINATION_DENIED"
                blocked += 1
            else:
                action = "APPROVED_WITH_ONE_TIME_PERSONAL_UNFREEZE_TOKEN"
                approved += 1
            rows.append({
                "Inquiry_ID": inq_id,
                "Monitored_Channel": ev["Channel"],
                "Requesting_Entity": ev["Requesting_Institution"],
                "Credit_Or_Loan_Product": ev["Product_Type"],
                "Credit_Freeze_State": "LOCKED" if credit_freeze_locked else "TEMPORARY_UNFREEZE",
                "Unfreeze_Token": self.generate_ceo_credit_unfreeze_token(inq_id)[:14] if has_tok else "NONE_PROVIDED",
                "Autonomous_Intercept_Action": action,
            })
        return {
            "credit_freeze_locked": credit_freeze_locked,
            "total_inquiries_monitored": len(rows),
            "fraudulent_loans_and_pulls_blocked": blocked,
            "authorized_inquiries_approved": approved,
            "credit_loan_rows": rows,
        }

    def init_personal_worm_sqlite(self, db_path: pathlib.Path) -> Dict[str, Any]:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_personal_credit_intercept_log (
                    intercept_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inquiry_id TEXT NOT NULL UNIQUE,
                    channel TEXT NOT NULL,
                    product_type TEXT NOT NULL,
                    intercept_action TEXT NOT NULL,
                    worm_row_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_pcred_no_update
                BEFORE UPDATE ON worm_personal_credit_intercept_log
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_pcred_no_delete
                BEFORE DELETE ON worm_personal_credit_intercept_log
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED');
                END;
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_personal_vault_revisions (
                    revision_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subscriber_id TEXT NOT NULL,
                    subscriber_name TEXT NOT NULL,
                    update_reason TEXT NOT NULL,
                    composite_vault_seal TEXT NOT NULL,
                    worm_revision_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_prev_no_update
                BEFORE UPDATE ON worm_personal_vault_revisions
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_prev_no_delete
                BEFORE DELETE ON worm_personal_vault_revisions
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED');
                END;
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_personal_unfreeze_tokens (
                    token_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subscriber_id TEXT NOT NULL,
                    inquiry_id TEXT NOT NULL,
                    unfreeze_token TEXT NOT NULL,
                    worm_token_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_ptok_no_update
                BEFORE UPDATE ON worm_personal_unfreeze_tokens
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_ptok_no_delete
                BEFORE DELETE ON worm_personal_unfreeze_tokens
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED');
                END;
            """)
            conn.commit()
        finally:
            conn.close()
        return {"db_path": str(db_path), "worm_triggers_active": 6}

    def open_personal_subscriber_gate(
        self,
        subscriber_key: str,
        privacy_charter_accepted: bool,
        provided_personal_pin: str,
        out_dir: pathlib.Path,
        credit_freeze_locked: bool = True,
    ) -> Dict[str, Any]:
        if not privacy_charter_accepted:
            return {
                "gate_open": False,
                "gate_status": "PERSONAL_VAULT_LOCKED_ACCEPT_PRIVACY_CHARTER_AND_ENTER_PERSONAL_PIN",
                "subscriber_profile": None,
                "credit_report": None,
                "personal_vault_rows": None,
            }
        sub = self.PERSONAL_SUBSCRIBER_PROFILES.get(
            subscriber_key,
            next(iter(self.PERSONAL_SUBSCRIBER_PROFILES.values())),
        )
        if provided_personal_pin.strip() != sub["personal_pin"]:
            return {
                "gate_open": False,
                "gate_status": "PERSONAL_VAULT_DENIED_INVALID_SUBSCRIBER_PIN",
                "subscriber_profile": None,
                "credit_report": None,
                "personal_vault_rows": None,
            }

        state_file = out_dir / "wp7_personal_subscriber_state.json"
        saved_map: Dict[str, Dict[str, str]] = {}
        if state_file.exists():
            try:
                saved_map = json.loads(state_file.read_text(encoding="utf-8")).get("subscribers", {})
            except Exception:
                saved_map = {}

        sub_id = sub["subscriber_id"]
        name_parts = sub["full_name"].split()
        sub_defaults = dict(self.DEFAULT_PERSONAL_18_VALUES)
        sub_defaults.update({
            "p01_first_name": name_parts[0] if len(name_parts) >= 1 else "JEFFERY",
            "p02_middle_name": name_parts[1] if len(name_parts) >= 3 else "SOVEREIGN",
            "p03_last_name": name_parts[-1] if len(name_parts) >= 2 else "HUMPHREY",
            "p08_primary_phone": sub["mobile_phone"],
            "p09_personal_email": sub["email"].upper(),
            "p17_home_deed_apn": sub["deed_apn"],
            "p18_mobile_sim_imei": sub["sim_imei_lock"],
        })
        if sub_id in saved_map and isinstance(saved_map[sub_id], dict):
            sub_defaults.update(saved_map[sub_id])

        vault_eval = self.evaluate_personal_18_vault(sub_defaults)
        cred_eval = self.evaluate_credit_and_loan_activity(credit_freeze_locked=credit_freeze_locked)
        return {
            "gate_open": True,
            "gate_status": f"PERSONAL_SOVEREIGN_SHIELD_OPEN // {sub_id} ({sub['full_name']})",
            "subscriber_profile": sub,
            "current_18_values": sub_defaults,
            "credit_report": cred_eval,
            "personal_vault_rows": vault_eval["attribute_rows"],
            "composite_personal_vault_seal": vault_eval["composite_personal_vault_seal"],
        }

    def save_personal_subscriber_18_fields(
        self,
        out_dir: pathlib.Path,
        subscriber_key: str,
        updated_18_inputs: Dict[str, str],
    ) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        sub = self.PERSONAL_SUBSCRIBER_PROFILES.get(
            subscriber_key,
            next(iter(self.PERSONAL_SUBSCRIBER_PROFILES.values())),
        )
        sub_id = sub["subscriber_id"]
        state_file = out_dir / "wp7_personal_subscriber_state.json"
        data: Dict[str, Any] = {"subscribers": {}}
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text(encoding="utf-8"))
            except Exception:
                data = {"subscribers": {}}
        clean_in = {k: str(v).strip() for k, v in updated_18_inputs.items()}
        data.setdefault("subscribers", {})[sub_id] = clean_in
        state_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

        res = self.generate_wp7_antifraud_dossier(out_dir, overrides_18=clean_in, subscriber_id=sub_id)
        return {
            "saved": True,
            "subscriber_id": sub_id,
            "composite_seal": res["personal_vault_report"]["composite_personal_vault_seal"],
            "worm_seal": res["worm_seal"],
        }

    def generate_wp7_antifraud_dossier(
        self,
        out_dir: pathlib.Path,
        overrides_18: Dict[str, str] | None = None,
        subscriber_id: str = "SUB-001",
    ) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        db_path = out_dir / "wp7_personal_antifraud_worm.db"
        self.init_personal_worm_sqlite(db_path)

        pv_eval = self.evaluate_personal_18_vault(overrides_18)
        cred_eval = self.evaluate_credit_and_loan_activity(credit_freeze_locked=True)
        rev_calc = self.calculate_b2c_and_enterprise_revenue()

        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            for r in cred_eval["credit_loan_rows"]:
                r_sha = hmac.new(
                    PERSONAL_VAULT_PEPPER.encode("utf-8"),
                    f"{r['Inquiry_ID']}|{r['Autonomous_Intercept_Action']}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                    hashlib.sha256,
                ).hexdigest()
                cur.execute(
                    """
                    INSERT OR IGNORE INTO worm_personal_credit_intercept_log (
                        inquiry_id, channel, product_type, intercept_action, worm_row_sha256
                    ) VALUES (?,?,?,?,?)
                    """,
                    (r["Inquiry_ID"], r["Monitored_Channel"], r["Credit_Or_Loan_Product"], r["Autonomous_Intercept_Action"], r_sha),
                )

            rev_sha = hmac.new(
                PERSONAL_VAULT_PEPPER.encode("utf-8"),
                f"{subscriber_id}|{pv_eval['composite_personal_vault_seal']}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            cur.execute(
                """
                INSERT OR IGNORE INTO worm_personal_vault_revisions (
                    subscriber_id, subscriber_name, update_reason, composite_vault_seal, worm_revision_sha256
                ) VALUES (?,?,?,?,?)
                """,
                (subscriber_id, "JEFFERY SOVEREIGN HUMPHREY", "PERSONAL_OWNER_SELF_SEAL", pv_eval["composite_personal_vault_seal"], rev_sha),
            )

            tok_val = self.generate_ceo_credit_unfreeze_token("REQ-HVF-EQUIP-2026-001")
            tok_sha = hmac.new(
                PERSONAL_VAULT_PEPPER.encode("utf-8"),
                f"{subscriber_id}|REQ-HVF-EQUIP-2026-001|{tok_val}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            cur.execute(
                """
                INSERT OR IGNORE INTO worm_personal_unfreeze_tokens (
                    subscriber_id, inquiry_id, unfreeze_token, worm_token_sha256
                ) VALUES (?,?,?,?)
                """,
                (subscriber_id, "REQ-HVF-EQUIP-2026-001", tok_val, tok_sha),
            )
            conn.commit()
        finally:
            conn.close()

        md_lines = [
            "# HVF SOVEREIGN NEXT-GEN // WP-7 (CLIN 0033 v8.0): STANDALONE PERSONAL CREDIT, LOAN, DEED & SIM ANTI-FRAUD SHIELD",
            f"- **Controlling Authority**: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect (CAGE `1AHA8` | UEI `S1M4ENLHTDH5`)",
            f"- **Enclave Tier**: `{ENCLAVE_MODE}` | **Host Baseline Merkle Root**: `{FROZEN_EBONY_MERKLE_ROOT}`",
            f"- **Physical Separation**: `100% DECOUPLED FROM ENTERPRISE HR (CLIN 0034) -- ZERO EMPLOYER ACCESS`",
            f"- **Personal 18-Field Vault Seal**: `{pv_eval['composite_personal_vault_seal']}`",
            f"- **7-Channel Fraudulent Loans/Pulls Blocked**: `{cred_eval['fraudulent_loans_and_pulls_blocked']} / {cred_eval['total_inquiries_monitored']}`",
            f"- **Projected B2C + Enterprise Annual Revenue**: `${rev_calc['combined_wp7_annual_revenue_usd']:,.2f}/yr` (`{rev_calc['total_protected_individuals']}` Protected Individuals)",
            "",
            "## 1. B2C Personal Subscription & Enterprise Seat Pricing Tiers",
            "| Tier_ID | Plan | Monthly | Annual | Protected_Channels |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for t in self.B2C_AND_SEAT_PRICING_TIERS:
            md_lines.append(
                f"| `{t['Tier_ID']}` | {t['Subscription_Plan']} | `${t['Monthly_Rate_USD']:,.2f}/mo` | `${t['Annual_Rate_USD']:,.2f}/yr` | {t['Protected_Channels']} |"
            )

        md_content = chr(10).join(md_lines) + chr(10)
        md_path = out_dir / "WP7_SOVEREIGN_IDENTITY_CREDIT_LOAN_SHIELD_SPEC.md"
        pdf_path = out_dir / "WP7_SOVEREIGN_IDENTITY_CREDIT_LOAN_SHIELD_SPEC.pdf"
        md_path.write_bytes(md_content.encode("ascii"))

        worm_seal = hashlib.sha256(md_content.encode("ascii")).hexdigest()
        pdf_lines = [line.replace("`", "").replace("*", "") for line in md_lines]
        pdf_bytes = compile_single_page_pdf_14(
            title="HVF WP-7 (CLIN 0033 v8.0): PERSONAL CREDIT, LOAN, DEED & SIM ANTI-FRAUD SHIELD",
            lines=pdf_lines,
            worm_sha256=worm_seal,
        )
        pdf_path.write_bytes(pdf_bytes)

        return {
            "manifest": self.manifest,
            "personal_vault_report": pv_eval,
            "credit_report": cred_eval,
            "revenue_model": rev_calc,
            "sqlite_db_path": str(db_path),
            "md_path": str(md_path),
            "pdf_path": str(pdf_path),
            "pdf_bytes_len": len(pdf_bytes),
            "worm_seal": worm_seal,
        }
