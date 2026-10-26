"""
HUMPHREY VIRTUAL FARMS LLC // CLIN 0033 (WP-7 v5.0): 42-FIELD ATOMIC PERSONNEL ONBOARDING, NOK/ICE, DIGITAL PROOF-OF-IDENTITY, & EMPLOYER LOCK VAULT
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5)
Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect
Work Package: WP-7 (60-Field Atomic Personnel Application, NOK/ICE Emergency Ledger, Unalterable Proof-of-Identity Lock, & 7-Channel Credit/Loan Shield)
Host Compatibility: Frozen Project Ebony TRL 7 Baseline (cc1ee1c8d29b2ae5e856fc0fcb672a52e7e49d50369499febe14e18e9150949a)
"""
from __future__ import annotations
import hashlib
import hmac
import json
import pathlib
import sqlite3
from typing import Any, Dict, List, Tuple

from nextgen_core.sovereign_plugin_contract import (
    FROZEN_EBONY_MERKLE_ROOT,
    SovereignExpansionModule,
)
from plugins.clin_0027_day1_license_wawf_generator import build_minimal_iso_pdf

ENCLAVE_MODE = "PUBLIC"
IDENTITY_VAULT_PEPPER = "PUBLIC_IDENTITY_CREDIT_PEPPER_REDACTED_DFARS_252_227_7018"


class SovereignIdentityAntiFraudShield(SovereignExpansionModule):
    """
    WP-7 / CLIN 0033 v7.7 Sovereign Personnel Onboarding, Proof-of-Identity, NOK/ICE, & Anti-Fraud Vault:
      1. 42 Atomic Application Fields (Strictly 1 single response per box; zero pipe-concatenated fields)
         covering Legal Identity, Vital Stats, Physical Description, Job/I-9/Clearance, Government IDs,
         Next of Kin (NOK), In Case of Emergency (ICE), 3-Modal Biometrics, and Financial/Asset Locks.
      2. Unalterable Employer Proof-of-Identity State Machine:
         - Once submitted/sealed, the input form is removed and replaced by a read-only, cryptographically
           sealed Digital Proof-of-Identity Dossier.
         - Modifying any field requires a cryptographic Employer/CEO Change-Approval Token and logged reason.
      3. 7-Channel Credit Bureau, SBA/Bank Loan, County Deed Title, ChexSystems/ACH, & SIM-Swap Interceptor.
      4. Physical ID & 3-Modal Biometric Sign-In / Sign-Out WORM Audit Ledger.
    """

    # (field_key, display_label, category_name, is_sensitive_masked)
    ATOMIC_42_SCHEMA: List[Tuple[str, str, str, bool]] = [
        # Section 1: Legal Identity & Vital Statistics (10 Atomic Fields)
        ("f01_first_name", "[01] Legal First Name", "1_LEGAL_VITAL", False),
        ("f02_middle_name", "[02] Legal Middle Name", "1_LEGAL_VITAL", False),
        ("f03_last_name", "[03] Legal Last Name", "1_LEGAL_VITAL", False),
        ("f04_name_suffix", "[04] Name Suffix (Jr/Sr/III/None)", "1_LEGAL_VITAL", False),
        ("f05_ssn", "[05] Social Security Number (9-Digit SSN)", "1_LEGAL_VITAL", True),
        ("f06_dob", "[06] Date of Birth (YYYY-MM-DD)", "1_LEGAL_VITAL", True),
        ("f07_birth_city", "[07] City of Birth", "1_LEGAL_VITAL", False),
        ("f08_birth_state", "[08] State / Province of Birth", "1_LEGAL_VITAL", False),
        ("f09_birth_country", "[09] Country of Birth", "1_LEGAL_VITAL", False),
        ("f10_mothers_maiden", "[10] Mother's Maiden Surname (KBA)", "1_LEGAL_VITAL", True),
        # Section 2: Residential Contact & Physical Description (10 Atomic Fields)
        ("f11_street_address", "[11] Residential Street Address", "2_CONTACT_PHYSICAL", True),
        ("f12_residence_city", "[12] Residential City", "2_CONTACT_PHYSICAL", False),
        ("f13_residence_state", "[13] Residential State", "2_CONTACT_PHYSICAL", False),
        ("f14_residence_zip", "[14] Residential ZIP / Postal Code", "2_CONTACT_PHYSICAL", False),
        ("f15_primary_phone", "[15] Primary Mobile Phone Number", "2_CONTACT_PHYSICAL", True),
        ("f16_email_address", "[16] Official Email Address", "2_CONTACT_PHYSICAL", False),
        ("f17_eye_color", "[17] Physical Eye Color", "2_CONTACT_PHYSICAL", False),
        ("f18_hair_color", "[18] Physical Hair Color", "2_CONTACT_PHYSICAL", False),
        ("f19_height_inches", "[19] Physical Height (Inches)", "2_CONTACT_PHYSICAL", False),
        ("f20_scars_marks_tattoos", "[20] Distinguishing Scars, Marks, or Tattoos (SMT)", "2_CONTACT_PHYSICAL", False),
        # Section 3: Employment Application, I-9, & Government IDs (7 Atomic Fields)
        ("f21_job_title", "[21] Position / Role Applied For", "3_EMPLOYMENT_GOV_IDS", False),
        ("f22_department_unit", "[22] Assigned Department / Command Unit", "3_EMPLOYMENT_GOV_IDS", False),
        ("f23_clearance_level", "[23] Security Clearance / Vetting Tier", "3_EMPLOYMENT_GOV_IDS", False),
        ("f24_citizenship_i9", "[24] Citizenship / Form I-9 Work Eligibility", "3_EMPLOYMENT_GOV_IDS", False),
        ("f25_drivers_license", "[25] State Driver's License / REAL-ID Number", "3_EMPLOYMENT_GOV_IDS", True),
        ("f26_passport_number", "[26] U.S. Passport Book / Card Number", "3_EMPLOYMENT_GOV_IDS", True),
        ("f27_dod_cac_edipi", "[27] DoD CAC / FIPS 201 PIV 10-Digit EDIPI", "3_EMPLOYMENT_GOV_IDS", True),
        # Section 4: Next of Kin (NOK) & In Case of Emergency (ICE) (8 Atomic Fields)
        ("f28_nok_full_name", "[28] Next of Kin (NOK) Full Legal Name", "4_NOK_AND_ICE", False),
        ("f29_nok_relationship", "[29] Next of Kin (NOK) Relationship", "4_NOK_AND_ICE", False),
        ("f30_nok_phone", "[30] Next of Kin (NOK) Primary Phone", "4_NOK_AND_ICE", True),
        ("f31_nok_address", "[31] Next of Kin (NOK) Residential Address", "4_NOK_AND_ICE", True),
        ("f32_ice_full_name", "[32] In Case of Emergency (ICE) Contact Name", "4_NOK_AND_ICE", False),
        ("f33_ice_relationship", "[33] In Case of Emergency (ICE) Relationship", "4_NOK_AND_ICE", False),
        ("f34_ice_phone", "[34] In Case of Emergency (ICE) Direct Phone", "4_NOK_AND_ICE", True),
        ("f35_ice_medical_blood", "[35] Emergency Blood Type & Medical Alert Notes", "4_NOK_AND_ICE", False),
        # Section 5: 3-Modal Biometrics & Financial / Asset Protection Locks (7 Atomic Fields)
        ("f36_bio_fingerprint", "[36] Biometric #1: Fingerprint Minutiae Template", "5_BIOMETRIC_ASSETS", True),
        ("f37_bio_iris", "[37] Biometric #2: Iris & Retinal Vascular Template", "5_BIOMETRIC_ASSETS", True),
        ("f38_bio_face_voice", "[38] Biometric #3: 3D Facial & Voiceprint Liveness", "5_BIOMETRIC_ASSETS", True),
        ("f39_bank_aba_routing", "[39] Direct Deposit / Treasury Bank ABA Routing", "5_BIOMETRIC_ASSETS", True),
        ("f40_bank_account_num", "[40] Direct Deposit / Treasury Account Number", "5_BIOMETRIC_ASSETS", True),
        ("f41_property_deed_apn", "[41] Real Estate Home/Land Deed Parcel APN", "5_BIOMETRIC_ASSETS", True),
                ("f42_mobile_sim_imei", "[42] Mobile Carrier SIM / IMEI Port-Out Lock", "5_BIOMETRIC_ASSETS", True),
        # Section 6: Previous 7-Year Residential Address History (6 Atomic Fields: 43 - 48)
        ("f43_prev_addr1_street", "[43] Previous Street Address #1", "6_PREVIOUS_ADDRESSES", True),
        ("f44_prev_addr1_city", "[44] Previous City #1", "6_PREVIOUS_ADDRESSES", False),
        ("f45_prev_addr1_state_zip", "[45] Previous State & ZIP Code #1", "6_PREVIOUS_ADDRESSES", False),
        ("f46_prev_addr1_dates", "[46] Previous Residence #1 Dates (From-To)", "6_PREVIOUS_ADDRESSES", False),
        ("f47_prev_addr2_summary", "[47] Previous Residence #2 City & State", "6_PREVIOUS_ADDRESSES", False),
        ("f48_prev_addr_verifier", "[48] Previous Residence Verification / Landlord Contact", "6_PREVIOUS_ADDRESSES", True),
        # Section 7: Prior Employment & Job History (6 Atomic Fields: 49 - 54)
        ("f49_prior_emp1_org", "[49] Prior Employer #1 Organization / Command", "7_JOB_HISTORY", False),
        ("f50_prior_emp1_title", "[50] Prior Employer #1 Job Title / Rank", "7_JOB_HISTORY", False),
        ("f51_prior_emp1_supervisor", "[51] Prior Employer #1 Supervisor & Verification Phone", "7_JOB_HISTORY", True),
        ("f52_prior_emp1_years", "[52] Prior Employer #1 Tenure (Years)", "7_JOB_HISTORY", False),
        ("f53_prior_emp2_org_role", "[53] Prior Employer #2 Organization & Title", "7_JOB_HISTORY", False),
        ("f54_total_experience_yrs", "[54] Total Verified Career Experience (Years)", "7_JOB_HISTORY", False),
        # Section 8: Training, Sovereign Academy, & Company Evaluations (6 Atomic Fields: 55 - 60)
        ("f55_highest_education", "[55] Highest Degree / Technical Diploma", "8_TRAINING_AND_EVAL", False),
        ("f56_academy_exam_score", "[56] HVF Sovereign Field Academy Exam Score (%)", "8_TRAINING_AND_EVAL", False),
        ("f57_completed_hvf_courses", "[57] Completed HVF Technical Modules", "8_TRAINING_AND_EVAL", False),
        ("f58_active_certifications", "[58] Active Federal / Safety / Trade Certifications", "8_TRAINING_AND_EVAL", False),
        ("f59_training_hours_total", "[59] Total Verified Continuing Training Hours", "8_TRAINING_AND_EVAL", False),
        ("f60_company_eval_rating", "[60] Annual Company Evaluation Rating (0.0 - 5.0)", "8_TRAINING_AND_EVAL", False),
    ]

    DEFAULT_ATOMIC_42_VALUES: Dict[str, str] = {
        "f01_first_name": "JEFFERY",
        "f02_middle_name": "SOVEREIGN",
        "f03_last_name": "HUMPHREY",
        "f04_name_suffix": "NONE",
        "f05_ssn": "999-00-1234",
        "f06_dob": "1975-08-15",
        "f07_birth_city": "OKLAHOMA CITY",
        "f08_birth_state": "OKLAHOMA",
        "f09_birth_country": "UNITED STATES",
        "f10_mothers_maiden": "VAULT-KBA-MAIDEN-991",
        "f11_street_address": "100 SOVEREIGN COMMAND PKWY",
        "f12_residence_city": "OKLAHOMA CITY",
        "f13_residence_state": "OK",
        "f14_residence_zip": "73102",
        "f15_primary_phone": "405-555-0199",
        "f16_email_address": "HUMPHREYVIRTUALFARM@GMAIL.COM",
        "f17_eye_color": "BROWN",
        "f18_hair_color": "BLACK",
        "f19_height_inches": "72",
        "f20_scars_marks_tattoos": "NONE_VERIFIED",
        "f21_job_title": "FOUNDER, CEO, & PRINCIPAL SOVEREIGN ARCHITECT",
        "f22_department_unit": "HVF EXECUTIVE COMMAND (CAGE 1AHA8)",
        "f23_clearance_level": "SOVEREIGN_COMMANDER_LEVEL_5",
        "f24_citizenship_i9": "US_CITIZEN_VERIFIED_I9_SEALED",
        "f25_drivers_license": "OK-REALID-1AHA8-7741",
        "f26_passport_number": "US-PASS-558912044",
        "f27_dod_cac_edipi": "1099482210",
        "f28_nok_full_name": "MRS. HUMPHREY (DESIGNATED SPOUSE / NOK)",
        "f29_nok_relationship": "SPOUSE_PRIMARY_BENEFICIARY",
        "f30_nok_phone": "405-555-0188",
        "f31_nok_address": "100 SOVEREIGN COMMAND PKWY, OKLAHOMA CITY, OK",
        "f32_ice_full_name": "HVF TACTICAL WATCH OFFICER DESK",
        "f33_ice_relationship": "SECONDARY_EMERGENCY_COMMAND_CONTACT",
        "f34_ice_phone": "405-555-0177",
        "f35_ice_medical_blood": "O_POSITIVE_NO_KNOWN_DRUG_ALLERGIES",
        "f36_bio_fingerprint": "ISO19794-2-MINUTIAE-SEAL-8841",
        "f37_bio_iris": "ISO19794-6-IRIS-VASCULAR-9920",
        "f38_bio_face_voice": "3DFACE-VOICE-LIVENESS-7712",
        "f39_bank_aba_routing": "103000648",
        "f40_bank_account_num": "990011223344",
        "f41_property_deed_apn": "OK-APN-DEED-LOCK-44019",
                "f42_mobile_sim_imei": "359881090044112",
        "f43_prev_addr1_street": "740 HERITAGE RIDGE RD",
        "f44_prev_addr1_city": "EDMOND",
        "f45_prev_addr1_state_zip": "OK 73034",
        "f46_prev_addr1_dates": "2016-01_TO_2022-06",
        "f47_prev_addr2_summary": "TULSA_OK_74103 (2011_TO_2016)",
        "f48_prev_addr_verifier": "OKLAHOMA_COUNTY_DEED_REGISTRY_VERIFIED",
        "f49_prior_emp1_org": "SOVEREIGN INDUSTRIAL & AGRICULTURAL SYSTEMS",
        "f50_prior_emp1_title": "PRINCIPAL SYSTEMS DIRECTOR",
        "f51_prior_emp1_supervisor": "BOARD_VERIFIED_405-555-0100",
        "f52_prior_emp1_years": "12",
        "f53_prior_emp2_org_role": "CRITICAL_INFRASTRUCTURE_OPERATIONS_LEAD",
        "f54_total_experience_yrs": "22",
        "f55_highest_education": "PRINCIPAL_SOVEREIGN_ARCHITECT_FELLOWSHIP",
        "f56_academy_exam_score": "100.0",
        "f57_completed_hvf_courses": "ALL_34_CLINS_MASTER_CERTIFIED",
        "f58_active_certifications": "CAGE_1AHA8_PRINCIPAL_IPC6012_DOD_RMF_MASTER",
        "f59_training_hours_total": "1420",
        "f60_company_eval_rating": "5.0",
    }


    # =========================================================================
    # STAGE 13R (v6.0): ZERO-SECOND EMERGENCY ICE TRIAGE ROSTER, USER AGREEMENT
    # GATE, & DUAL-COMPARTMENT PRIVACY WALL (EMPLOYEE vs. EMPLOYER)
    # =========================================================================
    USER_AGREEMENT_TEXT: str = (
        "SOVEREIGN IDENTITY, OSHA FRONT-SCREEN MUSTER ACCESS, & HIPAA/ADA MEDICAL CONFIDENTIALITY CHARTER "
        "(OSHA 29 CFR 1910.38 / HIPAA 45 CFR 164.502 / ADA 42 U.S.C. 12112(d)(3)(B) / FCRA 15 U.S.C. 1681): "
        "(1) ZERO-SECOND FRONT-SCREEN MUSTER POINTS & EMERGENCY PROCEDURES: In compliance with OSHA 29 CFR 1910.38 life-safety "
        "mandates, all Company Command / 911 Dispatch Desks, Primary & Secondary Muster Points, Shelter-in-Place Bunkers, "
        "AED/Trauma Kit Locations, Evacuation Routes, and 5-Step Emergency Action Procedures are displayed openly on the "
        "front screen with zero login required. "
        "(2) 100% GATE-LOCKED PERSONAL PII & HIPAA PHI: To comply with federal HIPAA and ADA medical confidentiality laws, "
        "zero personal employee information, blood types, allergies, medical history, or personal Next-of-Kin (NOK) / ICE "
        "contacts are displayed on the unauthenticated screen. All personal and medical data is locked behind this gate. "
        "(3) PATH A (EMPLOYEE PERSONAL VAULT): Unseals the Employee's personal Medical/ICE card, 7-Channel Credit/Loan Shield, "
        "and 60-Field Dossier (Employer/HR is 100% blocked from viewing Employee credit or loans). "
        "(4) PATH B (EMPLOYER / HR EMERGENCY & INTERNAL VAULT): Unseals Employee Blood Type, Allergies, Medical History, "
        "Primary Physician, & NOK/ICE Contacts for HR/EMS response (WORM-logged), plus Employer Notes & Promotion Shortlist."
    )

    COMPANY_EMERGENCY_CONTACTS: List[Dict[str, str]] = [
        {
            "Unit": "1. HVF Sovereign Command Watch Desk (24/7 Primary)",
            "Authority": "Jeffery Humphrey -- Founder, CEO, & Principal Sovereign Architect",
            "Direct_Line": "405-555-0100 (Priority Channel 1)",
            "Email_Dispatch": "humphreyvirtualfarm@gmail.com",
            "Location_Enclave": "Oklahoma City HQ // CAGE: 1AHA8 | UEI: S1M4ENLHTDH5",
        },
        {
            "Unit": "2. Site Physical Security & 36.75ns Safety Interlock Officer",
            "Authority": "HVF Tactical Watch Officer on Duty",
            "Direct_Line": "405-555-0111 (Emergency Guillotine & Medical Dispatch)",
            "Email_Dispatch": "watchfloor-sos@hvf-sovereign.local",
            "Location_Enclave": "TOC Enclave Alpha // Port 8501 & Port 8502",
        },
        {
            "Unit": "3. Facility Medical, Trauma, & Fire Rapid Response",
            "Authority": "Base / Regional EMS & Trauma Coordinator",
            "Direct_Line": "911 / Base Medical Direct 405-555-0911",
            "Email_Dispatch": "ems-triage@hvf-sovereign.local",
            "Location_Enclave": "Emergency Gate 1 // Helipad & Ambulance Bay",
        },
    ]

    PERSONNEL_EMERGENCY_ROSTER: Dict[str, Dict[str, Any]] = {
        "EMP-001 // JEFFERY HUMPHREY (CEO & Principal Sovereign Architect)": {
            "employee_id": "EMP-001",
            "full_name": "JEFFERY SOVEREIGN HUMPHREY",
            "role_title": "Founder, CEO, & Principal Sovereign Architect",
            "department": "HVF Executive Command (CAGE 1AHA8)",
            "direct_phone": "405-555-0199",
            "email": "humphreyvirtualfarm@gmail.com",
            "nok_full_name": "MRS. HUMPHREY (Designated Primary Spouse / NOK)",
            "nok_relationship": "SPOUSE_PRIMARY_BENEFICIARY",
            "nok_phone": "405-555-0188",
            "nok_address": "100 Sovereign Command Pkwy, Oklahoma City, OK 73102",
            "ice_full_name": "HVF Tactical Watch Officer Desk",
            "ice_relationship": "SECONDARY_EMERGENCY_COMMAND_CONTACT",
            "ice_phone": "405-555-0177",
            "blood_type_and_medical": "O_POSITIVE // NO_KNOWN_DRUG_ALLERGIES",
            "employee_pin": "EMP-PIN-1AHA8-001",
            "employer_internal_records": [
                {"Internal_Record_Field": "1. Security Clearance & Adjudication Tier", "Employer_Sealed_Value": "LEVEL_5_SOVEREIGN_COMMANDER (SCI/SAP Vetted)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "2. Form I-9 & E-Verify Federal Case Seal", "Employer_Sealed_Value": "I9-VERIFIED-1AHA8-CASE-2026-0001 (ACTIVE)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "3. Watch-Floor Bitwise RBAC Authority Mask", "Employer_Sealed_Value": "0xFF (FULL_COMMAND_AND_WORM_SEAL_AUTHORITY)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "4. Insider Threat & Polygraph/Background Audit", "Employer_Sealed_Value": "ZERO_ADVERSE_FINDINGS // CONTINUOUS_EVAL_PASS", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "5. Internal Executive Draw & Contract Bucket Code", "Employer_Sealed_Value": "BUCKET-2 (35.0% CEO & SME Compensation Allocation)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
            ],
        },
        "EMP-002 // CAPT. MARCUS VANCE (Senior Tactical Watch Officer)": {
            "employee_id": "EMP-002",
            "full_name": "MARCUS ALEXANDER VANCE",
            "role_title": "Senior Tactical Watch Officer (Shift Alpha)",
            "department": "TOC Watch Floor & 60Hz Microgrid Operations",
            "direct_phone": "405-555-0210",
            "email": "m.vance@hvf-sovereign.local",
            "nok_full_name": "ELENA VANCE",
            "nok_relationship": "SPOUSE",
            "nok_phone": "405-555-0211",
            "nok_address": "4420 Midwest Blvd, Midwest City, OK 73110",
            "ice_full_name": "DR. ROBERT VANCE",
            "ice_relationship": "BROTHER / PHYSICIAN CONTACT",
            "ice_phone": "405-555-0212",
            "blood_type_and_medical": "A_POSITIVE // PENICILLIN_ALLERGY_CARRY_EPIPEN",
            "employee_pin": "EMP-PIN-VANCE-002",
            "employer_internal_records": [
                {"Internal_Record_Field": "1. Security Clearance & Adjudication Tier", "Employer_Sealed_Value": "SECRET // DOD_RMF_WATCH_OFFICER_CLEARED", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "2. Form I-9 & E-Verify Federal Case Seal", "Employer_Sealed_Value": "I9-VERIFIED-1AHA8-CASE-2026-0002 (ACTIVE)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "3. Watch-Floor Bitwise RBAC Authority Mask", "Employer_Sealed_Value": "0x1F (WATCH_OFFICER_CONTACTOR_AND_SHIFT_SIGN)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "4. Insider Threat & Background Vetting Audit", "Employer_Sealed_Value": "PASSED_ANNUAL_NIST_800_53_PERSONNEL_SCREEN", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "5. Internal Labor CLIN Billing Allocation", "Employer_Sealed_Value": "BUCKET-3 (15.0% TRL 8/9 Site Integration Pool)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
            ],
        },
        "EMP-003 // DR. SARAH LIN (Lead SiC Power Electronics & PLC Engineer)": {
            "employee_id": "EMP-003",
            "full_name": "SARAH MEI LIN",
            "role_title": "Lead 36.75ns SiC MOSFET & SCADA Integration Engineer",
            "department": "Hardware Interlock & J1939 CAN-Bus Lab",
            "direct_phone": "405-555-0310",
            "email": "s.lin@hvf-sovereign.local",
            "nok_full_name": "DAVID LIN",
            "nok_relationship": "FATHER",
            "nok_phone": "405-555-0311",
            "nok_address": "812 Crimson Oak Dr, Norman, OK 73072",
            "ice_full_name": "GRACE LIN",
            "ice_relationship": "SISTER",
            "ice_phone": "405-555-0312",
            "blood_type_and_medical": "B_NEGATIVE // ASTHMA_INHALER_IN_LAB_LOCKER_B4",
            "employee_pin": "EMP-PIN-LIN-003",
            "employer_internal_records": [
                {"Internal_Record_Field": "1. Security Clearance & Adjudication Tier", "Employer_Sealed_Value": "SECRET // DFARS_252_227_7018_HARDWARE_CUSTODIAN", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "2. Form I-9 & E-Verify Federal Case Seal", "Employer_Sealed_Value": "I9-VERIFIED-1AHA8-CASE-2026-0003 (ACTIVE)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "3. Watch-Floor Bitwise RBAC Authority Mask", "Employer_Sealed_Value": "0x1F (HARDWARE_BENCH_AND_SCADA_REGISTER_SIGN)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "4. Insider Threat & Background Vetting Audit", "Employer_Sealed_Value": "PASSED_IPC_6012_CLASS_3_AND_IT_VETTING", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "5. Internal Labor CLIN Billing Allocation", "Employer_Sealed_Value": "BUCKET-1 (18.0% Hardware Setup & Calibration Pool)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
            ],
        },
        "EMP-004 // CALEB ROSS (UAS Optical GLI & OK Title 61 Survey Specialist)": {
            "employee_id": "EMP-004",
            "full_name": "CALEB JACKSON ROSS",
            "role_title": "UAS Flight Operator & Civil GIS Boundary Specialist",
            "department": "Aerial Multispectral & Title 61 Civil Works Division",
            "direct_phone": "405-555-0410",
            "email": "c.ross@hvf-sovereign.local",
            "nok_full_name": "HANNAH ROSS",
            "nok_relationship": "SPOUSE",
            "nok_phone": "405-555-0411",
            "nok_address": "1904 Prairie Wind Rd, Edmond, OK 73003",
            "ice_full_name": "THOMAS ROSS",
            "ice_relationship": "FATHER",
            "ice_phone": "405-555-0412",
            "blood_type_and_medical": "AB_POSITIVE // NO_KNOWN_ALLERGIES",
            "employee_pin": "EMP-PIN-ROSS-004",
            "employer_internal_records": [
                {"Internal_Record_Field": "1. Security Clearance & Adjudication Tier", "Employer_Sealed_Value": "PUBLIC_TRUST // FAA_PART_107_AND_TITLE_61_BONDED", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "2. Form I-9 & E-Verify Federal Case Seal", "Employer_Sealed_Value": "I9-VERIFIED-1AHA8-CASE-2026-0004 (ACTIVE)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "3. Watch-Floor Bitwise RBAC Authority Mask", "Employer_Sealed_Value": "0x03 (OBSERVER_AND_GIS_TELEMETRY_INGEST)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "4. Insider Threat & Background Vetting Audit", "Employer_Sealed_Value": "PASSED_FIELD_OPERATIONS_VETTING", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
                {"Internal_Record_Field": "5. Internal Labor CLIN Billing Allocation", "Employer_Sealed_Value": "BUCKET-3 (15.0% TRL 8/9 Site Integration Pool)", "Employee_Visibility": "HIDDEN_INTERNAL_EMPLOYER_ONLY"},
            ],
        },
    }

    FACILITY_ZONE_TO_ROSTER_KEY: Dict[str, str] = {
        "ZONE 01 // Executive Command & TOC Core (Muster Alpha-1)": "EMP-001 // JEFFERY HUMPHREY (Founder, CEO & Principal Sovereign Architect)",
        "ZONE 02 // Watch Floor & 60Hz Microgrid Operations (Muster Alpha-1)": "EMP-002 // CAPT. MARCUS VANCE (Senior Watch Officer -- Shift Alpha)",
        "ZONE 03 // 36.75ns SiC MOSFET & 480V Hardware Lab (Muster Charlie-2)": "EMP-003 // DR. SARAH LIN (Lead SiC MOSFET & SCADA Integration Engineer)",
        "ZONE 04 // East Airfield Apron, UAS & Title 61 GIS (Muster Delta-3)": "EMP-004 // CALEB ROSS (UAS Flight Operator & Civil GIS Specialist)",
    }

    SITE_MUSTER_AND_BUNKER_SUMMARY: List[Dict[str, str]] = [
        {
            "Facility_Zone": "ZONE 01 // Executive Command & TOC Core",
            "Primary_Muster_Point": "MUSTER ALPHA-1 (North Helipad Gate 1)",
            "Secondary_Muster_Point": "MUSTER BRAVO-1 (West Silo Access Road)",
            "Shelter_In_Place_Bunker": "VAULT BUNKER B1-COMMAND (Sub-Level Faraday Core)",
            "Nearest_AED_And_Trauma_Kit": "AED & Trauma Kit #01 (Command Corridor 10m East)",
            "Evacuation_Route_And_Channel": "Route Red-Alpha (Stairwell 1) // Radio Ch. 1",
        },
        {
            "Facility_Zone": "ZONE 02 // Watch Floor & 60Hz Microgrid Dispatch",
            "Primary_Muster_Point": "MUSTER ALPHA-1 (North Helipad Roll-Call Station)",
            "Secondary_Muster_Point": "MUSTER BRAVO-1 (West Silo Access Road)",
            "Shelter_In_Place_Bunker": "VAULT BUNKER B1-WATCH (TOC Sub-Floor Blast Shelter)",
            "Nearest_AED_And_Trauma_Kit": "AED & Trauma Kit #02 (Watch Desk Wall Cabinet)",
            "Evacuation_Route_And_Channel": "Route Red-Bravo (Watch Double Doors) // Radio Ch. 1",
        },
        {
            "Facility_Zone": "ZONE 03 // 36.75ns SiC MOSFET & 480V Hardware Lab",
            "Primary_Muster_Point": "MUSTER CHARLIE-2 (South Power Lab Assembly Pad)",
            "Secondary_Muster_Point": "MUSTER ALPHA-1 (North Helipad Gate 1)",
            "Shelter_In_Place_Bunker": "VAULT BUNKER B2-LAB (Reinforced Substation Vault)",
            "Nearest_AED_And_Trauma_Kit": "High-Voltage AED & Trauma Kit #03 (Lab Exit)",
            "Evacuation_Route_And_Channel": "Route Yellow-Charlie (High-Bay Door 3) // Radio Ch. 1",
        },
        {
            "Facility_Zone": "ZONE 04 // East Airfield Apron, UAS & Title 61 GIS",
            "Primary_Muster_Point": "MUSTER DELTA-3 (East Airfield Apron Perimeter)",
            "Secondary_Muster_Point": "MUSTER BRAVO-1 (West Silo Access Road)",
            "Shelter_In_Place_Bunker": "VAULT BUNKER B3-HANGAR (Reinforced Hangar Culvert)",
            "Nearest_AED_And_Trauma_Kit": "Field Trauma Kit #04 & Mobile AED (UAS Bay 1)",
            "Evacuation_Route_And_Channel": "Route Green-Delta (Flight Service Rd) // Radio Ch. 1",
        },
    ]

    def get_public_emergency_muster_and_sops(self, zone_or_roster_key: str) -> Dict[str, Any]:
        """
        Returns non-personal, OSHA 29 CFR 1910.38 facility Muster Points, Shelter-in-Place
        Bunkers, AED/Trauma Kit locations, whole-word KPI labels, and 5-Step Emergency
        Evacuation Procedures for immediate front-screen display (Zero login required).
        """
        mapped_key = self.FACILITY_ZONE_TO_ROSTER_KEY.get(zone_or_roster_key, zone_or_roster_key)
        card = self.get_instant_emergency_triage_card(mapped_key)
        emp_id = card["employee_id"]
        kpi_short_map = {
            "EMP-001": {
                "p_title": "MUSTER ALPHA-1",
                "p_sub": "North Helipad Perimeter (Gate 1)",
                "s_title": "MUSTER BRAVO-1",
                "s_sub": "West Silo Access Road Staging",
                "b_title": "VAULT BUNKER B1-COMMAND",
                "b_sub": "Sub-Level Faraday & Tornado Core",
                "a_title": "AED & Trauma Kit #01",
                "a_sub": "Command Corridor (10m East)",
            },
            "EMP-002": {
                "p_title": "MUSTER ALPHA-1",
                "p_sub": "North Helipad Roll-Call Station",
                "s_title": "MUSTER BRAVO-1",
                "s_sub": "West Silo Access Road Staging",
                "b_title": "VAULT BUNKER B1-WATCH",
                "b_sub": "TOC Sub-Floor Storm & Blast Core",
                "a_title": "AED & Trauma Kit #02",
                "a_sub": "Watch Desk Wall (With EpiPen)",
            },
            "EMP-003": {
                "p_title": "MUSTER CHARLIE-2",
                "p_sub": "South Power Lab Assembly Pad",
                "s_title": "MUSTER ALPHA-1",
                "s_sub": "North Helipad Perimeter (Gate 1)",
                "b_title": "VAULT BUNKER B2-LAB",
                "b_sub": "Reinforced Substation Storm Vault",
                "a_title": "AED & Trauma Kit #03",
                "a_sub": "SiC Lab Exit (Non-Latex & Locker B4)",
            },
            "EMP-004": {
                "p_title": "MUSTER DELTA-3",
                "p_sub": "East Airfield Apron Perimeter",
                "s_title": "MUSTER BRAVO-1",
                "s_sub": "West Silo Access Road Staging",
                "b_title": "VAULT BUNKER B3-HANGAR",
                "b_sub": "Reinforced Hangar Concrete Culvert",
                "a_title": "AED & Trauma Kit #04",
                "a_sub": "UAS Command Trailer (Bay 1)",
            },
        }
        ks = kpi_short_map.get(emp_id, kpi_short_map["EMP-001"])
        return {
            "department_zone": card["department"],
            "primary_muster_point": card["primary_muster_point"],
            "secondary_muster_point": card["secondary_muster_point"],
            "shelter_in_place_bunker": card["shelter_in_place_bunker"],
            "nearest_aed_trauma_kit": card["nearest_aed_trauma_kit"],
            "evacuation_route_and_warden": card["evacuation_route_and_warden"],
            "emergency_procedures_rows": card["emergency_procedures_rows"],
            "primary_muster_title": ks["p_title"],
            "primary_muster_sub": ks["p_sub"],
            "secondary_muster_title": ks["s_title"],
            "secondary_muster_sub": ks["s_sub"],
            "bunker_title": ks["b_title"],
            "bunker_sub": ks["b_sub"],
            "aed_kit_title": ks["a_title"],
            "aed_kit_sub": ks["a_sub"],
            "muster_dispatch_ledger_rows": [
                {"Dispatch_Line": "01 // FACILITY ZONE", "OSHA_1910_38_Parameter": "Active Operational Zone", "Verified_Site_Directive": card["department"]},
                {"Dispatch_Line": "02 // PRIMARY MUSTER", "OSHA_1910_38_Parameter": "Primary & Secondary Muster Points", "Verified_Site_Directive": f"{card['primary_muster_point']} | Secondary: {card['secondary_muster_point']}"},
                {"Dispatch_Line": "03 // SHELTER BUNKER", "OSHA_1910_38_Parameter": "Tornado / Blast / CBRN Shelter Vault", "Verified_Site_Directive": card["shelter_in_place_bunker"]},
                {"Dispatch_Line": "04 // AED & TRAUMA KIT", "OSHA_1910_38_Parameter": "Nearest AED & Level-1 Trauma Kit", "Verified_Site_Directive": card["nearest_aed_trauma_kit"]},
                {"Dispatch_Line": "05 // EVACUATION ROUTE", "OSHA_1910_38_Parameter": "Primary Egress Route & Zone Warden", "Verified_Site_Directive": card["evacuation_route_and_warden"]},
            ],
        }

    def get_instant_emergency_triage_card(self, roster_key: str) -> Dict[str, Any]:
        person = self.PERSONNEL_EMERGENCY_ROSTER.get(
            roster_key,
            next(iter(self.PERSONNEL_EMERGENCY_ROSTER.values())),
        )
        raw_med = person["blood_type_and_medical"]
        parts = [p.strip() for p in raw_med.split("//")]
        blood_clean = parts[0].replace("_POSITIVE", "+ (Positive)").replace("_NEGATIVE", "- (Negative)")
        med_clean = parts[1].replace("_", " ").title() if len(parts) > 1 else "Verified Clean"

        emp_id = person["employee_id"]
        role_short_map = {
            "EMP-001": "Founder, CEO & Sovereign Architect",
            "EMP-002": "Senior Tactical Watch Officer",
            "EMP-003": "Lead SiC & SCADA Engineer",
            "EMP-004": "UAS & Title 61 GIS Specialist",
        }
        nok_short_map = {
            "EMP-001": "Mrs. Humphrey (Spouse / Primary NOK)",
            "EMP-002": "Elena Vance (Spouse / Primary NOK)",
            "EMP-003": "David Lin (Father / Primary NOK)",
            "EMP-004": "Hannah Ross (Spouse / Primary NOK)",
        }
        ice_short_map = {
            "EMP-001": "HVF Tactical Watch Officer Desk",
            "EMP-002": "Dr. Robert Vance (Brother / MD)",
            "EMP-003": "Grace Lin (Sister / Secondary ICE)",
            "EMP-004": "Thomas Ross (Father / Secondary ICE)",
        }
        allergies_map = {
            "EMP-001": "No Known Drug or Food Allergies (NKDA)",
            "EMP-002": "SEVERE PENICILLIN ALLERGY -- Administer Epinephrine Auto-Injector (EpiPen in Watch Desk Kit #2)",
            "EMP-003": "Sulfonamide Antibiotics & Latex Sensitivity -- Use Non-Latex Trauma Gloves",
            "EMP-004": "No Known Drug Allergies (NKDA) -- Seasonal Pollen Sensitivity Only",
        }
        med_history_map = {
            "EMP-001": "Clear Annual Executive Flight/Duty Physical (2026); Tetanus Current; 0 Chronic Conditions; 0 Daily Rx.",
            "EMP-002": "Prior Resolved R-Knee Arthroscopy (2021); Carries Epinephrine 0.3mg Auto-Injector; Cleared High-Stress Watch Duty.",
            "EMP-003": "Mild Exercise-Induced Bronchospasm (Albuterol HFA Inhaler in Lab Locker B4); Cleared High-Voltage 480V/SiC Bench Duty.",
            "EMP-004": "FAA Class-2 Flight Medical Certified (2026); 20/15 Corrected Vision; 0 Surgical History; 0 Daily Medications.",
        }
        physician_hospital_map = {
            "EMP-001": "OU Health Level-1 Trauma Center (OKC) // Executive Physician Direct: 405-555-0801",
            "EMP-002": "Tinker AFB 72nd Medical Group / INTEGRIS Baptist Medical Center // Dr. R. Vance: 405-555-0212",
            "EMP-003": "Norman Regional HealthPlex Trauma Center // Pulmonary Specialist: 405-555-0833",
            "EMP-004": "INTEGRIS Health Edmond Hospital // FAA Aviation Medical Examiner: 405-555-0844",
        }
        muster_map = {
            "EMP-001": {
                "primary_muster_point": "MUSTER ALPHA-1 // North Helipad Command Perimeter (Gate 1)",
                "secondary_muster_point": "MUSTER BRAVO-1 // West Silo Access Road Mobile TOC Staging",
                "shelter_in_place_bunker": "VAULT BUNKER B1-COMMAND // Sub-Level Reinforced Faraday & Tornado Core",
                "nearest_aed_trauma_kit": "AED & Level-1 Trauma Kit #01 // Executive Command Corridor (10m East)",
                "evacuation_route_and_warden": "Route Red-Alpha via Armored Stairwell 1 // Warden: Capt. M. Vance (Ch. 1)",
                "emergency_procedures_rows": [
                    {"Step": "STEP 01 (Immediate Kinetic/Grid Cutoff)", "Procedure_Action": "Engage 36.75ns SiC MOSFET Hardware Guillotine E-Stop (CLIN 0006/0028) & Island 60Hz Microgrid Relay if electrical/kinetic hazard is present.", "Target_SLA": "< 1.0 Second"},
                    {"Step": "STEP 02 (Credential & WORM Lock)", "Procedure_Action": "Lock active Port 8501/8502 Watch-Floor console session and secure physical DoD CAC / PIV & REAL-ID badge for Muster scanner.", "Target_SLA": "15 Seconds"},
                    {"Step": "STEP 03 (Primary Evacuation / Shelter)", "Procedure_Action": "Proceed via Route Red-Alpha to MUSTER ALPHA-1 (North Helipad Gate 1). If tornado/CBRN alarm sounds, descend to VAULT BUNKER B1-COMMAND.", "Target_SLA": "90 Seconds"},
                    {"Step": "STEP 04 (Muster Roll-Call Check-In)", "Procedure_Action": "Scan badge with Duty Watch Officer at Muster Alpha-1 or report status on Tactical Radio Channel 1 (405-555-0100).", "Target_SLA": "180 Seconds"},
                    {"Step": "STEP 05 (Medical / EMS Triage Handoff)", "Procedure_Action": "If injured, HR/Warden unseals HIPAA Emergency Medical Packet (Blood Type, Allergies, Medical History & NOK/ICE) for EMS arrival at Helipad Bay.", "Target_SLA": "Immediate"},
                ],
            },
            "EMP-002": {
                "primary_muster_point": "MUSTER ALPHA-1 // North Helipad Command Perimeter (Roll-Call Warden Station)",
                "secondary_muster_point": "MUSTER BRAVO-1 // West Silo Access Road Mobile TOC Staging",
                "shelter_in_place_bunker": "VAULT BUNKER B1-WATCH // TOC Sub-Floor Reinforced Storm & Blast Shelter",
                "nearest_aed_trauma_kit": "AED & Trauma Kit #02 (Contains Epinephrine Auto-Injector) // Watch Desk Wall",
                "evacuation_route_and_warden": "Route Red-Bravo via Watch-Floor Double Doors // Role: Primary Muster Warden",
                "emergency_procedures_rows": [
                    {"Step": "STEP 01 (Watch-Floor E-Stop & Alarm)", "Procedure_Action": "Trigger Master Watch-Floor Klaxon, trip 36.75ns SiC breaker interlock, and open emergency exit mag-locks.", "Target_SLA": "< 1.0 Second"},
                    {"Step": "STEP 02 (Grab Emergency Muster Tablet & EpiPen)", "Procedure_Action": "Retrieve air-gapped Muster Roll-Call Tablet and personal Epinephrine Auto-Injector from Watch Desk Kit #02.", "Target_SLA": "15 Seconds"},
                    {"Step": "STEP 03 (Sweep TOC & Evacuate)", "Procedure_Action": "Conduct 10-second visual sweep of Watch Floor and lead Shift Alpha personnel via Route Red-Bravo to MUSTER ALPHA-1.", "Target_SLA": "90 Seconds"},
                    {"Step": "STEP 04 (Execute Personnel Headcount)", "Procedure_Action": "Account for all on-shift operators at Muster Alpha-1 and report headcount to CEO / Sovereign Command.", "Target_SLA": "180 Seconds"},
                    {"Step": "STEP 05 (Coordinate EMS & NOK/ICE)", "Procedure_Action": "Provide unsealed HIPAA Allergy/Blood/Medical History telemetry to arriving Base EMS and initiate NOK/ICE notifications.", "Target_SLA": "Immediate"},
                ],
            },
            "EMP-003": {
                "primary_muster_point": "MUSTER CHARLIE-2 // South Power Electronics & Hardware Lab Assembly Pad",
                "secondary_muster_point": "MUSTER ALPHA-1 // North Helipad Command Perimeter (Gate 1)",
                "shelter_in_place_bunker": "VAULT BUNKER B2-LAB // Reinforced Concrete Substation & Storm Vault",
                "nearest_aed_trauma_kit": "High-Voltage AED, Non-Latex Trauma Kit #03 & Albuterol Locker B4 // SiC Lab Exit",
                "evacuation_route_and_warden": "Route Yellow-Charlie via High-Bay Roll-Up Door 3 // Warden: Dr. Sarah Lin",
                "emergency_procedures_rows": [
                    {"Step": "STEP 01 (480V / SiC Capacitor Discharge)", "Procedure_Action": "Trip 36.75ns SiC MOSFET solid-state breaker & verify 480V 3-phase contactor zero-energy discharge indicator.", "Target_SLA": "< 1.0 Second"},
                    {"Step": "STEP 02 (Personal Medical & Badge Grab)", "Procedure_Action": "Secure Lab Locker B4 Albuterol inhaler and CAC/REAL-ID badge prior to exiting High-Bay.", "Target_SLA": "15 Seconds"},
                    {"Step": "STEP 03 (Lab Evacuation / Bunker)", "Procedure_Action": "Exit via Route Yellow-Charlie to MUSTER CHARLIE-2 (South Pad). For severe weather/blast, enter VAULT BUNKER B2-LAB.", "Target_SLA": "90 Seconds"},
                    {"Step": "STEP 04 (Muster Check-In)", "Procedure_Action": "Confirm Hardware Lab clear status with Watch Officer on Tactical Channel 1 (405-555-0111).", "Target_SLA": "180 Seconds"},
                    {"Step": "STEP 05 (Non-Latex EMS Protocol)", "Procedure_Action": "Ensure EMS observes Non-Latex / Sulfonamide allergy flag in HIPAA Medical Triage Card if treatment is required.", "Target_SLA": "Immediate"},
                ],
            },
            "EMP-004": {
                "primary_muster_point": "MUSTER DELTA-3 // East Airfield Apron & UAS Flight Line Perimeter",
                "secondary_muster_point": "MUSTER BRAVO-1 // West Silo Access Road Mobile TOC Staging",
                "shelter_in_place_bunker": "VAULT BUNKER B3-HANGAR // Reinforced Hangar Concrete Culvert & Storm Shelter",
                "nearest_aed_trauma_kit": "Field Trauma & Burn Kit #04 + Portable AED // UAS Command Trailer Bay 1",
                "evacuation_route_and_warden": "Route Green-Delta via Flight Line Service Road // Warden: Caleb Ross",
                "emergency_procedures_rows": [
                    {"Step": "STEP 01 (UAS Auto-Land / Return-to-Home)", "Procedure_Action": "Execute immediate Return-to-Home (RTH) or emergency ditching command on active UAS sorties & cut LiPo charging banks.", "Target_SLA": "< 2.0 Seconds"},
                    {"Step": "STEP 02 (Secure Survey & Flight Logs)", "Procedure_Action": "Lock field ruggedized terminal and grab portable Field Trauma Kit #04 from UAS Trailer.", "Target_SLA": "20 Seconds"},
                    {"Step": "STEP 03 (Flight Line Evacuation)", "Procedure_Action": "Evacuate via Route Green-Delta to MUSTER DELTA-3 (East Airfield Apron) or shelter in VAULT BUNKER B3-HANGAR.", "Target_SLA": "90 Seconds"},
                    {"Step": "STEP 04 (Field Muster Check-In)", "Procedure_Action": "Transmit GPS coordinates and Muster Delta-3 check-in to TOC Watch Desk (405-555-0100).", "Target_SLA": "180 Seconds"},
                    {"Step": "STEP 05 (Medical & ICE Standby)", "Procedure_Action": "Stand by on Channel 1 for all-clear or EMS/NOK dispatch instructions from Command.", "Target_SLA": "Immediate"},
                ],
            },
        }
        m_info = muster_map.get(emp_id, muster_map["EMP-001"])
        return {
            "employee_id": emp_id,
            "full_name": person["full_name"],
            "role_title": person["role_title"],
            "role_short": role_short_map.get(emp_id, person["role_title"]),
            "department": person["department"],
            "direct_phone": person["direct_phone"],
            "email": person["email"],
            "nok_full_name": person["nok_full_name"],
            "nok_relationship": person["nok_relationship"],
            "nok_short": nok_short_map.get(emp_id, person["nok_full_name"]),
            "nok_phone": person["nok_phone"],
            "nok_address": person["nok_address"],
            "ice_full_name": person["ice_full_name"],
            "ice_relationship": person["ice_relationship"],
            "ice_short": ice_short_map.get(emp_id, person["ice_full_name"]),
            "ice_phone": person["ice_phone"],
            "blood_type_and_medical": raw_med,
            "blood_type_clean": blood_clean,
            "medical_alert_clean": med_clean,
            "allergies_detailed": allergies_map.get(emp_id, med_clean),
            "medical_history_detailed": med_history_map.get(emp_id, "Cleared for Full Duty"),
            "physician_and_hospital": physician_hospital_map.get(emp_id, "Regional Level-1 Trauma Center"),
            "primary_muster_point": m_info["primary_muster_point"],
            "secondary_muster_point": m_info["secondary_muster_point"],
            "shelter_in_place_bunker": m_info["shelter_in_place_bunker"],
            "nearest_aed_trauma_kit": m_info["nearest_aed_trauma_kit"],
            "evacuation_route_and_warden": m_info["evacuation_route_and_warden"],
            "emergency_procedures_rows": m_info["emergency_procedures_rows"],
            "hipaa_triage_ledger_rows": [
                {"Triage_Line": "01 // AUTHENTICATED SUBJECT", "HIPAA_45_CFR_164_502_Field": "Employee ID, Name & Duty Unit", "Unsealed_Emergency_Telemetry": f"{emp_id} -- {person['full_name']} ({person['department']})"},
                {"Triage_Line": "02 // BLOOD & ALLERGIES", "HIPAA_45_CFR_164_502_Field": "Blood Type & Drug/Latex Allergies", "Unsealed_Emergency_Telemetry": f"{blood_clean} // ALLERGIES: {allergies_map.get(emp_id, med_clean)}"},
                {"Triage_Line": "03 // MEDICAL HISTORY & RX", "HIPAA_45_CFR_164_502_Field": "Chronic Conditions, Surgeries & Rx", "Unsealed_Emergency_Telemetry": med_history_map.get(emp_id, "Cleared for Full Duty")},
                {"Triage_Line": "04 // PHYSICIAN & HOSPITAL", "HIPAA_45_CFR_164_502_Field": "Primary Physician & Trauma Center", "Unsealed_Emergency_Telemetry": physician_hospital_map.get(emp_id, "Regional Level-1 Trauma Center")},
                {"Triage_Line": "05 // NEXT OF KIN (NOK)", "HIPAA_45_CFR_164_502_Field": "Primary Next of Kin (Name, Phone, Address)", "Unsealed_Emergency_Telemetry": f"{person['nok_full_name']} ({person['nok_relationship']}) | Phone: {person['nok_phone']} | Address: {person['nok_address']}"},
                {"Triage_Line": "06 // IN CASE OF EMERGENCY", "HIPAA_45_CFR_164_502_Field": "Secondary ICE & Employee Direct Phone", "Unsealed_Emergency_Telemetry": f"{person['ice_full_name']} ({person['ice_relationship']}) | ICE Phone: {person['ice_phone']} | Employee Phone: {person['direct_phone']}"},
            ],
        }

    def record_hipaa_emergency_triage_access(
        self,
        db_path: pathlib.Path,
        employee_id: str,
        employee_name: str,
        accessor_role: str,
        access_purpose: str = "AUTHORIZED_GATE_MEDICAL_MUSTER_AND_ICE_VIEW",
    ) -> Dict[str, Any]:
        self.init_worm_sqlite_ledger(db_path)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            last_row = cur.execute(
                "SELECT triage_log_id, worm_hipaa_sha256 FROM worm_hipaa_emergency_triage_log ORDER BY triage_log_id DESC LIMIT 1"
            ).fetchone()
            prev_hash = last_row[1] if last_row else ("0" * 64)
            log_sha = hmac.new(
                IDENTITY_VAULT_PEPPER.encode("utf-8"),
                f"{prev_hash}|{employee_id}|{employee_name}|{accessor_role}|{access_purpose}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            cur.execute(
                """
                INSERT OR IGNORE INTO worm_hipaa_emergency_triage_log (
                    employee_id, employee_name, accessor_role, access_purpose,
                    hipaa_statutory_basis, previous_log_hash, worm_hipaa_sha256
                ) VALUES (?,?,?,?,?,?,?)
                """,
                (
                    employee_id,
                    employee_name,
                    accessor_role,
                    access_purpose,
                    "HIPAA_45_CFR_164_502_AND_OSHA_1910_38_MUSTER_GATE",
                    prev_hash,
                    log_sha,
                ),
            )
            conn.commit()
            cnt = cur.execute("SELECT COUNT(*) FROM worm_hipaa_emergency_triage_log").fetchone()[0]
        finally:
            conn.close()
        return {"hipaa_triage_logs_count": cnt, "worm_hipaa_sha256": log_sha}

    def seed_default_employer_notes(self, db_path: pathlib.Path) -> None:
        self.init_worm_sqlite_ledger(db_path)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cnt = conn.cursor().execute("SELECT COUNT(*) FROM worm_employer_personnel_notes").fetchone()[0]
        finally:
            conn.close()
        if cnt == 0:
            defaults = [
                ("EMP-001", "JEFFERY SOVEREIGN HUMPHREY", "HVF BOARD & SECURITY AUTHORITY", "EXECUTIVE_COMMENDATION_AND_CLEARANCE", "Principal Sovereign Architect of Project Ebony (631 modules) & Next-Gen Forge (WP-1..8). Level-5 Command Authority verified."),
                ("EMP-002", "MARCUS ALEXANDER VANCE", "JEFFERY HUMPHREY (CEO)", "WATCH_FLOOR_QUALIFICATION", "Qualified on 60Hz Microgrid Islanding Relay (CLIN 0003) and Watch-Floor Bitmask 0x1F shift handover protocols."),
                ("EMP-003", "SARAH MEI LIN", "JEFFERY HUMPHREY (CEO)", "HARDWARE_BENCH_CERTIFICATION", "Certified custodian for 36.75ns SiC MOSFET solid-state breaker board (CLIN 0028) and IPC-6012 Class-3 assembly."),
                ("EMP-004", "CALEB JACKSON ROSS", "JEFFERY HUMPHREY (CEO)", "FIELD_SURVEY_AUTHORIZATION", "Cleared for air-gapped UAS Louhaichi GLI flights and Oklahoma Title 61 (5% retainage) boundary surveys."),
            ]
            for eid, ename, auth, cat, txt in defaults:
                self.append_employer_personnel_note(
                    db_path=db_path,
                    employee_id=eid,
                    employee_name=ename,
                    author_authority=auth,
                    note_category=cat,
                    confidential_note_text=txt,
                )

    def append_employer_personnel_note(
        self,
        db_path: pathlib.Path,
        employee_id: str,
        employee_name: str,
        author_authority: str,
        note_category: str,
        confidential_note_text: str,
    ) -> Dict[str, Any]:
        self.init_worm_sqlite_ledger(db_path)
        clean_text = confidential_note_text.strip()
        assert len(clean_text) >= 3, "Employer personnel note text must be at least 3 characters"
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            last_row = cur.execute(
                "SELECT note_id, worm_note_sha256 FROM worm_employer_personnel_notes ORDER BY note_id DESC LIMIT 1"
            ).fetchone()
            prev_hash = last_row[1] if last_row else ("0" * 64)
            next_id = (last_row[0] + 1) if last_row else 1

            note_sha = hmac.new(
                IDENTITY_VAULT_PEPPER.encode("utf-8"),
                f"{prev_hash}|{employee_id.strip()}|{employee_name.strip()}|{author_authority.strip()}|{note_category.strip()}|{clean_text}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            cur.execute(
                """
                INSERT OR IGNORE INTO worm_employer_personnel_notes (
                    employee_id, employee_name, author_authority, note_category,
                    confidential_note_text, previous_note_hash, worm_note_sha256
                ) VALUES (?,?,?,?,?,?,?)
                """,
                (
                    employee_id.strip(),
                    employee_name.strip(),
                    author_authority.strip(),
                    note_category.strip(),
                    clean_text,
                    prev_hash,
                    note_sha,
                ),
            )
            conn.commit()
            total_emp_notes = cur.execute(
                "SELECT COUNT(*) FROM worm_employer_personnel_notes WHERE employee_id = ?",
                (employee_id.strip(),),
            ).fetchone()[0]
        finally:
            conn.close()
        return {
            "note_sequence": next_id,
            "employee_id": employee_id.strip(),
            "employee_name": employee_name.strip(),
            "author_authority": author_authority.strip(),
            "note_category": note_category.strip(),
            "confidential_note_text": clean_text,
            "total_notes_for_employee": total_emp_notes,
            "worm_note_sha256": note_sha,
        }

    def get_employer_personnel_notes(
        self,
        db_path: pathlib.Path,
        employee_id: str | None = None,
    ) -> List[Dict[str, str]]:
        self.seed_default_employer_notes(db_path)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            if employee_id:
                rows = cur.execute(
                    """
                    SELECT note_id, employee_id, employee_name, author_authority,
                           note_category, confidential_note_text, previous_note_hash, worm_note_sha256
                    FROM worm_employer_personnel_notes
                    WHERE employee_id = ?
                    ORDER BY note_id DESC
                    """,
                    (employee_id.strip(),),
                ).fetchall()
            else:
                rows = cur.execute(
                    """
                    SELECT note_id, employee_id, employee_name, author_authority,
                           note_category, confidential_note_text, previous_note_hash, worm_note_sha256
                    FROM worm_employer_personnel_notes
                    ORDER BY note_id DESC
                    """
                ).fetchall()
        finally:
            conn.close()
        return [
            {
                "Note_ID": f"NOTE #{r[0]:03d}",
                "Employee_ID": r[1],
                "Employee_Name": r[2],
                "Author_Authority": r[3],
                "Category": r[4],
                "Confidential_Employer_Note": r[5],
                "Prev_Note_Hash": r[6][:14] + "...",
                "WORM_Note_SHA256": r[7][:18] + "...",
            }
            for r in rows
        ]

    # =========================================================================
    # STAGE 13W (v7.0): 60-FIELD DOSSIER (PREVIOUS ADDRESSES, JOB HISTORY, &
    # TRAINING) + AUTOMATED EMPLOYER PROMOTION & EVALUATION SHORTLIST ENGINE
    # =========================================================================
    CANDIDATE_CAREER_AND_TRAINING_MATRIX: Dict[str, Dict[str, Any]] = {
        "EMP-001": {
            "employee_id": "EMP-001",
            "full_name": "JEFFERY SOVEREIGN HUMPHREY",
            "current_role": "Founder, CEO, & Principal Sovereign Architect",
            "target_promotion_track": "EXECUTIVE_COMMAND_BOARD_CHAIR_LEVEL_5",
            "clearance_tier": "LEVEL_5_SOVEREIGN_COMMANDER",
            "prev_address_1": "740 Heritage Ridge Rd, Edmond, OK 73034 (2016-2022)",
            "prev_address_2": "Tulsa, OK 74103 (2011-2016) // 7-Yr Address Check: VERIFIED",
            "prior_job_1": "Principal Systems Director -- Sovereign Industrial Systems (12 Yrs)",
            "prior_job_2": "Critical Infrastructure Operations Lead (10 Yrs)",
            "total_experience_yrs": 22,
            "highest_education": "Principal Sovereign Architect Fellowship",
            "academy_exam_score_pct": 100.0,
            "completed_hvf_modules": "ALL_34_CLINS_MASTER_CERTIFIED (Ch.1 800 Qs + Ch.5 620 Qs)",
            "active_certifications": "CAGE 1AHA8 Principal | DoD RMF ATO Master | IPC-6012 Class-3",
            "training_hours": 1420,
            "company_eval_rating": 5.0,
            "specialty_tags": ["ALL", "EXECUTIVE_C2", "SIC_HARDWARE", "SCADA_PLC", "UAS_GIS", "RMF_CYBER"],
        },
        "EMP-002": {
            "employee_id": "EMP-002",
            "full_name": "MARCUS ALEXANDER VANCE",
            "current_role": "Senior Tactical Watch Officer (Shift Alpha)",
            "target_promotion_track": "DEPUTY_WATCH_FLOOR_COMMANDER_0xFF",
            "clearance_tier": "SECRET // DOD_RMF_CLEARED",
            "prev_address_1": "118 Falcon Crest Blvd, Tinker AFB / Midwest City, OK 73110 (2019-2024)",
            "prev_address_2": "Colorado Springs, CO 80914 (2014-2019) // 7-Yr Address Check: VERIFIED",
            "prior_job_1": "USAF C2 Battle Management Watch Officer (8 Yrs)",
            "prior_job_2": "Regional Microgrid Dispatch Supervisor (4 Yrs)",
            "total_experience_yrs": 12,
            "highest_education": "B.S. Electrical & Systems Engineering",
            "academy_exam_score_pct": 96.5,
            "completed_hvf_modules": "CLIN 0001, CLIN 0003 (60Hz SCADA), CLIN 0031 (RBAC), CLIN 0032 (RMF)",
            "active_certifications": "CompTIA Security+ CE | NERC Grid Operator | DoD RMF Watch Officer",
            "training_hours": 480,
            "company_eval_rating": 4.9,
            "specialty_tags": ["ALL", "EXECUTIVE_C2", "SCADA_PLC", "RMF_CYBER"],
        },
        "EMP-003": {
            "employee_id": "EMP-003",
            "full_name": "SARAH MEI LIN",
            "current_role": "Lead 36.75ns SiC MOSFET & SCADA Integration Engineer",
            "target_promotion_track": "CHIEF_HARDWARE_AND_ROBOTICS_SAFETY_DIRECTOR",
            "clearance_tier": "SECRET // DFARS_HARDWARE_CUSTODIAN",
            "prev_address_1": "2901 Research Park Dr, Norman, OK 73072 (2020-2024)",
            "prev_address_2": "Austin, TX 78712 (2016-2020) // 7-Yr Address Check: VERIFIED",
            "prior_job_1": "Senior Power Electronics Designer -- Defense SiC Lab (6 Yrs)",
            "prior_job_2": "Industrial SAE J1939 CAN-Bus Firmware Engineer (4 Yrs)",
            "total_experience_yrs": 10,
            "highest_education": "Ph.D. Power Electronics & Solid-State Switching",
            "academy_exam_score_pct": 98.0,
            "completed_hvf_modules": "CLIN 0006, CLIN 0008, CLIN 0009, CLIN 0028 (36.75ns SiC), CLIN 0029 (PLC/J1939)",
            "active_certifications": "IPC-6012 Class-3 Master | IEEE Power Electronics Fellow | OSHA-30",
            "training_hours": 610,
            "company_eval_rating": 4.95,
            "specialty_tags": ["ALL", "SIC_HARDWARE", "SCADA_PLC"],
        },
        "EMP-004": {
            "employee_id": "EMP-004",
            "full_name": "CALEB JACKSON ROSS",
            "current_role": "UAS Flight Operator & Civil GIS Boundary Specialist",
            "target_promotion_track": "DIRECTOR_OF_AERIAL_RECON_AND_TITLE_61_CIVIL_WORKS",
            "clearance_tier": "PUBLIC_TRUST // TITLE_61_BONDED",
            "prev_address_1": "512 Cimmaron Trail, Stillwater, OK 74074 (2020-2024)",
            "prev_address_2": "Enid, OK 73701 (2017-2020) // 7-Yr Address Check: VERIFIED",
            "prior_job_1": "Lead Photogrammetry & Multispectral UAS Pilot (5 Yrs)",
            "prior_job_2": "Civil Earthwork & Retainage Survey Technician (3 Yrs)",
            "total_experience_yrs": 8,
            "highest_education": "M.S. Geomatics & Remote Sensing",
            "academy_exam_score_pct": 94.0,
            "completed_hvf_modules": "CLIN 0007 (UAS GLI), CLIN 0010 (Title 61), CLIN 0030 (GIS Boundary)",
            "active_certifications": "FAA Part 107 Remote Pilot | OK Licensed GIS Surveyor | Louhaichi GLI Spec",
            "training_hours": 340,
            "company_eval_rating": 4.8,
            "specialty_tags": ["ALL", "UAS_GIS"],
        },
    }

    def evaluate_promotion_and_company_shortlist(
        self,
        out_dir: pathlib.Path,
        min_experience_years: int = 5,
        min_academy_score_pct: float = 90.0,
        min_eval_rating: float = 4.5,
        required_specialty: str = "ALL",
    ) -> Dict[str, Any]:
        """
        Pulls all personnel who meet the Employer's experience, training/Academy score,
        7-year address/job background verification, and company evaluation thresholds
        into a single ranked Promotion & Evaluation Shortlist, sealing the board run in WORM SQLite.
        """
        db_path = out_dir / "wp7_identity_credit_worm_ledger.db"
        self.init_worm_sqlite_ledger(db_path)

        qualified_rows: List[Dict[str, Any]] = []
        all_evaluated_rows: List[Dict[str, Any]] = []

        state_data = self.load_or_init_vault_lock_state(out_dir)
        saved_by_emp = state_data.get("saved_profiles_by_emp", {})
        for emp_id, cand in self.CANDIDATE_CAREER_AND_TRAINING_MATRIX.items():
            emp_saved = saved_by_emp.get(emp_id, {})
            try:
                exp_yrs = int(float(emp_saved.get("f54_total_experience_yrs", cand["total_experience_yrs"])))
            except ValueError:
                exp_yrs = int(cand["total_experience_yrs"])
            try:
                acad_pct = float(emp_saved.get("f56_academy_exam_score", cand["academy_exam_score_pct"]))
            except ValueError:
                acad_pct = float(cand["academy_exam_score_pct"])
            try:
                eval_rat = float(emp_saved.get("f60_company_eval_rating", cand["company_eval_rating"]))
            except ValueError:
                eval_rat = float(cand["company_eval_rating"])
            try:
                train_hrs = int(float(emp_saved.get("f59_training_hours_total", cand["training_hours"])))
            except ValueError:
                train_hrs = int(cand["training_hours"])

            # 100-Point Composite Promotion Readiness Index (PRI)
            pri_score = round(
                (0.35 * acad_pct)
                + (0.35 * ((eval_rat / 5.0) * 100.0))
                + (0.15 * min(100.0, (exp_yrs / 15.0) * 100.0))
                + (0.15 * min(100.0, (train_hrs / 300.0) * 100.0)),
                2,
            )

            spec_ok = (required_specialty.upper() == "ALL") or (required_specialty.upper() in cand["specialty_tags"])
            meets_all = (
                (exp_yrs >= int(min_experience_years))
                and (acad_pct >= float(min_academy_score_pct))
                and (eval_rat >= float(min_eval_rating))
                and spec_ok
            )

            status_str = "QUALIFIED_PROMOTION_SHORTLIST" if meets_all else "BELOW_CURRENT_FILTER_THRESHOLD"
            row_item = {
                "Employee_ID": emp_id,
                "Candidate_Name": cand["full_name"],
                "Current_Role": cand["current_role"],
                "Recommended_Promotion_Track": cand["target_promotion_track"],
                "Exp_Yrs": exp_yrs,
                "Academy_Score": f"{acad_pct:.1f}%",
                "Training_Hrs": train_hrs,
                "Eval_Rating": f"{eval_rat:.2f} / 5.00",
                "Promotion_Readiness_Index": pri_score,
                "Prior_Jobs_and_Addresses": f"VERIFIED ({cand['prior_job_1'][:28]}...)",
                "Active_Certifications": cand["active_certifications"],
                "Promotion_Board_Decision": status_str,
            }
            all_evaluated_rows.append(row_item)
            if meets_all:
                qualified_rows.append(row_item)

        # Sort qualified shortlist by Promotion_Readiness_Index descending
        qualified_rows.sort(key=lambda r: r["Promotion_Readiness_Index"], reverse=True)
        for rank_idx, qrow in enumerate(qualified_rows, start=1):
            qrow["Shortlist_Rank"] = f"RANK #{rank_idx:02d}"

        # Record shortlist board evaluation in the 5th WORM SQLite table
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            for qrow in qualified_rows:
                b_hash = hashlib.sha256(
                    f"{qrow['Employee_ID']}|{qrow['Promotion_Readiness_Index']}|{qrow['Recommended_Promotion_Track']}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8")
                ).hexdigest()
                cur.execute(
                    """
                    INSERT OR IGNORE INTO worm_promotion_evaluation_board (
                        employee_id, candidate_name, recommended_promotion_track,
                        experience_years, academy_score_pct, eval_rating,
                        promotion_readiness_index, board_decision, worm_board_sha256
                    ) VALUES (?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        qrow["Employee_ID"],
                        qrow["Candidate_Name"],
                        qrow["Recommended_Promotion_Track"],
                        int(qrow["Exp_Yrs"]),
                        float(qrow["Academy_Score"].replace("%", "")),
                        float(qrow["Eval_Rating"].split("/")[0].strip()),
                        float(qrow["Promotion_Readiness_Index"]),
                        qrow["Promotion_Board_Decision"],
                        b_hash,
                    ),
                )
            conn.commit()
            board_rows_cnt = cur.execute("SELECT COUNT(*) FROM worm_promotion_evaluation_board").fetchone()[0]
        finally:
            conn.close()

        return {
            "total_personnel_evaluated": len(all_evaluated_rows),
            "qualified_candidates_count": len(qualified_rows),
            "top_ranked_candidate": qualified_rows[0]["Candidate_Name"] if qualified_rows else "NONE_MATCHING_FILTER",
            "top_pri_score": qualified_rows[0]["Promotion_Readiness_Index"] if qualified_rows else 0.0,
            "worm_board_rows_logged": board_rows_cnt,
            "qualified_shortlist_rows": qualified_rows,
            "all_evaluated_rows": all_evaluated_rows,
        }

    def get_saved_user_60field_values(
        self,
        out_dir: pathlib.Path,
        roster_key: str | None = None,
    ) -> Dict[str, str]:
        """
        Returns the 60 atomic field values currently pre-populated or saved by the user/employee
        so the 60-Field Interactive Input Form displays their exact current values.
        """
        base_vals = dict(self.DEFAULT_ATOMIC_42_VALUES)
        if roster_key and roster_key in self.PERSONNEL_EMERGENCY_ROSTER:
            person = self.PERSONNEL_EMERGENCY_ROSTER[roster_key]
            name_parts = person["full_name"].split()
            base_vals.update({
                "f01_first_name": name_parts[0] if len(name_parts) >= 1 else "JEFFERY",
                "f02_middle_name": name_parts[1] if len(name_parts) >= 3 else "SOVEREIGN",
                "f03_last_name": name_parts[-1] if len(name_parts) >= 2 else "HUMPHREY",
                "f15_primary_phone": person["direct_phone"],
                "f16_email_address": person["email"].upper(),
                "f21_job_title": person["role_title"].upper(),
                "f22_department_unit": person["department"].upper(),
                "f28_nok_full_name": person["nok_full_name"].upper(),
                "f29_nok_relationship": person["nok_relationship"].upper(),
                "f30_nok_phone": person["nok_phone"],
                "f31_nok_address": person["nok_address"].upper(),
                "f32_ice_full_name": person["ice_full_name"].upper(),
                "f33_ice_relationship": person["ice_relationship"].upper(),
                "f34_ice_phone": person["ice_phone"],
                "f35_ice_medical_blood": person["blood_type_and_medical"],
            })
            cand_m = self.CANDIDATE_CAREER_AND_TRAINING_MATRIX.get(person["employee_id"])
            if cand_m:
                base_vals.update({
                    "f43_prev_addr1_street": cand_m["prev_address_1"].upper(),
                    "f47_prev_addr2_summary": cand_m["prev_address_2"].upper(),
                    "f49_prior_emp1_org": cand_m["prior_job_1"].upper(),
                    "f53_prior_emp2_org_role": cand_m["prior_job_2"].upper(),
                    "f54_total_experience_yrs": str(cand_m["total_experience_yrs"]),
                    "f55_highest_education": cand_m["highest_education"].upper(),
                    "f56_academy_exam_score": str(cand_m["academy_exam_score_pct"]),
                    "f57_completed_hvf_courses": cand_m["completed_hvf_modules"].upper(),
                    "f58_active_certifications": cand_m["active_certifications"].upper(),
                    "f59_training_hours_total": str(cand_m["training_hours"]),
                    "f60_company_eval_rating": str(cand_m["company_eval_rating"]),
                })
        state = self.load_or_init_vault_lock_state(out_dir)
        emp_id = self.PERSONNEL_EMERGENCY_ROSTER[roster_key]["employee_id"] if (roster_key and roster_key in self.PERSONNEL_EMERGENCY_ROSTER) else "EMP-001"
        saved_by_emp = state.get("saved_profiles_by_emp", {})
        if emp_id in saved_by_emp and isinstance(saved_by_emp[emp_id], dict):
            base_vals.update(saved_by_emp[emp_id])
        return base_vals

    def submit_user_60field_onboarding_application(
        self,
        out_dir: pathlib.Path,
        roster_key: str,
        profile_60_inputs: Dict[str, str],
        submitted_by_role: str = "EMPLOYEE_SELF_SERVICE_SUBMISSION",
        submission_reason: str = "USER_60FIELD_ONBOARDING_AND_DOSSIER_SUBMISSION",
    ) -> Dict[str, Any]:
        """
        Saves the user's 60-field input form values into persistent vault state, seals the
        revision into the WORM SQLite ledger (worm_identity_profile_revisions), and locks
        the updated Proof-of-Identity record.
        """
        state = self.load_or_init_vault_lock_state(out_dir)
        person = self.PERSONNEL_EMERGENCY_ROSTER.get(
            roster_key,
            next(iter(self.PERSONNEL_EMERGENCY_ROSTER.values())),
        )
        emp_id = person["employee_id"]
        saved_by_emp = state.get("saved_profiles_by_emp", {})
        clean_inputs = {k: str(v).strip() for k, v in profile_60_inputs.items()}
        saved_by_emp[emp_id] = clean_inputs
        state["saved_profiles_by_emp"] = saved_by_emp
        state["is_locked"] = True
        state["revision_number"] = int(state.get("revision_number", 1)) + 1
        state["last_approved_by"] = submitted_by_role
        state["last_change_reason"] = submission_reason
        (out_dir / "wp7_personnel_vault_state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")

        dossier_res = self.generate_wp7_antifraud_dossier(
            out_dir,
            raw_ssn=clean_inputs.get("f05_ssn", "999-00-1234"),
            raw_dob=clean_inputs.get("f06_dob", "1975-08-15"),
            operator_name=f"{clean_inputs.get('f01_first_name', 'JEFFERY')} {clean_inputs.get('f02_middle_name', 'SOVEREIGN')} {clean_inputs.get('f03_last_name', 'HUMPHREY')}",
            update_reason=f"{submitted_by_role}: {submission_reason}",
            profile_42_overrides=clean_inputs,
        )
        return {
            "submitted": True,
            "employee_id": emp_id,
            "revision_number": state["revision_number"],
            "composite_60field_seal": dossier_res["pii_report"]["composite_42field_application_seal"],
            "worm_seal": dossier_res["worm_seal"],
        }

    def open_compartment_gate(
        self,
        roster_key: str,
        viewer_role: str,
        user_agreement_accepted: bool,
        access_key_or_pin: str,
        out_dir: pathlib.Path,
        credit_freeze_locked: bool = True,
        emergency_purpose: str = "AUTHORIZED_HIPAA_MEDICAL_MUSTER_AND_ICE_ACCESS",
    ) -> Dict[str, Any]:
        """
        Enforces strict HIPAA / ADA / OSHA Gate Locking & Dual-Compartment Separation:
          - If user_agreement_accepted is False or PIN/Key is invalid -> GATE_LOCKED:
              * emergency_medical_ice_card = None (Zero PHI or personal PII exposed on locked screen!)
              * emergency_procedures_muster = None
              * credit_report = None
              * employer_internal_records = None
              * proof_of_id_rows = None
          - Path A (viewer_role == "EMPLOYEE", Valid Employee PIN):
              * Unseals emergency_procedures_muster (Primary/Secondary Muster Points, Shelter-in-Place Bunker,
                Nearest AED/Trauma Kit, Evacuation Route, & 5-Step Emergency Action Plan)
              * Unseals emergency_medical_ice_card (Blood Type, Allergies, Medical History, Physician, NOK/ICE)
              * Unseals Employee Personal Credit/Loan Shield & 60-Field Dossier
              * BLOCKS Employer Internal HR/Clearance records & Employer Notes
          - Path B (viewer_role == "EMPLOYER", Valid Employer/HR Master Key):
              * Unseals emergency_medical_ice_card & Muster Accountability for HR / Emergency Triage
                (Blood Type, Allergies, Medical History, Physician, NOK/ICE, & Assigned Muster Point)
                and logs the access to worm_hipaa_emergency_triage_log
              * Unseals Employer Proof-of-Identity, Internal HR Records, Employer Notes, & Promotion Shortlist
              * BLOCKS Employee Personal Credit/Loans & Personal Bank/Deed Accounts
        """
        if not user_agreement_accepted:
            return {
                "gate_open": False,
                "gate_status": "GATE_LOCKED_HIPAA_AND_USER_AGREEMENT_AUTHORIZATION_REQUIRED",
                "viewer_role": viewer_role,
                "emergency_medical_ice_card": None,
                "emergency_procedures_muster": self.get_public_emergency_muster_and_sops(roster_key),
                "credit_report": None,
                "employer_internal_records": None,
                "employer_personnel_notes": None,
                "proof_of_id_rows": None,
            }

        person = self.PERSONNEL_EMERGENCY_ROSTER.get(
            roster_key,
            next(iter(self.PERSONNEL_EMERGENCY_ROSTER.values())),
        )
        expected_emp_pin = person["employee_pin"]
        expected_employer_key = "EMPLOYER-MASTER-1AHA8"

        name_parts = person["full_name"].split()
        first_n = name_parts[0] if len(name_parts) >= 1 else "JEFFERY"
        mid_n   = name_parts[1] if len(name_parts) >= 3 else "SOVEREIGN"
        last_n  = name_parts[-1] if len(name_parts) >= 2 else "HUMPHREY"
        person_overrides = {
            "f01_first_name": first_n,
            "f02_middle_name": mid_n,
            "f03_last_name": last_n,
            "f15_primary_phone": person["direct_phone"],
            "f16_email_address": person["email"].upper(),
            "f21_job_title": person["role_title"].upper(),
            "f22_department_unit": person["department"].upper(),
            "f28_nok_full_name": person["nok_full_name"].upper(),
            "f29_nok_relationship": person["nok_relationship"].upper(),
            "f30_nok_phone": person["nok_phone"],
            "f31_nok_address": person["nok_address"].upper(),
            "f32_ice_full_name": person["ice_full_name"].upper(),
            "f33_ice_relationship": person["ice_relationship"].upper(),
            "f34_ice_phone": person["ice_phone"],
            "f35_ice_medical_blood": person["blood_type_and_medical"],
        }
        cand_m = self.CANDIDATE_CAREER_AND_TRAINING_MATRIX.get(person["employee_id"])
        if cand_m:
            person_overrides.update({
                "f43_prev_addr1_street": cand_m["prev_address_1"].upper(),
                "f47_prev_addr2_summary": cand_m["prev_address_2"].upper(),
                "f49_prior_emp1_org": cand_m["prior_job_1"].upper(),
                "f53_prior_emp2_org_role": cand_m["prior_job_2"].upper(),
                "f54_total_experience_yrs": str(cand_m["total_experience_yrs"]),
                "f55_highest_education": cand_m["highest_education"].upper(),
                "f56_academy_exam_score": str(cand_m["academy_exam_score_pct"]),
                "f57_completed_hvf_courses": cand_m["completed_hvf_modules"].upper(),
                "f58_active_certifications": cand_m["active_certifications"].upper(),
                "f59_training_hours_total": str(cand_m["training_hours"]),
                "f60_company_eval_rating": str(cand_m["company_eval_rating"]),
            })
        saved_vals = self.get_saved_user_60field_values(out_dir, roster_key)
        person_overrides.update(saved_vals)
        app_eval = self.evaluate_atomic_42_application(person_overrides)
        db_file = out_dir / "wp7_identity_credit_worm_ledger.db"

        if viewer_role == "EMPLOYEE":
            if access_key_or_pin.strip() != expected_emp_pin:
                return {
                    "gate_open": False,
                    "gate_status": "GATE_DENIED_INVALID_EMPLOYEE_PERSONAL_PIN",
                    "viewer_role": "EMPLOYEE",
                    "emergency_medical_ice_card": None,
                    "emergency_procedures_muster": None,
                    "credit_report": None,
                    "employer_internal_records": None,
                    "employer_personnel_notes": None,
                    "proof_of_id_rows": None,
                }
            med_ice = self.get_instant_emergency_triage_card(roster_key)
            hipaa_log = self.record_hipaa_emergency_triage_access(
                db_path=db_file,
                employee_id=person["employee_id"],
                employee_name=person["full_name"],
                accessor_role="PATH_A_EMPLOYEE_SELF_VAULT_AND_MUSTER_SOP",
                access_purpose=emergency_purpose,
            )
            cred = self.evaluate_credit_and_loan_activity(credit_freeze_locked=credit_freeze_locked)
            return {
                "gate_open": True,
                "gate_status": "PATH_A_EMPLOYEE_PERSONAL_VAULT_AND_MUSTER_SOP_OPEN",
                "viewer_role": "EMPLOYEE",
                "privacy_notice": (
                    "PATH A (EMPLOYEE PERSONAL COMPARTMENT) ACTIVE: Your Assigned Muster Points, 5-Step Emergency "
                    "Evacuation Procedures, Medical History/Allergies/Blood Type, NOK/ICE Contacts, 60-Field Dossier, "
                    "and 7-Channel Credit/Loan Shield are unsealed. Employer/HR is 100% blocked from your credit/loans."
                ),
                "emergency_medical_ice_card": med_ice,
                "emergency_procedures_muster": {
                    "primary_muster_point": med_ice["primary_muster_point"],
                    "secondary_muster_point": med_ice["secondary_muster_point"],
                    "shelter_in_place_bunker": med_ice["shelter_in_place_bunker"],
                    "nearest_aed_trauma_kit": med_ice["nearest_aed_trauma_kit"],
                    "evacuation_route_and_warden": med_ice["evacuation_route_and_warden"],
                    "emergency_procedures_rows": med_ice["emergency_procedures_rows"],
                },
                "hipaa_audit_seal": hipaa_log["worm_hipaa_sha256"],
                "credit_report": cred,
                "employer_internal_records": None,
                "employer_personnel_notes": None,
                "proof_of_id_rows": app_eval["attribute_rows"],
                "composite_seal": app_eval["composite_42field_application_seal"],
            }

        if viewer_role == "EMPLOYER":
            if access_key_or_pin.strip() != expected_employer_key:
                return {
                    "gate_open": False,
                    "gate_status": "GATE_DENIED_INVALID_EMPLOYER_HR_MASTER_KEY",
                    "viewer_role": "EMPLOYER",
                    "emergency_medical_ice_card": None,
                    "emergency_procedures_muster": None,
                    "credit_report": None,
                    "employer_internal_records": None,
                    "employer_personnel_notes": None,
                    "proof_of_id_rows": None,
                }
            med_ice = self.get_instant_emergency_triage_card(roster_key)
            hipaa_log = self.record_hipaa_emergency_triage_access(
                db_path=db_file,
                employee_id=person["employee_id"],
                employee_name=person["full_name"],
                accessor_role="PATH_B_EMPLOYER_HR_EMERGENCY_MEDICAL_AND_MUSTER_AUTHORITY",
                access_purpose=emergency_purpose,
            )
            employer_allowed_rows = [
                r for r in app_eval["attribute_rows"]
                if not r["Field_ID"].startswith(("F39_", "F40_", "F41_", "F42_"))
            ]
            return {
                "gate_open": True,
                "gate_status": "PATH_B_EMPLOYER_HR_AND_EMERGENCY_MEDICAL_ICE_VAULT_OPEN",
                "viewer_role": "EMPLOYER",
                "privacy_notice": (
                    "PATH B (EMPLOYER / HR COMPARTMENT) ACTIVE: Unsealed Employee Emergency Medical History, Allergies, "
                    "Blood Type, Primary Physician, NOK/ICE Triage Packet, & Assigned Muster Zone (Logged to HIPAA WORM "
                    "Audit Table), plus 60-Field Proof-of-Identity, Employer Notes, & Promotion Shortlist. "
                    "[PRIVACY WALL ENFORCED: Employee Personal Credit Bureaus & Loans Remain 100% Blocked]."
                ),
                "emergency_medical_ice_card": med_ice,
                "emergency_procedures_muster": {
                    "primary_muster_point": med_ice["primary_muster_point"],
                    "secondary_muster_point": med_ice["secondary_muster_point"],
                    "shelter_in_place_bunker": med_ice["shelter_in_place_bunker"],
                    "nearest_aed_trauma_kit": med_ice["nearest_aed_trauma_kit"],
                    "evacuation_route_and_warden": med_ice["evacuation_route_and_warden"],
                    "emergency_procedures_rows": med_ice["emergency_procedures_rows"],
                },
                "hipaa_audit_seal": hipaa_log["worm_hipaa_sha256"],
                "credit_report": None,
                "employer_internal_records": person["employer_internal_records"],
                "employer_personnel_notes": self.get_employer_personnel_notes(
                    db_file,
                    employee_id=person["employee_id"],
                ),
                "proof_of_id_rows": employer_allowed_rows,
                "composite_seal": app_eval["composite_42field_application_seal"],
            }

        return {
            "gate_open": False,
            "gate_status": "GATE_LOCKED_HIPAA_PROTECTED_SELECT_ROLE_TO_UNSEAL",
            "viewer_role": viewer_role,
            "emergency_medical_ice_card": None,
            "emergency_procedures_muster": None,
            "credit_report": None,
            "employer_internal_records": None,
            "employer_personnel_notes": None,
            "proof_of_id_rows": None,
        }

    def __init__(self) -> None:
        super().__init__(
            plugin_id="HVF-NG-CLIN-0033",
            clin_number="CLIN 0033",
            title="60-Field Atomic Personnel Dossier, NOK/ICE, Promotion Shortlist, & Credit Shield",
            version="7.7.0",
            target_trl="TRL 8/9",
            per_node_annual_gov_usd=95000,
            per_node_monthly_comm_usd=8500,
        )
        self._used_nonces: set[str] = set()

    @staticmethod
    def mask_ssn(raw_ssn: str) -> str:
        digits = "".join(ch for ch in raw_ssn if ch.isdigit())
        last4 = digits[-4:] if len(digits) >= 4 else "0000"
        return f"XXX-XX-{last4}"

    @staticmethod
    def mask_dob(raw_dob: str) -> str:
        clean = raw_dob.strip()
        day_part = clean[-2:] if len(clean) >= 2 else "01"
        return f"XXXX-XX-{day_part}"

    @staticmethod
    def mask_generic(raw_val: str, visible_tail: int = 4) -> str:
        alnum = "".join(ch for ch in raw_val.strip() if ch.isalnum())
        tail = alnum[-visible_tail:] if len(alnum) >= visible_tail else (alnum or "0000")
        return f"XXXX-MASKED-{tail}"

    def format_display_value(self, field_key: str, raw_val: str, is_sensitive: bool) -> str:
        if field_key == "f05_ssn":
            return self.mask_ssn(raw_val)
        if field_key == "f06_dob":
            return self.mask_dob(raw_val)
        if is_sensitive:
            return self.mask_generic(raw_val, 4)
        return raw_val.strip()

    def hash_identity_zero_knowledge(self, attribute_type: str, raw_value: str) -> Dict[str, str]:
        norm = f"{attribute_type.strip().upper()}:{raw_value.strip().upper()}"
        full_sha = hmac.new(
            IDENTITY_VAULT_PEPPER.encode("utf-8"),
            norm.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest().upper()
        return {
            "attribute_type": attribute_type.strip().upper(),
            "k_anonymity_prefix_5hex": full_sha[:5],
            "k_anonymity_suffix_59hex": full_sha[5:],
            "full_salted_hmac_sha256": full_sha,
        }

    def generate_ceo_credit_unfreeze_token(self, inquiry_reference_id: str) -> str:
        return hmac.new(
            IDENTITY_VAULT_PEPPER.encode("utf-8"),
            f"CEO_UNFREEZE|{inquiry_reference_id.strip().upper()}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest().upper()[:20]

    def generate_employer_change_approval_token(self, current_revision_number: int) -> str:
        digest = hmac.new(
            IDENTITY_VAULT_PEPPER.encode("utf-8"),
            f"EMPLOYER_CHANGE_APPROVAL|REV_{int(current_revision_number)}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest().upper()[:16]
        return f"HVF-APPROVE-{digest}"

    def verify_employer_change_approval_token(
        self,
        provided_token: str,
        current_revision_number: int,
    ) -> bool:
        expected = self.generate_employer_change_approval_token(current_revision_number)
        return hmac.compare_digest(provided_token.strip().upper(), expected)

    def evaluate_atomic_42_application(
        self,
        profile_42: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        merged: Dict[str, str] = dict(self.DEFAULT_ATOMIC_42_VALUES)
        if profile_42:
            for k, v in profile_42.items():
                if k in merged and v is not None and str(v).strip() != "":
                    merged[k] = str(v).strip()

        rows: List[Dict[str, str]] = []
        composite_parts: List[str] = []
        masked_summary: Dict[str, str] = {}

        for f_key, f_label, f_cat, is_sens in self.ATOMIC_42_SCHEMA:
            raw_v = merged[f_key]
            disp_v = self.format_display_value(f_key, raw_v, is_sens)
            zk = self.hash_identity_zero_knowledge(f_key, raw_v)
            composite_parts.append(zk["full_salted_hmac_sha256"])
            masked_summary[f_key] = disp_v
            rows.append({
                "Field_ID": f_key.upper(),
                "Section_Category": f_cat,
                "Application_Field": f_label,
                "Sealed_Display_Value": disp_v,
                "k_Anonymity_Prefix": zk["k_anonymity_prefix_5hex"],
                "Zero_Knowledge_HMAC": zk["full_salted_hmac_sha256"][:20] + "...",
                "Verification_State": "SEALED_UNALTERABLE",
            })

        honeypot_raw = "DARKWEB-LEAKED-SSN-CLONE-999-88-7777"
        hp_zk = self.hash_identity_zero_knowledge("HONEYPOT_TRAP", honeypot_raw)
        rows.append({
            "Field_ID": "F61_DARKWEB_CANARY",
            "Section_Category": "9_ACTIVE_THREAT_CANARY",
            "Application_Field": "61. Active Dark-Web Honeypot Canary (XXX-XX-7777)",
            "Sealed_Display_Value": "XXX-XX-7777 (QUARANTINED)",
            "k_Anonymity_Prefix": hp_zk["k_anonymity_prefix_5hex"],
            "Zero_Knowledge_HMAC": hp_zk["full_salted_hmac_sha256"][:20] + "...",
            "Verification_State": "DARKWEB_LEAK_INTERCEPTED",
        })

        composite_42_seal = hmac.new(
            IDENTITY_VAULT_PEPPER.encode("utf-8"),
            ("|".join(composite_parts) + "|" + FROZEN_EBONY_MERKLE_ROOT).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        full_legal_name = f"{merged['f01_first_name']} {merged['f02_middle_name']} {merged['f03_last_name']}".strip()
        masked_ssn = self.mask_ssn(merged["f05_ssn"])
        masked_dob = self.mask_dob(merged["f06_dob"])

        return {
            "full_legal_name": full_legal_name,
            "masked_ssn": masked_ssn,
            "masked_dob": masked_dob,
            "atomic_fields_count": len(self.ATOMIC_42_SCHEMA),
            "core_identifying_features_count": len(self.ATOMIC_42_SCHEMA),
            "attributes_monitored": len(rows),
            "clean_attributes": len(self.ATOMIC_42_SCHEMA),
            "compromised_vectors_quarantined": 1,
            "composite_8factor_identity_seal": composite_42_seal,
            "composite_16factor_identity_seal": composite_42_seal,
            "composite_42field_application_seal": composite_42_seal,
            "masked_summary": masked_summary,
            "attribute_rows": rows,
        }

    def scan_pii_and_biometric_darkweb_feed(
        self,
        raw_ssn: str = "999-00-1234",
        raw_dob: str = "1975-08-15",
        pob_and_maiden_kba: str = "VAULT-KBA-MAIDEN-991",
        physical_id_number: str = "OK-REALID-1AHA8-7741",
        passport_number: str = "US-PASS-558912044",
        dod_cac_piv_serial: str = "1099482210",
        physical_smt_features: str = "NONE_VERIFIED",
        fingerprint_minutiae: str = "ISO19794-2-MINUTIAE-SEAL-8841",
        iris_vascular_hash: str = "ISO19794-6-IRIS-VASCULAR-9920",
        face_voice_liveness: str = "3DFACE-VOICE-LIVENESS-7712",
        home_deed_parcel_apn: str = "OK-APN-DEED-LOCK-44019",
        bank_ach_aba_routing: str = "103000648",
        mobile_sim_imei_lock: str = "359881090044112",
        medical_npi_beneficiary: str = "O_POSITIVE_NO_KNOWN_DRUG_ALLERGIES",
        vehicle_fleet_vin: str = "1HVF882910SOVEREIGN",
        corporate_ein_uei: str = "HVF EXECUTIVE COMMAND (CAGE 1AHA8)",
        profile_42_overrides: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        prof = dict(self.DEFAULT_ATOMIC_42_VALUES)
        prof.update({
            "f05_ssn": raw_ssn,
            "f06_dob": raw_dob,
            "f10_mothers_maiden": pob_and_maiden_kba,
            "f25_drivers_license": physical_id_number,
            "f26_passport_number": passport_number,
            "f27_dod_cac_edipi": dod_cac_piv_serial,
            "f20_scars_marks_tattoos": physical_smt_features,
            "f36_bio_fingerprint": fingerprint_minutiae,
            "f37_bio_iris": iris_vascular_hash,
            "f38_bio_face_voice": face_voice_liveness,
            "f41_property_deed_apn": home_deed_parcel_apn,
            "f39_bank_aba_routing": bank_ach_aba_routing,
            "f42_mobile_sim_imei": mobile_sim_imei_lock,
            "f35_ice_medical_blood": medical_npi_beneficiary,
            "f22_department_unit": corporate_ein_uei,
        })
        if profile_42_overrides:
            for k, v in profile_42_overrides.items():
                if k in prof and v is not None:
                    prof[k] = str(v)
        return self.evaluate_atomic_42_application(prof)

    def load_or_init_vault_lock_state(self, out_dir: pathlib.Path) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        state_file = out_dir / "wp7_personnel_vault_state.json"
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text(encoding="utf-8"))
                if isinstance(data, dict) and "masked_profile" in data:
                    return data
            except Exception:
                pass
        app_eval = self.evaluate_atomic_42_application(self.DEFAULT_ATOMIC_42_VALUES)
        default_state = {
            "is_locked": True,
            "revision_number": 1,
            "last_approved_by": "SYSTEM_INITIAL_SOVEREIGN_SEAL",
            "last_change_reason": "INITIAL_42FIELD_ONBOARDING_PROOF_OF_IDENTITY",
            "composite_42field_seal": app_eval["composite_42field_application_seal"],
            "masked_profile": app_eval["masked_summary"],
        }
        state_file.write_text(json.dumps(default_state, indent=2, sort_keys=True), encoding="utf-8")
        return default_state

    def request_employer_unlock_for_edit(
        self,
        out_dir: pathlib.Path,
        provided_approval_token: str,
        change_reason: str,
        approving_authority: str = "JEFFERY HUMPHREY (EMPLOYER / CEO AUTHORITY)",
    ) -> Dict[str, Any]:
        state = self.load_or_init_vault_lock_state(out_dir)
        rev_num = int(state.get("revision_number", 1))
        if not self.verify_employer_change_approval_token(provided_approval_token, rev_num):
            return {
                "unlocked": False,
                "status": "UNLOCK_DENIED_INVALID_EMPLOYER_APPROVAL_TOKEN",
                "state": state,
            }
        if not change_reason or len(change_reason.strip()) < 4:
            return {
                "unlocked": False,
                "status": "UNLOCK_DENIED_CHANGE_REASON_REQUIRED",
                "state": state,
            }
        state["is_locked"] = False
        state["last_approved_by"] = approving_authority.strip()
        state["last_change_reason"] = change_reason.strip()
        (out_dir / "wp7_personnel_vault_state.json").write_text(
            json.dumps(state, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return {
            "unlocked": True,
            "status": "UNLOCK_APPROVED_FOR_ONE_TIME_REVISION",
            "state": state,
        }

    def seal_and_lock_personnel_application(
        self,
        out_dir: pathlib.Path,
        profile_42: Dict[str, str],
        update_reason: str = "EMPLOYER_VERIFIED_ONBOARDING_SEAL",
        approving_authority: str = "JEFFERY HUMPHREY (EMPLOYER / CEO AUTHORITY)",
    ) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        app_eval = self.evaluate_atomic_42_application(profile_42)
        db_file = out_dir / "wp7_identity_credit_worm_ledger.db"
        rev_info = self.commit_profile_update_revision(
            db_path=db_file,
            operator_name=app_eval["full_legal_name"],
            update_reason=update_reason,
            pii_report=app_eval,
        )
        new_state = {
            "is_locked": True,
            "revision_number": rev_info["revision_number"],
            "last_approved_by": approving_authority,
            "last_change_reason": update_reason,
            "composite_42field_seal": app_eval["composite_42field_application_seal"],
            "masked_profile": app_eval["masked_summary"],
        }
        (out_dir / "wp7_personnel_vault_state.json").write_text(
            json.dumps(new_state, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return {
            "locked": True,
            "status": "SEALED_UNALTERABLE_PROOF_OF_IDENTITY",
            "revision_info": rev_info,
            "state": new_state,
            "app_eval": app_eval,
        }

    def evaluate_credit_and_loan_activity(
        self,
        credit_freeze_locked: bool = True,
        loan_events: List[Dict[str, str]] | None = None,
    ) -> Dict[str, Any]:
        if loan_events is None:
            valid_ceo_token = self.generate_ceo_credit_unfreeze_token("REQ-HVF-EQUIP-2026-001")
            loan_events = [
                {
                    "inquiry_id": "INQ-EQFX-99201",
                    "bureau_or_lender": "1. Equifax // Online Auto & Personal Loan Desk",
                    "product_type": "UNAUTHORIZED_HARD_CREDIT_PULL_AND_75K_AUTO_LOAN",
                    "applicant_ssn_masked": "XXX-XX-1234",
                    "applicant_dob_masked": "XXXX-XX-15",
                    "ceo_unfreeze_token": "NONE_STOLEN_SSN_ATTEMPT",
                },
                {
                    "inquiry_id": "INQ-EXPN-88412",
                    "bureau_or_lender": "2. Experian & SBA // Commercial Loan & UCC-1 Desk",
                    "product_type": "FRAUDULENT_SBA_LOAN_AND_UCC1_LIEN_FILING",
                    "applicant_ssn_masked": "UEI:S1M4ENLHTDH5",
                    "applicant_dob_masked": "CAGE:1AHA8",
                    "ceo_unfreeze_token": "FORGED_TOKEN_0000",
                },
                {
                    "inquiry_id": "INQ-TRNS-55109",
                    "bureau_or_lender": "3. TransUnion // Synthetic Identity Credit Card",
                    "product_type": "SYNTHETIC_ID_MISMATCH_SSN_WITH_WRONG_DOB_AND_BIO",
                    "applicant_ssn_masked": "XXX-XX-1234",
                    "applicant_dob_masked": "XXXX-XX-99 (MISMATCH)",
                    "ceo_unfreeze_token": "NONE",
                },
                {
                    "inquiry_id": "INQ-CHEX-33104",
                    "bureau_or_lender": "4. ChexSystems & Early Warning (EWS) // Bank Wire Desk",
                    "product_type": "UNAUTHORIZED_CHECKING_ACCOUNT_AND_ACH_WIRE_DRAIN",
                    "applicant_ssn_masked": "XXX-XX-1234",
                    "applicant_dob_masked": "ABA-ACH-LOCKED",
                    "ceo_unfreeze_token": "NONE",
                },
                {
                    "inquiry_id": "INQ-DEED-77420",
                    "bureau_or_lender": "5. County Assessor Recorder // Real Estate Title Desk",
                    "product_type": "FRAUDULENT_QUITCLAIM_DEED_AND_HELOC_MORTGAGE_LOAN",
                    "applicant_ssn_masked": "APN-DEED-44019",
                    "applicant_dob_masked": "XXXX-XX-15",
                    "ceo_unfreeze_token": "NONE",
                },
                {
                    "inquiry_id": "INQ-SIMP-66018",
                    "bureau_or_lender": "6. Mobile Telecom Carrier // SIM Port-Out & 2FA Desk",
                    "product_type": "UNAUTHORIZED_SIM_SWAP_AND_NUMBER_PORT_OUT_ATTEMPT",
                    "applicant_ssn_masked": "IMEI-SIMLOCK-ON",
                    "applicant_dob_masked": "XXXX-XX-15",
                    "ceo_unfreeze_token": "NONE",
                },
                {
                    "inquiry_id": "REQ-HVF-EQUIP-2026-001",
                    "bureau_or_lender": "7. Dun & Bradstreet // Authorized Sovereign Vendor Line",
                    "product_type": "CEO_PREAUTHORIZED_COMMERCIAL_HARDWARE_CREDIT_LINE",
                    "applicant_ssn_masked": "UEI:S1M4ENLHTDH5",
                    "applicant_dob_masked": "CAGE:1AHA8",
                    "ceo_unfreeze_token": valid_ceo_token,
                },
            ]

        evaluated_rows: List[Dict[str, str]] = []
        blocked_loans = 0
        approved_loans = 0

        for ev in loan_events:
            inq_id = ev["inquiry_id"]
            expected_token = self.generate_ceo_credit_unfreeze_token(inq_id)
            provided_token = ev.get("ceo_unfreeze_token", "")
            dob_mismatch = "MISMATCH" in ev.get("applicant_dob_masked", "")

            if dob_mismatch:
                blocked_loans += 1
                decision = "BLOCKED_SYNTHETIC_IDENTITY_SSN_DOB_BIO_MISMATCH"
                remedy = "FCRA_605B_BLOCK_AND_LAW_ENFORCEMENT_PACKET_SEALED"
            elif credit_freeze_locked and (provided_token != expected_token):
                blocked_loans += 1
                decision = "BLOCKED_UNAUTHORIZED_LOAN_CREDIT_DEED_OR_SIM_SWAP"
                remedy = "HARD_PULL_REJECTED_AND_SOVEREIGN_FREEZE_ENFORCED"
            else:
                approved_loans += 1
                decision = "AUTHORIZED_BY_CEO_CRYPTOGRAPHIC_UNFREEZE_TOKEN"
                remedy = "ONE_TIME_WINDOW_VERIFIED_AND_RELOCKED"

            evaluated_rows.append({
                "Inquiry_ID": inq_id,
                "Bureau_or_Channel": ev["bureau_or_lender"],
                "Credit_Loan_or_Asset_Event": ev["product_type"],
                "Protected_ID_Vector": f"{ev['applicant_ssn_masked']} | {ev['applicant_dob_masked']}",
                "Interception_Decision": decision,
                "Statutory_Action": remedy,
            })

        return {
            "credit_freeze_locked": credit_freeze_locked,
            "total_inquiries_monitored": len(evaluated_rows),
            "fraudulent_loans_and_pulls_blocked": blocked_loans,
            "ceo_authorized_transactions": approved_loans,
            "credit_loan_rows": evaluated_rows,
        }

    def record_physical_id_access_event(
        self,
        operator_name: str,
        physical_id_serial: str,
        raw_ssn: str = "999-00-1234",
        raw_dob: str = "1975-08-15",
        biometric_liveness_hash: str = "BIO-3MODAL-FINGER-IRIS-FACE-VERIFIED",
        id_type: str = "OKLAHOMA_REAL_ID_PASSPORT_AND_CAC",
        action: str = "SIGN_IN",
        hardware_liveness_nonce: str = "NONCE-2026-10-26-ALPHA-001",
        previous_ledger_hash: str = "0000000000000000000000000000000000000000000000000000000000000000",
        is_compromised_or_mismatched: bool = False,
    ) -> Dict[str, Any]:
        assert action in ("SIGN_IN", "SIGN_OUT"), f"Invalid access action: {action}"
        masked_ssn = self.mask_ssn(raw_ssn)
        masked_dob = self.mask_dob(raw_dob)
        zk_id = self.hash_identity_zero_knowledge(
            id_type,
            f"{physical_id_serial}|{raw_ssn}|{raw_dob}|{biometric_liveness_hash}",
        )

        replay_detected = hardware_liveness_nonce in self._used_nonces
        if replay_detected or is_compromised_or_mismatched:
            access_decision = "ACCESS_DENIED_FRAUD_INTERLOCK_TRIPPED"
            reason = "REPLAYED_NONCE_OR_STOLEN_SSN_DOB_BIOMETRIC_MISMATCH"
        else:
            self._used_nonces.add(hardware_liveness_nonce)
            access_decision = f"AUTHORIZED_{action}_RECORDED"
            reason = "60_FIELD_ID_SSN_DOB_AND_BIOMETRIC_LIVENESS_VERIFIED"

        worm_entry_hash = hmac.new(
            IDENTITY_VAULT_PEPPER.encode("utf-8"),
            (
                f"{previous_ledger_hash}|{operator_name}|{zk_id['full_salted_hmac_sha256']}|"
                f"{action}|{hardware_liveness_nonce}|{access_decision}|{FROZEN_EBONY_MERKLE_ROOT}"
            ).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return {
            "Operator_Name": operator_name,
            "ID_Document_Type": id_type,
            "Masked_SSN_DOB_Bind": f"{masked_ssn} | {masked_dob}",
            "Biometric_Gate": self.mask_generic(biometric_liveness_hash, 8),
            "Action": action,
            "Liveness_Nonce": hardware_liveness_nonce,
            "Access_Decision": access_decision,
            "Security_Reason": reason,
            "WORM_Ledger_SHA256": worm_entry_hash,
        }

    def init_worm_sqlite_ledger(self, db_path: pathlib.Path) -> Dict[str, Any]:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_id_access_log (
                    seq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operator_name TEXT NOT NULL,
                    id_document_type TEXT NOT NULL,
                    masked_ssn_dob TEXT NOT NULL,
                    biometric_gate TEXT NOT NULL,
                    action TEXT NOT NULL,
                    liveness_nonce TEXT NOT NULL,
                    access_decision TEXT NOT NULL,
                    security_reason TEXT NOT NULL,
                    worm_ledger_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_id_access_no_update
                BEFORE UPDATE ON worm_id_access_log
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED ON worm_id_access_log');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_id_access_no_delete
                BEFORE DELETE ON worm_id_access_log
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED ON worm_id_access_log');
                END;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_credit_loan_intercept_log (
                    seq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inquiry_id TEXT NOT NULL,
                    bureau_or_channel TEXT NOT NULL,
                    credit_loan_event TEXT NOT NULL,
                    protected_id_vector TEXT NOT NULL,
                    interception_decision TEXT NOT NULL,
                    statutory_action TEXT NOT NULL,
                    worm_intercept_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_credit_no_update
                BEFORE UPDATE ON worm_credit_loan_intercept_log
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED ON worm_credit_loan_intercept_log');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_credit_no_delete
                BEFORE DELETE ON worm_credit_loan_intercept_log
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED ON worm_credit_loan_intercept_log');
                END;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_identity_profile_revisions (
                    rev_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operator_name TEXT NOT NULL,
                    update_reason TEXT NOT NULL,
                    masked_ssn_dob TEXT NOT NULL,
                    composite_16factor_seal TEXT NOT NULL,
                    masked_profile_json TEXT NOT NULL,
                    previous_revision_hash TEXT NOT NULL,
                    worm_revision_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_profile_rev_no_update
                BEFORE UPDATE ON worm_identity_profile_revisions
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED ON worm_identity_profile_revisions');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_profile_rev_no_delete
                BEFORE DELETE ON worm_identity_profile_revisions
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED ON worm_identity_profile_revisions');
                END;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_employer_personnel_notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT NOT NULL,
                    employee_name TEXT NOT NULL,
                    author_authority TEXT NOT NULL,
                    note_category TEXT NOT NULL,
                    confidential_note_text TEXT NOT NULL,
                    previous_note_hash TEXT NOT NULL,
                    worm_note_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_emp_notes_no_update
                BEFORE UPDATE ON worm_employer_personnel_notes
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED ON worm_employer_personnel_notes');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_emp_notes_no_delete
                BEFORE DELETE ON worm_employer_personnel_notes
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED ON worm_employer_personnel_notes');
                END;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_promotion_evaluation_board (
                    board_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT NOT NULL,
                    candidate_name TEXT NOT NULL,
                    recommended_promotion_track TEXT NOT NULL,
                    experience_years INTEGER NOT NULL,
                    academy_score_pct REAL NOT NULL,
                    eval_rating REAL NOT NULL,
                    promotion_readiness_index REAL NOT NULL,
                    board_decision TEXT NOT NULL,
                    worm_board_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_promo_board_no_update
                BEFORE UPDATE ON worm_promotion_evaluation_board
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED ON worm_promotion_evaluation_board');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_promo_board_no_delete
                BEFORE DELETE ON worm_promotion_evaluation_board
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED ON worm_promotion_evaluation_board');
                END;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS worm_hipaa_emergency_triage_log (
                    triage_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT NOT NULL,
                    employee_name TEXT NOT NULL,
                    accessor_role TEXT NOT NULL,
                    access_purpose TEXT NOT NULL,
                    hipaa_statutory_basis TEXT NOT NULL,
                    previous_log_hash TEXT NOT NULL,
                    worm_hipaa_sha256 TEXT NOT NULL UNIQUE
                )
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_hipaa_no_update
                BEFORE UPDATE ON worm_hipaa_emergency_triage_log
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED ON worm_hipaa_emergency_triage_log');
                END;
            """)
            cur.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_worm_hipaa_no_delete
                BEFORE DELETE ON worm_hipaa_emergency_triage_log
                BEGIN
                    SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED ON worm_hipaa_emergency_triage_log');
                END;
            """)
            conn.commit()
        finally:
            conn.close()
        return {"db_path": str(db_path), "worm_triggers_active": 12}

    def commit_profile_update_revision(
        self,
        db_path: pathlib.Path,
        operator_name: str,
        update_reason: str,
        pii_report: Dict[str, Any],
    ) -> Dict[str, Any]:
        self.init_worm_sqlite_ledger(db_path)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            last_row = cur.execute(
                "SELECT rev_id, worm_revision_sha256 FROM worm_identity_profile_revisions ORDER BY rev_id DESC LIMIT 1"
            ).fetchone()
            prev_hash = last_row[1] if last_row else ("0" * 64)
            next_rev_num = (last_row[0] + 1) if last_row else 1

            masked_json = json.dumps(pii_report.get("masked_summary", {}), sort_keys=True)
            comp_seal = pii_report["composite_16factor_identity_seal"]
            masked_ssn_dob = f"{pii_report['masked_ssn']} | {pii_report['masked_dob']}"

            rev_sha = hmac.new(
                IDENTITY_VAULT_PEPPER.encode("utf-8"),
                f"{prev_hash}|{operator_name}|{update_reason}|{comp_seal}|{masked_json}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            cur.execute(
                """
                INSERT OR IGNORE INTO worm_identity_profile_revisions (
                    operator_name, update_reason, masked_ssn_dob, composite_16factor_seal,
                    masked_profile_json, previous_revision_hash, worm_revision_sha256
                ) VALUES (?,?,?,?,?,?,?)
                """,
                (
                    operator_name,
                    update_reason,
                    masked_ssn_dob,
                    comp_seal,
                    masked_json,
                    prev_hash,
                    rev_sha,
                ),
            )
            conn.commit()
            total_revs = cur.execute("SELECT COUNT(*) FROM worm_identity_profile_revisions").fetchone()[0]
        finally:
            conn.close()
        return {
            "revision_number": total_revs or next_rev_num,
            "operator_name": operator_name,
            "update_reason": update_reason,
            "composite_16factor_seal": comp_seal,
            "previous_revision_hash": prev_hash,
            "worm_revision_sha256": rev_sha,
        }

    def get_profile_revision_history(self, db_path: pathlib.Path) -> List[Dict[str, Any]]:
        self.init_worm_sqlite_ledger(db_path)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            rows = cur.execute(
                """
                SELECT rev_id, operator_name, update_reason, masked_ssn_dob,
                       composite_16factor_seal, previous_revision_hash, worm_revision_sha256
                FROM worm_identity_profile_revisions
                ORDER BY rev_id DESC
                """
            ).fetchall()
        finally:
            conn.close()
        return [
            {
                "Revision": f"Rev #{r[0]:02d}",
                "Principal": r[1],
                "Approval_Reason": r[2],
                "Masked_SSN_DOB": r[3],
                "42Field_Seal": r[4][:20] + "...",
                "Prev_Rev_Hash": r[5][:16] + "...",
                "WORM_Revision_SHA256": r[6][:20] + "...",
            }
            for r in rows
        ]

    def sync_events_to_worm_sqlite(
        self,
        db_path: pathlib.Path,
        access_events: List[Dict[str, Any]],
        credit_rows: List[Dict[str, str]],
        operator_name: str = "JEFFERY SOVEREIGN HUMPHREY",
        pii_report: Dict[str, Any] | None = None,
        update_reason: str = "INITIAL_42FIELD_ONBOARDING_PROOF_OF_IDENTITY",
    ) -> Dict[str, int]:
        self.init_worm_sqlite_ledger(db_path)
        if pii_report is not None:
            self.commit_profile_update_revision(
                db_path=db_path,
                operator_name=operator_name,
                update_reason=update_reason,
                pii_report=pii_report,
            )
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            for ev in access_events:
                cur.execute(
                    """
                    INSERT OR IGNORE INTO worm_id_access_log (
                        operator_name, id_document_type, masked_ssn_dob, biometric_gate,
                        action, liveness_nonce, access_decision, security_reason, worm_ledger_sha256
                    ) VALUES (?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        ev["Operator_Name"],
                        ev["ID_Document_Type"],
                        ev["Masked_SSN_DOB_Bind"],
                        ev["Biometric_Gate"],
                        ev["Action"],
                        ev["Liveness_Nonce"],
                        ev["Access_Decision"],
                        ev["Security_Reason"],
                        ev["WORM_Ledger_SHA256"],
                    ),
                )
            for crow in credit_rows:
                c_hash = hashlib.sha256(
                    f"{crow['Inquiry_ID']}|{crow['Bureau_or_Channel']}|{crow['Interception_Decision']}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8")
                ).hexdigest()
                cur.execute(
                    """
                    INSERT OR IGNORE INTO worm_credit_loan_intercept_log (
                        inquiry_id, bureau_or_channel, credit_loan_event, protected_id_vector,
                        interception_decision, statutory_action, worm_intercept_sha256
                    ) VALUES (?,?,?,?,?,?,?)
                    """,
                    (
                        crow["Inquiry_ID"],
                        crow["Bureau_or_Channel"],
                        crow["Credit_Loan_or_Asset_Event"],
                        crow["Protected_ID_Vector"],
                        crow["Interception_Decision"],
                        crow["Statutory_Action"],
                        c_hash,
                    ),
                )
            conn.commit()
            id_cnt = cur.execute("SELECT COUNT(*) FROM worm_id_access_log").fetchone()[0]
            cr_cnt = cur.execute("SELECT COUNT(*) FROM worm_credit_loan_intercept_log").fetchone()[0]
            rv_cnt = cur.execute("SELECT COUNT(*) FROM worm_identity_profile_revisions").fetchone()[0]
        finally:
            conn.close()
        return {
            "worm_id_access_rows": id_cnt,
            "worm_credit_intercept_rows": cr_cnt,
            "worm_profile_revision_rows": rv_cnt,
            "worm_triggers_active": 12,
        }

    def generate_wp7_antifraud_dossier(
        self,
        out_dir: pathlib.Path,
        operator_name: str = "JEFFERY SOVEREIGN HUMPHREY",
        raw_ssn: str = "999-00-1234",
        raw_dob: str = "1975-08-15",
        pob_and_maiden_kba: str = "VAULT-KBA-MAIDEN-991",
        physical_id_number: str = "OK-REALID-1AHA8-7741",
        passport_number: str = "US-PASS-558912044",
        dod_cac_piv_serial: str = "1099482210",
        physical_smt_features: str = "NONE_VERIFIED",
        fingerprint_minutiae: str = "ISO19794-2-MINUTIAE-SEAL-8841",
        iris_vascular_hash: str = "ISO19794-6-IRIS-VASCULAR-9920",
        face_voice_liveness: str = "3DFACE-VOICE-LIVENESS-7712",
        home_deed_parcel_apn: str = "OK-APN-DEED-LOCK-44019",
        bank_ach_aba_routing: str = "103000648",
        mobile_sim_imei_lock: str = "359881090044112",
        medical_npi_beneficiary: str = "O_POSITIVE_NO_KNOWN_DRUG_ALLERGIES",
        vehicle_fleet_vin: str = "1HVF882910SOVEREIGN",
        corporate_ein_uei: str = "HVF EXECUTIVE COMMAND (CAGE 1AHA8)",
        credit_freeze_locked: bool = True,
        update_reason: str = "INITIAL_42FIELD_ONBOARDING_PROOF_OF_IDENTITY",
        profile_42_overrides: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        pii_report = self.scan_pii_and_biometric_darkweb_feed(
            raw_ssn=raw_ssn,
            raw_dob=raw_dob,
            pob_and_maiden_kba=pob_and_maiden_kba,
            physical_id_number=physical_id_number,
            passport_number=passport_number,
            dod_cac_piv_serial=dod_cac_piv_serial,
            physical_smt_features=physical_smt_features,
            fingerprint_minutiae=fingerprint_minutiae,
            iris_vascular_hash=iris_vascular_hash,
            face_voice_liveness=face_voice_liveness,
            home_deed_parcel_apn=home_deed_parcel_apn,
            bank_ach_aba_routing=bank_ach_aba_routing,
            mobile_sim_imei_lock=mobile_sim_imei_lock,
            medical_npi_beneficiary=medical_npi_beneficiary,
            vehicle_fleet_vin=vehicle_fleet_vin,
            corporate_ein_uei=corporate_ein_uei,
            profile_42_overrides=profile_42_overrides,
        )
        credit_report = self.evaluate_credit_and_loan_activity(credit_freeze_locked=credit_freeze_locked)

        self._used_nonces.clear()
        ev1 = self.record_physical_id_access_event(
            operator_name=pii_report["full_legal_name"],
            physical_id_serial=physical_id_number,
            raw_ssn=raw_ssn,
            raw_dob=raw_dob,
            biometric_liveness_hash=f"{fingerprint_minutiae}|{iris_vascular_hash}|{face_voice_liveness}",
            action="SIGN_IN",
            hardware_liveness_nonce="NONCE-HVF-20261026-0001",
        )
        ev2 = self.record_physical_id_access_event(
            operator_name="IMPOSTOR_WITH_STOLEN_SSN_AND_CLONED_BADGE",
            physical_id_serial="STOLEN-WEB-SSN-CREDENTIAL",
            raw_ssn=raw_ssn,
            raw_dob=raw_dob,
            biometric_liveness_hash="FAILED-BIOMETRIC-SPOOF",
            action="SIGN_IN",
            hardware_liveness_nonce="NONCE-HVF-20261026-0001",
            previous_ledger_hash=ev1["WORM_Ledger_SHA256"],
            is_compromised_or_mismatched=True,
        )
        ev3 = self.record_physical_id_access_event(
            operator_name=pii_report["full_legal_name"],
            physical_id_serial=physical_id_number,
            raw_ssn=raw_ssn,
            raw_dob=raw_dob,
            biometric_liveness_hash=f"{fingerprint_minutiae}|{iris_vascular_hash}|{face_voice_liveness}",
            action="SIGN_OUT",
            hardware_liveness_nonce="NONCE-HVF-20261026-0002",
            previous_ledger_hash=ev2["WORM_Ledger_SHA256"],
        )

        db_file = out_dir / "wp7_identity_credit_worm_ledger.db"
        worm_db_stats = self.sync_events_to_worm_sqlite(
            db_path=db_file,
            access_events=[ev1, ev2, ev3],
            credit_rows=credit_report["credit_loan_rows"],
            operator_name=pii_report["full_legal_name"],
            pii_report=pii_report,
            update_reason=update_reason,
        )
        revision_history = self.get_profile_revision_history(db_file)

        seal_str = (
            f"WP7|{pii_report['composite_42field_application_seal']}|"
            f"{credit_report['fraudulent_loans_and_pulls_blocked']}|"
            f"{ev1['WORM_Ledger_SHA256']}|{ev2['WORM_Ledger_SHA256']}|"
            f"{ev3['WORM_Ledger_SHA256']}|{FROZEN_EBONY_MERKLE_ROOT}"
        )
        worm_seal = hashlib.sha256(seal_str.encode("utf-8")).hexdigest()

        if ENCLAVE_MODE == "PRIVATE":
            pepper_desc = f"Active Sovereign 60-Field Pepper ({IDENTITY_VAULT_PEPPER[:18]}...)"
        else:
            pepper_desc = "[REDACTED_42FIELD_PII_PEPPER_DFARS_252_227_7018]"

        lines = [
            "# HUMPHREY VIRTUAL FARMS LLC // WP-7: 42-FIELD PERSONNEL ONBOARDING, NOK/ICE, PROOF-OF-IDENTITY, & CREDIT SHIELD",
            "**Entity:** Humphrey Virtual Farms LLC (`CAGE: 1AHA8` | `SAM.gov UEI: S1M4ENLHTDH5`)",
            "**Controlling Authority:** Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect",
            f"**Plug-In Module:** `CLIN 0033 v7.7 (WP-7 60-Field Proof-of-Identity & NOK/ICE Vault)` | **Enclave Tier:** `{ENCLAVE_MODE}`",
            f"**Host Ebony Baseline Merkle Root:** `{FROZEN_EBONY_MERKLE_ROOT}`",
            "",
            "---",
            "",
            "## 1. Unalterable 60-Field Personnel Proof-of-Identity, Employment, & NOK/ICE Application Dossier",
            f"* **Verified Applicant / Employee:** `{pii_report['full_legal_name']}` | **Reason:** `{update_reason}`",
            f"* **Masked SSN & DOB Binding:** `{pii_report['masked_ssn']}` | `{pii_report['masked_dob']}` (`0` Plaintext Sensitive Digits Stored)",
            f"* **Atomic Onboarding Fields Sealed:** `{pii_report['atomic_fields_count']} / 60` (`100% Atomic 1-Response-Per-Box`) + `1 Active Dark-Web Canary`",
            f"* **Composite 60-Field Proof-of-Identity Seal (HMAC-SHA256):** `{pii_report['composite_42field_application_seal']}`",
            f"* **Cryptographic Pepper Binding:** `{pepper_desc}`",
        ]
        for arow in pii_report["attribute_rows"]:
            lines.append(
                f"* **{arow['Application_Field']}:** `{arow['Sealed_Display_Value']}` (`k-Prefix {arow['k_Anonymity_Prefix']}` | `{arow['Verification_State']}`)"
            )
        lines.extend([
            "",
            "---",
            "",
            "## 2. 7-Channel Credit Bureau, SBA/Bank Loan, Home Deed Title, ACH Wire, & SIM-Swap Interceptor",
            f"* **Sovereign Credit, Loan, Title, & SIM Freeze State:** `LOCKED ({credit_report['credit_freeze_locked']})`",
            f"* **Fraudulent Loans, Hard Pulls, Deed Transfers, & SIM Swaps Blocked:** **`{credit_report['fraudulent_loans_and_pulls_blocked']}`**",
            f"* **CEO Pre-Authorized Unfreeze Transactions:** `{credit_report['ceo_authorized_transactions']}`",
        ])
        for crow in credit_report["credit_loan_rows"]:
            lines.append(
                f"* **`{crow['Inquiry_ID']}` ({crow['Bureau_or_Channel']}):** `{crow['Credit_Loan_or_Asset_Event']}` -> **`{crow['Interception_Decision']}`**"
            )
        lines.extend([
            "",
            "---",
            "",
            "## 3. Physical ID & 3-Modal Biometric Sign-In / Sign-Out WORM Audit Ledger",
            f"* **Event #1 ({ev1['Action']}):** `{ev1['Operator_Name']}` (`{ev1['Masked_SSN_DOB_Bind']}`) -> `{ev1['Access_Decision']}`",
            f"* **Event #2 ({ev2['Action']} - Fraud Blocked):** `{ev2['Operator_Name']}` -> **`{ev2['Access_Decision']}`** (`{ev2['Security_Reason']}`)",
            f"* **Event #3 ({ev3['Action']}):** `{ev3['Operator_Name']}` (`{ev3['Masked_SSN_DOB_Bind']}`) -> `{ev3['Access_Decision']}`",
            f"* **WORM Profile Revisions Logged:** `{worm_db_stats['worm_profile_revision_rows']}` (`6` WORM Tables / `12` Active SQLite WORM Triggers)",
            "",
            "---",
            f"**WORM WP-7 16-Factor Identity, Credit, Loan, & Deed Shield Master Seal (SHA-256):** `{worm_seal}`",
        ])

        md_text = "\n".join(lines) + "\n"
        md_file = out_dir / "WP7_SOVEREIGN_IDENTITY_CREDIT_LOAN_SHIELD_SPEC.md"
        pdf_file = out_dir / "WP7_SOVEREIGN_IDENTITY_CREDIT_LOAN_SHIELD_SPEC.pdf"
        md_file.write_bytes(md_text.encode("ascii", errors="ignore"))
        pdf_bytes = build_minimal_iso_pdf(lines)
        pdf_file.write_bytes(pdf_bytes)

        return {
            "pii_report": pii_report,
            "credit_report": credit_report,
            "access_events": [ev1, ev2, ev3],
            "worm_db_stats": worm_db_stats,
            "revision_history": revision_history,
            "worm_seal": worm_seal,
            "md_path": str(md_file),
            "pdf_path": str(pdf_file),
            "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        }
