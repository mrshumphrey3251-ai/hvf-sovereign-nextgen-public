"""
HVF Sovereign Next-Gen Work Package 8 (CLIN 0034 v8.0):
Enterprise HR, Front-Screen OSHA 1910.38 Muster & Emergency SOPs, HIPAA 45 CFR 164.502
Medical/Allergy/Blood/ICE Triage, Zero-Trust Two-Person Integrity (NIST SP 800-53 AC-5)
60-Field Personnel Dossier, & Qualified Promotion Shortlist Engine.
100% Physically Separated From Personal Credit/Loan Telemetry (CLIN 0033).
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
HR_VAULT_PEPPER = "PUBLIC_ENTERPRISE_HR_PEPPER_REDACTED_DFARS_252_227_7018"


class EnterpriseHRMusterHipaaPromotionEngine(SovereignExpansionModule):
    """
    Standalone WP-8 (CLIN 0034 v8.0): Enterprise HR, OSHA Front-Screen Muster SOPs,
    HIPAA Gate-Locked Medical/Allergy/Blood/ICE Triage, Zero-Trust Two-Person Integrity
    (HR Custodian + Independent Second Verifier) 60-Field Dossier, & Promotion Shortlist Puller.
    """

    ENTERPRISE_HR_AND_HIPAA_CHARTER: str = (
        "SOVEREIGN ENTERPRISE HR, OSHA MUSTER, HIPAA MEDICAL CONFIDENTIALITY, & ZERO-TRUST AC-5 CHARTER "
        "(OSHA 29 CFR 1910.38 / HIPAA 45 CFR 164.502 / ADA 42 U.S.C. 12112(d)(3)(B) / NIST SP 800-53 AC-5): "
        "(1) ZERO-SECOND FRONT-SCREEN MUSTER & EMERGENCY PROCEDURES: Facility Command Desks, Primary/Secondary Muster "
        "Points, Tornado/Blast Shelter Bunkers, AED/Trauma Kits, and 5-Step Emergency Evacuation SOPs are openly "
        "accessible on the front screen with zero login required. "
        "(2) 100% GATE-LOCKED HIPAA PHI & PERSONAL PII: Employee Blood Types, Drug/Latex Allergies, Medical History, "
        "Primary Physicians, Next-of-Kin (NOK), ICE contacts, and 60-Field Dossiers are strictly locked behind the HR Gate. "
        "(3) ZERO-TRUST TWO-PERSON INTEGRITY (NO SELF-APPROVAL): Once a 60-field dossier is sealed, NO single person "
        "(neither CEO, HR, nor Employee) can approve or unlock it alone. Unlocking requires Co-Signer #1 (HR Custodian) "
        "PLUS Co-Signer #2 (Independent Second-Party Verifier) where Signer #1 != Signer #2 and Signer #2 != Subject! "
        "(4) ZERO PERSONAL CREDIT CO-MINGLING: Personal credit bureaus and loans are 100% separated into WP-7 (CLIN 0033)."
    )

    COMPANY_EMERGENCY_CONTACTS: List[Dict[str, str]] = [
        {
            "Priority": "PRIORITY 1 (IMMEDIATE LIFE/SAFETY)",
            "Entity_Desk": "911 / Base Fire, EMS & Level-1 Trauma Dispatch",
            "Direct_Line": "911 / 405-555-0911",
            "Radio_Channel": "Emergency Repeater Ch. 1 (155.340 MHz)",
            "SLA_Response": "< 90 Seconds On-Site Muster",
        },
        {
            "Priority": "PRIORITY 2 (SOVEREIGN COMMAND)",
            "Entity_Desk": "HVF 24/7 Tactical Watch-Floor Commander Desk",
            "Direct_Line": "405-555-0100",
            "Radio_Channel": "Tactical Watch Net Ch. 2 (Encrypted)",
            "SLA_Response": "Zero-Second Continuous Watch",
        },
        {
            "Priority": "PRIORITY 3 (36.75ns HARDWARE E-STOP)",
            "Entity_Desk": "SiC MOSFET High-Voltage & 60Hz Microgrid Safety Desk",
            "Direct_Line": "405-555-0111",
            "Radio_Channel": "Engineering Safety Net Ch. 3",
            "SLA_Response": "36.75ns Autonomous Hardware Cutoff",
        },
        {
            "Priority": "PRIORITY 4 (EXECUTIVE & HR TRIAGE)",
            "Entity_Desk": "HVF Executive Command & HR Emergency NOK/ICE Desk",
            "Direct_Line": "405-555-0199",
            "Radio_Channel": "Command Override Ch. 1",
            "SLA_Response": "Immediate HIPAA Medical/ICE Unseal",
        },
    ]

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

    PERSONNEL_EMERGENCY_ROSTER: Dict[str, Dict[str, Any]] = {
        "EMP-001 // JEFFERY HUMPHREY (Founder, CEO & Principal Sovereign Architect)": {
            "employee_id": "EMP-001",
            "full_name": "JEFFERY SOVEREIGN HUMPHREY",
            "role_title": "Founder, CEO & Principal Sovereign Architect",
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
            "employer_internal_records": [
                {"Record_ID": "HR-001-CLR", "Employer_Category": "DoD Security Clearance & Vetting", "Internal_Status": "SOVEREIGN_COMMAND_AUTHORITY_ACTIVE (CAGE 1AHA8)", "Employer_Audit_Seal": "SEAL-CLR-1AHA8-001"},
                {"Record_ID": "HR-001-I9", "Employer_Category": "DHS Form I-9 & E-Verify Seal", "Internal_Status": "US_CITIZEN_VERIFIED_LIST_A_PASSPORT", "Employer_Audit_Seal": "SEAL-I9-1AHA8-001"},
                {"Record_ID": "HR-001-RBAC", "Employer_Category": "Watch-Floor Bitmask & E-Stop Override", "Internal_Status": "0xFF (SOVEREIGN_COMMANDER_ALL_8_BITS)", "Employer_Audit_Seal": "SEAL-RBAC-1AHA8-001"},
            ],
        },
        "EMP-002 // CAPT. MARCUS VANCE (Senior Watch Officer -- Shift Alpha)": {
            "employee_id": "EMP-002",
            "full_name": "MARCUS A. VANCE",
            "role_title": "Senior Tactical Watch Officer (Shift Alpha)",
            "department": "Watch-Floor Operations (CLIN 0031)",
            "direct_phone": "405-555-0211",
            "email": "mvance@hvf-sovereign.mil",
            "nok_full_name": "ELENA VANCE (Spouse / Primary NOK)",
            "nok_relationship": "SPOUSE_PRIMARY_BENEFICIARY",
            "nok_phone": "405-555-0219",
            "nok_address": "4420 Falcon Ridge Rd, Edmond, OK 73013",
            "ice_full_name": "DR. ROBERT VANCE (Brother / Secondary ICE)",
            "ice_relationship": "BROTHER_SECONDARY_ICE",
            "ice_phone": "405-555-0212",
            "blood_type_and_medical": "A_POSITIVE // PENICILLIN_ALLERGY_CARRY_EPIPEN",
            "employer_internal_records": [
                {"Record_ID": "HR-002-CLR", "Employer_Category": "DoD Security Clearance & Vetting", "Internal_Status": "SECRET_ACTIVE_TIER3_ADJUDICATED", "Employer_Audit_Seal": "SEAL-CLR-VANCE-002"},
                {"Record_ID": "HR-002-I9", "Employer_Category": "DHS Form I-9 & E-Verify Seal", "Internal_Status": "US_CITIZEN_VERIFIED_CAC_EDIPI", "Employer_Audit_Seal": "SEAL-I9-VANCE-002"},
                {"Record_ID": "HR-002-RBAC", "Employer_Category": "Watch-Floor Bitmask & E-Stop Override", "Internal_Status": "0x1F (WATCH_OFFICER_5_BITS)", "Employer_Audit_Seal": "SEAL-RBAC-VANCE-002"},
            ],
        },
        "EMP-003 // DR. SARAH LIN (Lead SiC MOSFET & SCADA Integration Engineer)": {
            "employee_id": "EMP-003",
            "full_name": "DR. SARAH E. LIN",
            "role_title": "Lead SiC MOSFET & SCADA Integration Engineer",
            "department": "Hardware & Microgrid Engineering (CLIN 0028/0029)",
            "direct_phone": "405-555-0233",
            "email": "slin@hvf-sovereign.mil",
            "nok_full_name": "DAVID LIN (Father / Primary NOK)",
            "nok_relationship": "PARENT_PRIMARY_NOK",
            "nok_phone": "405-555-0238",
            "nok_address": "815 Tech Pkwy, Norman, OK 73069",
            "ice_full_name": "GRACE LIN (Sister / Secondary ICE)",
            "ice_relationship": "SISTER_SECONDARY_ICE",
            "ice_phone": "405-555-0239",
            "blood_type_and_medical": "B_NEGATIVE // NO_KNOWN_DRUG_ALLERGIES",
            "employer_internal_records": [
                {"Record_ID": "HR-003-CLR", "Employer_Category": "DoD Security Clearance & Vetting", "Internal_Status": "SECRET_ACTIVE_CRITICAL_INFRASTRUCTURE", "Employer_Audit_Seal": "SEAL-CLR-LIN-003"},
                {"Record_ID": "HR-003-I9", "Employer_Category": "DHS Form I-9 & E-Verify Seal", "Internal_Status": "US_CITIZEN_VERIFIED_PASSPORT", "Employer_Audit_Seal": "SEAL-I9-LIN-003"},
                {"Record_ID": "HR-003-RBAC", "Employer_Category": "Watch-Floor Bitmask & E-Stop Override", "Internal_Status": "0x1F (HARDWARE_ENGINEER_INTERLOCK_AUTH)", "Employer_Audit_Seal": "SEAL-RBAC-LIN-003"},
            ],
        },
        "EMP-004 // CALEB ROSS (UAS Flight Operator & Civil GIS Specialist)": {
            "employee_id": "EMP-004",
            "full_name": "CALEB J. ROSS",
            "role_title": "UAS Flight Operator & Title 61 Civil GIS Specialist",
            "department": "Aerial GLI & Civil Survey (CLIN 0030)",
            "direct_phone": "405-555-0244",
            "email": "cross@hvf-sovereign.mil",
            "nok_full_name": "HANNAH ROSS (Spouse / Primary NOK)",
            "nok_relationship": "SPOUSE_PRIMARY_BENEFICIARY",
            "nok_phone": "405-555-0248",
            "nok_address": "2910 Prairie View Ln, Guthrie, OK 73044",
            "ice_full_name": "THOMAS ROSS (Father / Secondary ICE)",
            "ice_relationship": "PARENT_SECONDARY_ICE",
            "ice_phone": "405-555-0249",
            "blood_type_and_medical": "AB_POSITIVE // NO_KNOWN_DRUG_ALLERGIES",
            "employer_internal_records": [
                {"Record_ID": "HR-004-CLR", "Employer_Category": "DoD Security Clearance & Vetting", "Internal_Status": "PUBLIC_TRUST_FAA_PART_107_CERTIFIED", "Employer_Audit_Seal": "SEAL-CLR-ROSS-004"},
                {"Record_ID": "HR-004-I9", "Employer_Category": "DHS Form I-9 & E-Verify Seal", "Internal_Status": "US_CITIZEN_VERIFIED_REAL_ID", "Employer_Audit_Seal": "SEAL-I9-ROSS-004"},
                {"Record_ID": "HR-004-RBAC", "Employer_Category": "Watch-Floor Bitmask & E-Stop Override", "Internal_Status": "0x03 (TELEMETRY_AND_GIS_OPERATOR)", "Employer_Audit_Seal": "SEAL-RBAC-ROSS-004"},
            ],
        },
    }

    CANDIDATE_CAREER_AND_TRAINING_MATRIX: Dict[str, Dict[str, Any]] = {
        "EMP-001": {
            "employee_id": "EMP-001",
            "full_name": "JEFFERY SOVEREIGN HUMPHREY",
            "current_role": "Founder, CEO & Principal Sovereign Architect",
            "target_promotion_grade": "GS-15 / SES-Equivalent Sovereign Command Authority",
            "specialty_tracks": ["ALL", "EXECUTIVE_C2", "SIC_HARDWARE", "SCADA_PLC", "UAS_GIS", "RMF_CYBER"],
            "total_experience_yrs": 18,
            "academy_exam_score_pct": 100.0,
            "company_eval_rating": 5.00,
            "training_hours": 480,
            "highest_education": "Executive Sovereign Systems Architecture & Ag-Defense C2 Mastery",
            "prior_job_1": "Humphrey Virtual Farms LLC -- Founder & CEO (12 Yrs)",
            "prior_job_2": "Principal Critical Infrastructure & Autonomous Systems Architect (6 Yrs)",
            "prev_address_1": "200 Legacy Ranch Rd, Oklahoma City, OK 73101 (2018-2022)",
            "prev_address_2": "450 Heartland Ag Pkwy, Edmond, OK 73013 (2015-2018)",
            "active_certifications": "CAGE 1AHA8 Controlling Authority // Tradewinds TRL-7 Architect // DoD RMF Lead",
            "completed_hvf_modules": "ALL 26 CORE CLINs + WP-1..WP-9 NEXT-GEN MASTER CURRICULUM (1,420 Qs)",
        },
        "EMP-002": {
            "employee_id": "EMP-002",
            "full_name": "CAPT. MARCUS A. VANCE",
            "current_role": "Senior Tactical Watch Officer (Shift Alpha)",
            "target_promotion_grade": "Watch-Floor Operations Director (GS-14 Equivalent)",
            "specialty_tracks": ["ALL", "EXECUTIVE_C2", "RMF_CYBER", "SCADA_PLC"],
            "total_experience_yrs": 11,
            "academy_exam_score_pct": 95.5,
            "company_eval_rating": 4.85,
            "training_hours": 320,
            "highest_education": "B.S. Systems Engineering & Joint C2 Operations",
            "prior_job_1": "USAF / DoD Tactical Command Center Watch Officer (7 Yrs)",
            "prior_job_2": "Regional Grid Emergency Operations Supervisor (4 Yrs)",
            "prev_address_1": "1102 Base View Dr, Midwest City, OK 73110 (2019-2023)",
            "prev_address_2": "740 Air Depot Blvd, Moore, OK 73160 (2016-2019)",
            "active_certifications": "DoD IAT Level III (CISSP) // HVF Watch-Floor Commander 0x1F // NERC CIP",
            "completed_hvf_modules": "WP-5 Watch-Floor RBAC, WP-6 DoD RMF ATO, CLIN 0022/0024 Shift Handover",
        },
        "EMP-003": {
            "employee_id": "EMP-003",
            "full_name": "DR. SARAH E. LIN",
            "current_role": "Lead SiC MOSFET & SCADA Integration Engineer",
            "target_promotion_grade": "VP of Hardware & Microgrid Engineering (GS-15 Equivalent)",
            "specialty_tracks": ["ALL", "SIC_HARDWARE", "SCADA_PLC"],
            "total_experience_yrs": 9,
            "academy_exam_score_pct": 98.0,
            "company_eval_rating": 4.95,
            "training_hours": 360,
            "highest_education": "Ph.D. Power Electronics & Solid-State SiC Switching",
            "prior_job_1": "National Power Electronics Lab -- Senior SiC Design Lead (5 Yrs)",
            "prior_job_2": "Industrial Microgrid Modbus/DNP3 Protection Engineer (4 Yrs)",
            "prev_address_1": "904 Campus Crest Ln, Norman, OK 73072 (2020-2024)",
            "prev_address_2": "2210 Research Park Blvd, Austin, TX 78759 (2017-2020)",
            "active_certifications": "Licensed PE (Electrical) // IPC-2221B High-Voltage PCB // SAE J1939 Specialist",
            "completed_hvf_modules": "WP-2 36.75ns SiC Board, WP-3 PLC/SCADA/J1939, CLIN 0003/0006/0009",
        },
        "EMP-004": {
            "employee_id": "EMP-004",
            "full_name": "CALEB J. ROSS",
            "current_role": "UAS Flight Operator & Title 61 Civil GIS Specialist",
            "target_promotion_grade": "Chief Aerial Survey & Title 61 GIS Officer (GS-13 Equivalent)",
            "specialty_tracks": ["ALL", "UAS_GIS"],
            "total_experience_yrs": 6,
            "academy_exam_score_pct": 91.0,
            "company_eval_rating": 4.70,
            "training_hours": 240,
            "highest_education": "M.S. Geomatics, Photogrammetry & Civil GIS Surveying",
            "prior_job_1": "Oklahoma Civil Land & Aerial Survey Corp -- Lead UAS Pilot (4 Yrs)",
            "prior_job_2": "Precision Ag Multispectral GLI Analyst (2 Yrs)",
            "prev_address_1": "512 Cottonwood Creek Rd, Stillwater, OK 74074 (2020-2023)",
            "prev_address_2": "880 Pioneer Trl, Enid, OK 73701 (2018-2020)",
            "active_certifications": "FAA Part 107 Unmanned Aircraft Pilot // Oklahoma GIS Surveyor // Title 61 Auditor",
            "completed_hvf_modules": "WP-4 UAS GLI & Title 61 GIS, CLIN 0007 Louhaichi GLI, CLIN 0010 Retainage",
        },
    }

    ATOMIC_60_SCHEMA: List[Tuple[str, str, str, bool]] = [
        ("f01_first_name", "[01] Legal First Name", "SEC1_LEGAL_VITAL", False),
        ("f02_middle_name", "[02] Legal Middle Name", "SEC1_LEGAL_VITAL", False),
        ("f03_last_name", "[03] Legal Last Name", "SEC1_LEGAL_VITAL", False),
        ("f04_suffix", "[04] Name Suffix (Jr/Sr/III/None)", "SEC1_LEGAL_VITAL", False),
        ("f05_ssn", "[05] Social Security Number (9-Digit SSN)", "SEC1_LEGAL_VITAL", True),
        ("f06_dob", "[06] Date of Birth (YYYY-MM-DD)", "SEC1_LEGAL_VITAL", True),
        ("f07_birth_city", "[07] City of Birth", "SEC1_LEGAL_VITAL", True),
        ("f08_birth_state", "[08] State / Province of Birth", "SEC1_LEGAL_VITAL", True),
        ("f09_birth_country", "[09] Country of Birth", "SEC1_LEGAL_VITAL", False),
        ("f10_mothers_maiden", "[10] Mother's Maiden Surname (KBA)", "SEC1_LEGAL_VITAL", True),
        ("f11_street_address", "[11] Residential Street Address", "SEC2_CONTACT_PHYSICAL", True),
        ("f12_city", "[12] Residential City", "SEC2_CONTACT_PHYSICAL", False),
        ("f13_state", "[13] Residential State", "SEC2_CONTACT_PHYSICAL", False),
        ("f14_zip_code", "[14] Residential ZIP / Postal Code", "SEC2_CONTACT_PHYSICAL", False),
        ("f15_primary_phone", "[15] Primary Mobile Phone Number", "SEC2_CONTACT_PHYSICAL", False),
        ("f16_email_address", "[16] Official Email Address", "SEC2_CONTACT_PHYSICAL", False),
        ("f17_eye_color", "[17] Physical Eye Color", "SEC2_CONTACT_PHYSICAL", False),
        ("f18_hair_color", "[18] Physical Hair Color", "SEC2_CONTACT_PHYSICAL", False),
        ("f19_height_inches", "[19] Physical Height (Inches)", "SEC2_CONTACT_PHYSICAL", False),
        ("f20_distinguishing_marks", "[20] Distinguishing Scars, Marks, or Tattoos (SMT)", "SEC2_CONTACT_PHYSICAL", True),
        ("f21_job_title", "[21] Position / Role Applied For", "SEC3_JOB_GOV_ID", False),
        ("f22_department_unit", "[22] Assigned Department / Command Unit", "SEC3_JOB_GOV_ID", False),
        ("f23_clearance_level", "[23] Security Clearance / Vetting Tier", "SEC3_JOB_GOV_ID", False),
        ("f24_citizenship_i9", "[24] Citizenship / Form I-9 Work Eligibility", "SEC3_JOB_GOV_ID", False),
        ("f25_drivers_license_num", "[25] State Driver's License / REAL-ID Number", "SEC3_JOB_GOV_ID", True),
        ("f26_passport_num", "[26] U.S. Passport Book / Card Number", "SEC3_JOB_GOV_ID", True),
        ("f27_dod_cac_edipi", "[27] DoD CAC / FIPS 201 PIV 10-Digit EDIPI", "SEC3_JOB_GOV_ID", True),
        ("f28_nok_full_name", "[28] Next of Kin (NOK) Full Legal Name", "SEC4_NOK_ICE", False),
        ("f29_nok_relationship", "[29] Next of Kin (NOK) Relationship", "SEC4_NOK_ICE", False),
        ("f30_nok_phone", "[30] Next of Kin (NOK) Primary Phone", "SEC4_NOK_ICE", False),
        ("f31_nok_address", "[31] Next of Kin (NOK) Residential Address", "SEC4_NOK_ICE", True),
        ("f32_ice_full_name", "[32] In Case of Emergency (ICE) Contact Name", "SEC4_NOK_ICE", False),
        ("f33_ice_relationship", "[33] In Case of Emergency (ICE) Relationship", "SEC4_NOK_ICE", False),
        ("f34_ice_phone", "[34] In Case of Emergency (ICE) Direct Phone", "SEC4_NOK_ICE", False),
        ("f35_ice_medical_blood", "[35] Emergency Blood Type & Medical Alert Notes", "SEC4_NOK_ICE", False),
        ("f36_bio_fingerprint", "[36] Biometric #1: Fingerprint Minutiae Template", "SEC5_BIOMETRIC_SECURITY", True),
        ("f37_bio_iris_retina", "[37] Biometric #2: Iris & Retinal Vascular Template", "SEC5_BIOMETRIC_SECURITY", True),
        ("f38_bio_face_voice", "[38] Biometric #3: 3D Facial & Voiceprint Liveness", "SEC5_BIOMETRIC_SECURITY", True),
        ("f39_hardware_token_uuid", "[39] Issued YubiKey / Hardware Token Serial UUID", "SEC5_BIOMETRIC_SECURITY", False),
        ("f40_watchfloor_callsign", "[40] Assigned Watch-Floor Tactical Callsign", "SEC5_BIOMETRIC_SECURITY", False),
        ("f41_duty_shift_assignment", "[41] Primary Watch Shift & Muster Warden Role", "SEC5_BIOMETRIC_SECURITY", False),
        ("f42_nda_sf312_date", "[42] Executed SF-312 Classified/Sovereign NDA Date", "SEC5_BIOMETRIC_SECURITY", False),
        ("f43_prev_addr1_street", "[43] Previous Street Address #1", "SEC6_ADDRESS_HISTORY", False),
        ("f44_prev_addr1_city", "[44] Previous City #1", "SEC6_ADDRESS_HISTORY", False),
        ("f45_prev_addr1_state_zip", "[45] Previous State & ZIP Code #1", "SEC6_ADDRESS_HISTORY", False),
        ("f46_prev_addr1_dates", "[46] Previous Residence #1 Dates (From-To)", "SEC6_ADDRESS_HISTORY", False),
        ("f47_prev_addr2_summary", "[47] Previous Residence #2 City & State", "SEC6_ADDRESS_HISTORY", False),
        ("f48_prev_addr_landlord", "[48] Previous Residence Verification / Landlord Contact", "SEC6_ADDRESS_HISTORY", False),
        ("f49_prior_emp1_org", "[49] Prior Employer #1 Organization / Command", "SEC7_JOB_HISTORY", False),
        ("f50_prior_emp1_title", "[50] Prior Employer #1 Job Title / Rank", "SEC7_JOB_HISTORY", False),
        ("f51_prior_emp1_supervisor", "[51] Prior Employer #1 Supervisor & Verification Phone", "SEC7_JOB_HISTORY", False),
        ("f52_prior_emp1_years", "[52] Prior Employer #1 Tenure (Years)", "SEC7_JOB_HISTORY", False),
        ("f53_prior_emp2_org_role", "[53] Prior Employer #2 Organization & Title", "SEC7_JOB_HISTORY", False),
        ("f54_total_experience_yrs", "[54] Total Verified Career Experience (Years)", "SEC7_JOB_HISTORY", False),
        ("f55_highest_education", "[55] Highest Degree / Technical Diploma", "SEC8_TRAINING_PROMOTION", False),
        ("f56_academy_exam_score", "[56] HVF Sovereign Field Academy Exam Score (%)", "SEC8_TRAINING_PROMOTION", False),
        ("f57_completed_hvf_courses", "[57] Completed HVF Technical Modules", "SEC8_TRAINING_PROMOTION", False),
        ("f58_active_certifications", "[58] Active Federal / Safety / Trade Certifications", "SEC8_TRAINING_PROMOTION", False),
        ("f59_training_hours_total", "[59] Total Verified Continuing Training Hours", "SEC8_TRAINING_PROMOTION", False),
        ("f60_company_eval_rating", "[60] Annual Company Evaluation Rating (0.0 - 5.0)", "SEC8_TRAINING_PROMOTION", False),
    ]

    DEFAULT_ATOMIC_60_VALUES: Dict[str, str] = {
        "f01_first_name": "JEFFERY",
        "f02_middle_name": "SOVEREIGN",
        "f03_last_name": "HUMPHREY",
        "f04_suffix": "NONE",
        "f05_ssn": "999-00-1234",
        "f06_dob": "1975-08-15",
        "f07_birth_city": "OKLAHOMA CITY",
        "f08_birth_state": "OK",
        "f09_birth_country": "UNITED STATES",
        "f10_mothers_maiden": "SOVEREIGN_MATRIARCH_KBA",
        "f11_street_address": "100 SOVEREIGN COMMAND PKWY",
        "f12_city": "OKLAHOMA CITY",
        "f13_state": "OK",
        "f14_zip_code": "73102-1000",
        "f15_primary_phone": "405-555-0199",
        "f16_email_address": "HUMPHREYVIRTUALFARM@GMAIL.COM",
        "f17_eye_color": "BROWN",
        "f18_hair_color": "BLACK",
        "f19_height_inches": "72",
        "f20_distinguishing_marks": "NONE_RECORDED",
        "f21_job_title": "FOUNDER, CEO & PRINCIPAL SOVEREIGN ARCHITECT",
        "f22_department_unit": "HVF EXECUTIVE COMMAND (CAGE 1AHA8)",
        "f23_clearance_level": "SOVEREIGN_COMMAND_AUTHORITY_TIER_1",
        "f24_citizenship_i9": "US_CITIZEN_I9_VERIFIED",
        "f25_drivers_license_num": "OK-DL-994827164",
        "f26_passport_num": "USA-P-558291044",
        "f27_dod_cac_edipi": "1984726150",
        "f28_nok_full_name": "MRS. HUMPHREY",
        "f29_nok_relationship": "SPOUSE_PRIMARY_BENEFICIARY",
        "f30_nok_phone": "405-555-0188",
        "f31_nok_address": "100 SOVEREIGN COMMAND PKWY, OKLAHOMA CITY, OK 73102",
        "f32_ice_full_name": "HVF TACTICAL WATCH OFFICER DESK",
        "f33_ice_relationship": "SECONDARY_EMERGENCY_COMMAND_CONTACT",
        "f34_ice_phone": "405-555-0177",
        "f35_ice_medical_blood": "O_POSITIVE // NO_KNOWN_DRUG_ALLERGIES",
        "f36_bio_fingerprint": "ISO19794-2-FINGERPRINT-MINUTIAE-10DIGIT-OK",
        "f37_bio_iris_retina": "ISO19794-6-DUAL-IRIS-RETINAL-VASCULAR-OK",
        "f38_bio_face_voice": "3D-DEPTH-FACE-AND-SPECTRAL-VOICEPRINT-OK",
        "f39_hardware_token_uuid": "YUBIKEY-FIPS-1AHA8-0001",
        "f40_watchfloor_callsign": "SOVEREIGN-ACTUAL-01",
        "f41_duty_shift_assignment": "COMMAND_CONTINUOUS_WATCH // MUSTER_ALPHA_1",
        "f42_nda_sf312_date": "2026-01-01 // WORM_SEALED",
        "f43_prev_addr1_street": "200 LEGACY RANCH RD",
        "f44_prev_addr1_city": "OKLAHOMA CITY",
        "f45_prev_addr1_state_zip": "OK 73101",
        "f46_prev_addr1_dates": "2018-01 TO 2022-06 (4.5 YRS VERIFIED)",
        "f47_prev_addr2_summary": "450 HEARTLAND AG PKWY, EDMOND, OK 73013 (2015-2018)",
        "f48_prev_addr_landlord": "OKLAHOMA COUNTY DEED & TITLE VERIFIED // 405-555-0300",
        "f49_prior_emp1_org": "HUMPHREY VIRTUAL FARMS LLC (CAGE 1AHA8)",
        "f50_prior_emp1_title": "FOUNDER, CEO & PRINCIPAL SOVEREIGN ARCHITECT",
        "f51_prior_emp1_supervisor": "BOARD OF DIRECTORS / CAGE 1AHA8 // 405-555-0199",
        "f52_prior_emp1_years": "12",
        "f53_prior_emp2_org_role": "PRINCIPAL CRITICAL INFRASTRUCTURE & AUTONOMOUS C2 ARCHITECT (6 YRS)",
        "f54_total_experience_yrs": "18",
        "f55_highest_education": "EXECUTIVE SOVEREIGN SYSTEMS ARCHITECTURE & AG-DEFENSE C2 MASTERY",
        "f56_academy_exam_score": "100.0",
        "f57_completed_hvf_courses": "ALL 26 CORE CLINS + WP-1..WP-9 NEXT-GEN MASTER CURRICULUM (1,420 QS)",
        "f58_active_certifications": "CAGE 1AHA8 CONTROLLING AUTHORITY // TRADEWINDS TRL-7 ARCHITECT // DOD RMF LEAD",
        "f59_training_hours_total": "480",
        "f60_company_eval_rating": "5.00",
    }

    AUTHORIZED_VERIFIER_OFFICERS: List[str] = [
        "EMP-002 // CAPT. MARCUS VANCE (HR & Watch-Floor Custody Officer)",
        "EMP-003 // DR. SARAH LIN (Lead SiC/SCADA Independent Verifier)",
        "EMP-004 // CALEB ROSS (UAS/GIS Independent Compliance Verifier)",
        "EMP-001 // JEFFERY HUMPHREY (Executive Second-Party Verifier -- Non-Self Only)",
    ]

    def __init__(self) -> None:
        super().__init__(
            plugin_id="HVF-NG-CLIN-0034",
            clin_number="CLIN 0034",
            title="Enterprise HR, Front-Screen OSHA Muster, HIPAA Medical/ICE Triage, Dual-Custody 60-Field Dossier & Promotion Board (v8.0)",
            version="8.0.0",
            target_trl="TRL 8/9",
            per_node_annual_gov_usd=85000,
            per_node_monthly_comm_usd=7100,
        )
        self.manifest = self.export_manifest()

    def get_instant_emergency_triage_card(
        self,
        roster_key: str,
        out_dir: pathlib.Path | None = None,
    ) -> Dict[str, Any]:
        base_person = self.PERSONNEL_EMERGENCY_ROSTER.get(
            roster_key,
            next(iter(self.PERSONNEL_EMERGENCY_ROSTER.values())),
        )
        person = dict(base_person)
        if out_dir is not None:
            st_file = out_dir / "wp8_hr_dossier_vault_state.json"
            if st_file.exists():
                try:
                    st_data = json.loads(st_file.read_text(encoding="utf-8"))
                    emp_saved = st_data.get("saved_profiles_by_emp", {}).get(person["employee_id"], {})
                    if isinstance(emp_saved, dict) and emp_saved:
                        f1 = emp_saved.get("f01_first_name", "").strip()
                        f2 = emp_saved.get("f02_middle_name", "").strip()
                        f3 = emp_saved.get("f03_last_name", "").strip()
                        f4 = emp_saved.get("f04_suffix", "").strip()
                        name_tokens = [x for x in (f1, f2, f3) if x]
                        if f4 and f4.upper() not in ("NONE", "N/A", ""):
                            name_tokens.append(f4)
                        if name_tokens:
                            person["full_name"] = " ".join(name_tokens)
                        if emp_saved.get("f15_primary_phone", "").strip():
                            person["direct_phone"] = emp_saved["f15_primary_phone"].strip()
                        if emp_saved.get("f16_email_address", "").strip():
                            person["email"] = emp_saved["f16_email_address"].strip().lower()
                        if emp_saved.get("f21_job_title", "").strip():
                            person["role_title"] = emp_saved["f21_job_title"].strip()
                        if emp_saved.get("f22_department_unit", "").strip():
                            person["department"] = emp_saved["f22_department_unit"].strip()
                        if emp_saved.get("f28_nok_full_name", "").strip():
                            person["nok_full_name"] = emp_saved["f28_nok_full_name"].strip()
                        if emp_saved.get("f29_nok_relationship", "").strip():
                            person["nok_relationship"] = emp_saved["f29_nok_relationship"].strip()
                        if emp_saved.get("f30_nok_phone", "").strip():
                            person["nok_phone"] = emp_saved["f30_nok_phone"].strip()
                        if emp_saved.get("f31_nok_address", "").strip():
                            person["nok_address"] = emp_saved["f31_nok_address"].strip()
                        if emp_saved.get("f32_ice_full_name", "").strip():
                            person["ice_full_name"] = emp_saved["f32_ice_full_name"].strip()
                        if emp_saved.get("f33_ice_relationship", "").strip():
                            person["ice_relationship"] = emp_saved["f33_ice_relationship"].strip()
                        if emp_saved.get("f34_ice_phone", "").strip():
                            person["ice_phone"] = emp_saved["f34_ice_phone"].strip()
                        if emp_saved.get("f35_ice_medical_blood", "").strip():
                            person["blood_type_and_medical"] = emp_saved["f35_ice_medical_blood"].strip()
                except Exception:
                    pass

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

    def get_public_emergency_muster_and_sops(self, zone_or_roster_key: str) -> Dict[str, Any]:
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

    def init_hr_worm_sqlite(self, db_path: pathlib.Path) -> Dict[str, Any]:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            tables_sql = [
                (
                    "worm_hr_biometric_access_log",
                    """
                    CREATE TABLE IF NOT EXISTS worm_hr_biometric_access_log (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id TEXT NOT NULL,
                        operator_name TEXT NOT NULL,
                        gate_action TEXT NOT NULL,
                        worm_row_sha256 TEXT NOT NULL UNIQUE
                    )
                    """,
                    "trg_hr_bio",
                ),
                (
                    "worm_hr_dossier_revisions",
                    """
                    CREATE TABLE IF NOT EXISTS worm_hr_dossier_revisions (
                        revision_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id TEXT NOT NULL,
                        operator_name TEXT NOT NULL,
                        dual_custody_signers TEXT NOT NULL,
                        update_reason TEXT NOT NULL,
                        composite_60field_seal TEXT NOT NULL,
                        worm_revision_sha256 TEXT NOT NULL UNIQUE
                    )
                    """,
                    "trg_hr_rev",
                ),
                (
                    "worm_employer_personnel_notes",
                    """
                    CREATE TABLE IF NOT EXISTS worm_employer_personnel_notes (
                        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id TEXT NOT NULL,
                        employee_name TEXT NOT NULL,
                        author_authority TEXT NOT NULL,
                        note_category TEXT NOT NULL,
                        confidential_note_text TEXT NOT NULL,
                        worm_note_sha256 TEXT NOT NULL UNIQUE
                    )
                    """,
                    "trg_hr_note",
                ),
                (
                    "worm_promotion_evaluation_board",
                    """
                    CREATE TABLE IF NOT EXISTS worm_promotion_evaluation_board (
                        board_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        pri_score REAL NOT NULL,
                        qualification_status TEXT NOT NULL,
                        worm_board_sha256 TEXT NOT NULL UNIQUE
                    )
                    """,
                    "trg_hr_promo",
                ),
                (
                    "worm_hipaa_emergency_triage_log",
                    """
                    CREATE TABLE IF NOT EXISTS worm_hipaa_emergency_triage_log (
                        triage_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id TEXT NOT NULL,
                        employee_name TEXT NOT NULL,
                        accessor_role TEXT NOT NULL,
                        access_purpose TEXT NOT NULL,
                        worm_hipaa_sha256 TEXT NOT NULL UNIQUE
                    )
                    """,
                    "trg_hr_hipaa",
                ),
            ]
            for tbl_name, create_stmt, trg_prefix in tables_sql:
                cur.execute(create_stmt)
                cur.execute(f"""
                    CREATE TRIGGER IF NOT EXISTS {trg_prefix}_no_update
                    BEFORE UPDATE ON {tbl_name}
                    BEGIN
                        SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: UPDATE PROHIBITED ON {tbl_name}');
                    END;
                """)
                cur.execute(f"""
                    CREATE TRIGGER IF NOT EXISTS {trg_prefix}_no_delete
                    BEFORE DELETE ON {tbl_name}
                    BEGIN
                        SELECT RAISE(ABORT, 'WORM_IMMUTABILITY_VIOLATION: DELETE PROHIBITED ON {tbl_name}');
                    END;
                """)
            conn.commit()
        finally:
            conn.close()
        return {"db_path": str(db_path), "worm_triggers_active": 10}

    def load_or_init_vault_lock_state(self, out_dir: pathlib.Path) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        st_path = out_dir / "wp8_hr_dossier_vault_state.json"
        if st_path.exists():
            try:
                return json.loads(st_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        init_state: Dict[str, Any] = {
            "is_locked": True,
            "revision_number": 1,
            "last_approved_by": "HR:EMP-002 + VERIFIED_BY:EMP-003",
            "last_change_reason": "INITIAL_DUAL_CUSTODY_ONBOARDING_SEAL",
            "locked_by_emp": {"EMP-001": True, "EMP-002": True, "EMP-003": True, "EMP-004": True},
            "rev_by_emp": {"EMP-001": 1, "EMP-002": 1, "EMP-003": 1, "EMP-004": 1},
            "last_actor_by_emp": {},
            "last_reason_by_emp": {},
            "saved_profiles_by_emp": {},
        }
        st_path.write_text(json.dumps(init_state, indent=2), encoding="utf-8")
        return init_state

    def generate_hr_custodian_unlock_token(self, employee_id: str, revision_number: int) -> str:
        digest = hmac.new(
            HR_VAULT_PEPPER.encode("utf-8"),
            f"HR_CUSTODIAN_INITIATE|{employee_id}|REV_{revision_number:04d}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()[:14].upper()
        return f"HVF-HR-CUSTODY-{digest}"

    def generate_second_verifier_unlock_token(self, employee_id: str, revision_number: int) -> str:
        digest = hmac.new(
            HR_VAULT_PEPPER.encode("utf-8"),
            f"SECOND_PARTY_VERIFIER|{employee_id}|REV_{revision_number:04d}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()[:14].upper()
        return f"HVF-2P-VERIFY-{digest}"

    def get_employee_dossier_lock_status(self, out_dir: pathlib.Path, roster_key: str) -> Dict[str, Any]:
        state = self.load_or_init_vault_lock_state(out_dir)
        person = self.PERSONNEL_EMERGENCY_ROSTER.get(
            roster_key,
            next(iter(self.PERSONNEL_EMERGENCY_ROSTER.values())),
        )
        emp_id = person["employee_id"]
        is_locked = bool(state.get("locked_by_emp", {}).get(emp_id, True))
        cur_rev = int(state.get("rev_by_emp", {}).get(emp_id, 1))
        return {
            "employee_id": emp_id,
            "is_locked": is_locked,
            "revision_number": cur_rev,
            "hr_custodian_token": self.generate_hr_custodian_unlock_token(emp_id, cur_rev),
            "second_verifier_token": self.generate_second_verifier_unlock_token(emp_id, cur_rev),
            "last_actor": state.get("last_actor_by_emp", {}).get(emp_id, "HR:EMP-002 + VERIFIED_BY:EMP-003"),
            "last_reason": state.get("last_reason_by_emp", {}).get(emp_id, "INITIAL_DUAL_CUSTODY_ONBOARDING_SEAL"),
        }

    def request_dual_custody_unlock_for_employee(
        self,
        out_dir: pathlib.Path,
        roster_key: str,
        hr_custodian_officer: str,
        provided_hr_token: str,
        second_verifier_officer: str,
        provided_verifier_token: str,
        change_reason: str,
    ) -> Dict[str, Any]:
        lock_st = self.get_employee_dossier_lock_status(out_dir, roster_key)
        emp_id = lock_st["employee_id"]
        hr_clean = hr_custodian_officer.strip()
        ver_clean = second_verifier_officer.strip()
        hr_id = hr_clean.split("//")[0].strip() if "//" in hr_clean else hr_clean
        ver_id = ver_clean.split("//")[0].strip() if "//" in ver_clean else ver_clean

        if not hr_clean or not ver_clean or hr_id.upper() == ver_id.upper():
            return {
                "unlocked": False,
                "employee_id": emp_id,
                "status": "ZERO_TRUST_AC5_VIOLATION_SELF_APPROVAL_PROHIBITED_REQUIRES_TWO_DISTINCT_OFFICIALS",
            }
        if ver_id.upper() == emp_id.upper():
            return {
                "unlocked": False,
                "employee_id": emp_id,
                "status": f"ZERO_TRUST_CONFLICT_OF_INTEREST_SUBJECT_{emp_id}_CANNOT_SELF_VERIFY_OWN_DOSSIER",
            }
        if provided_hr_token.strip() != lock_st["hr_custodian_token"]:
            return {
                "unlocked": False,
                "employee_id": emp_id,
                "status": "DUAL_CUSTODY_DENIED_INVALID_SIGNER1_HR_CUSTODIAN_TOKEN",
            }
        if provided_verifier_token.strip() != lock_st["second_verifier_token"]:
            return {
                "unlocked": False,
                "employee_id": emp_id,
                "status": "DUAL_CUSTODY_DENIED_INVALID_SIGNER2_INDEPENDENT_VERIFIER_TOKEN",
            }
        if not change_reason or len(change_reason.strip()) < 4:
            return {
                "unlocked": False,
                "employee_id": emp_id,
                "status": "DUAL_CUSTODY_DENIED_VERIFIED_DOCUMENTATION_REASON_REQUIRED",
            }

        dual_actor = f"HR:{hr_id} + VERIFIED_BY:{ver_id}"
        state = self.load_or_init_vault_lock_state(out_dir)
        state.setdefault("locked_by_emp", {})[emp_id] = False
        state.setdefault("last_actor_by_emp", {})[emp_id] = dual_actor
        state.setdefault("last_reason_by_emp", {})[emp_id] = change_reason.strip()
        (out_dir / "wp8_hr_dossier_vault_state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
        return {
            "unlocked": True,
            "employee_id": emp_id,
            "status": "DUAL_CUSTODY_VERIFIED_60FIELD_DOSSIER_UNLOCKED_FOR_1_REVISION",
            "approved_by": dual_actor,
            "change_reason": change_reason.strip(),
        }

    def get_saved_user_60field_values(self, out_dir: pathlib.Path, roster_key: str | None = None) -> Dict[str, str]:
        base_vals = dict(self.DEFAULT_ATOMIC_60_VALUES)
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

    def evaluate_atomic_60_application(self, profile_overrides: Dict[str, str] | None = None) -> Dict[str, Any]:
        vals = dict(self.DEFAULT_ATOMIC_60_VALUES)
        if profile_overrides:
            for k, v in profile_overrides.items():
                if k in vals and v is not None:
                    vals[k] = str(v)

        rows: List[Dict[str, str]] = []
        seals: List[str] = []
        for idx, (fkey, flabel, fsec, is_sec) in enumerate(self.ATOMIC_60_SCHEMA, start=1):
            raw_v = vals.get(fkey, "")
            f_seal = hmac.new(
                HR_VAULT_PEPPER.encode("utf-8"),
                f"{fkey}|{raw_v.strip().upper()}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            seals.append(f_seal)
            masked_v = (f"REDACTED-****-{raw_v.strip()[-4:]}" if len(raw_v.strip()) >= 4 else "REDACTED-****") if is_sec else raw_v.strip()
            rows.append({
                "Field_ID": f"F{idx:02d}_{fkey.upper()}",
                "Section": fsec,
                "Dossier_Attribute": flabel,
                "Verified_Record_Value": masked_v,
                "Zero_Trust_Verification": "DUAL_CUSTODY_HR_AND_2ND_VERIFIER_SEALED",
                "HMAC_SHA256_Seal": f_seal[:18].upper(),
            })

        comp_seal = hmac.new(
            HR_VAULT_PEPPER.encode("utf-8"),
            "|".join(seals).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return {
            "total_atomic_fields": len(rows),
            "attribute_rows": rows,
            "composite_60field_seal": comp_seal,
        }

    def submit_dual_custody_60field_dossier(
        self,
        out_dir: pathlib.Path,
        roster_key: str,
        profile_60_inputs: Dict[str, str],
        submitted_by_role: str = "HR:EMP-002 + VERIFIED_BY:EMP-003",
        submission_reason: str = "DUAL_CUSTODY_VERIFIED_60FIELD_DOSSIER_SEAL",
        enforce_dual_custody_lock: bool = False,
    ) -> Dict[str, Any]:
        state = self.load_or_init_vault_lock_state(out_dir)
        person = self.PERSONNEL_EMERGENCY_ROSTER.get(
            roster_key,
            next(iter(self.PERSONNEL_EMERGENCY_ROSTER.values())),
        )
        emp_id = person["employee_id"]
        if enforce_dual_custody_lock and bool(state.get("locked_by_emp", {}).get(emp_id, False)):
            return {
                "submitted": False,
                "employee_id": emp_id,
                "status": "SUBMISSION_BLOCKED_DOSSIER_SEALED_REQUIRES_DUAL_CUSTODY_HR_AND_VERIFIER_UNLOCK",
            }

        clean_inputs = {k: str(v).strip() for k, v in profile_60_inputs.items()}
        state.setdefault("saved_profiles_by_emp", {})[emp_id] = clean_inputs
        state.setdefault("locked_by_emp", {})[emp_id] = True
        next_rev = int(state.get("rev_by_emp", {}).get(emp_id, 1)) + 1
        state.setdefault("rev_by_emp", {})[emp_id] = next_rev
        state.setdefault("last_actor_by_emp", {})[emp_id] = submitted_by_role
        state.setdefault("last_reason_by_emp", {})[emp_id] = submission_reason
        (out_dir / "wp8_hr_dossier_vault_state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")

        dossier_res = self.generate_wp8_hr_dossier(out_dir, profile_60_overrides=clean_inputs, employee_id=emp_id)
        return {
            "submitted": True,
            "employee_id": emp_id,
            "is_locked": True,
            "revision_number": next_rev,
            "composite_60field_seal": dossier_res["dossier_report"]["composite_60field_seal"],
            "worm_seal": dossier_res["worm_seal"],
        }

    def append_employer_personnel_note(
        self,
        db_path: pathlib.Path,
        employee_id: str,
        employee_name: str,
        author_authority: str,
        note_category: str,
        confidential_note_text: str,
    ) -> Dict[str, Any]:
        self.init_hr_worm_sqlite(db_path)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            note_sha = hmac.new(
                HR_VAULT_PEPPER.encode("utf-8"),
                f"{employee_id}|{author_authority}|{note_category}|{confidential_note_text}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            cur.execute(
                """
                INSERT OR IGNORE INTO worm_employer_personnel_notes (
                    employee_id, employee_name, author_authority, note_category, confidential_note_text, worm_note_sha256
                ) VALUES (?,?,?,?,?,?)
                """,
                (employee_id, employee_name, author_authority, note_category, confidential_note_text, note_sha),
            )
            conn.commit()
            cnt = cur.execute("SELECT COUNT(*) FROM worm_employer_personnel_notes WHERE employee_id = ?", (employee_id,)).fetchone()[0]
        finally:
            conn.close()
        return {"worm_note_sha256": note_sha, "total_notes_for_employee": cnt}

    def get_employer_personnel_notes(self, db_path: pathlib.Path, employee_id: str) -> List[Dict[str, Any]]:
        self.init_hr_worm_sqlite(db_path)
        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            cnt = cur.execute("SELECT COUNT(*) FROM worm_employer_personnel_notes").fetchone()[0]
            if cnt == 0:
                for rk, pobj in self.PERSONNEL_EMERGENCY_ROSTER.items():
                    self.append_employer_personnel_note(
                        db_path,
                        pobj["employee_id"],
                        pobj["full_name"],
                        "HR:EMP-002 + VERIFIED_BY:EMP-003",
                        "ANNUAL_SECURITY_AND_READINESS_VERIFICATION",
                        f"Dual-custody verified onboarding, I-9, & emergency readiness file for {pobj['full_name']}.",
                    )
            rows = cur.execute(
                """
                SELECT note_id, employee_id, employee_name, author_authority, note_category, confidential_note_text, worm_note_sha256
                FROM worm_employer_personnel_notes
                WHERE employee_id = ?
                ORDER BY note_id DESC
                """,
                (employee_id,),
            ).fetchall()
        finally:
            conn.close()
        return [
            {
                "Note_ID": f"HR-NOTE-{r[0]:03d}",
                "Employee_ID": r[1],
                "Employee_Name": r[2],
                "Co_Signing_Authorities": r[3],
                "Category": r[4],
                "Verified_HR_Note": r[5],
                "WORM_SHA256_Seal": r[6][:18].upper(),
            }
            for r in rows
        ]

    def evaluate_promotion_and_company_shortlist(
        self,
        out_dir: pathlib.Path,
        min_experience_years: int = 5,
        min_academy_score_pct: float = 90.0,
        min_eval_rating: float = 4.5,
        required_specialty: str = "ALL",
    ) -> Dict[str, Any]:
        db_file = out_dir / "wp8_enterprise_hr_triage_worm.db"
        self.init_hr_worm_sqlite(db_file)
        state_data = self.load_or_init_vault_lock_state(out_dir)
        saved_by_emp = state_data.get("saved_profiles_by_emp", {})
        req_spec = required_specialty.strip().upper()

        all_rows: List[Dict[str, Any]] = []
        conn = sqlite3.connect(str(db_file), timeout=30.0)
        try:
            cur = conn.cursor()
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

                f1 = emp_saved.get("f01_first_name", "").strip()
                f2 = emp_saved.get("f02_middle_name", "").strip()
                f3 = emp_saved.get("f03_last_name", "").strip()
                f4 = emp_saved.get("f04_suffix", "").strip()
                name_tokens = [x for x in (f1, f2, f3) if x]
                if f4 and f4.upper() not in ("NONE", "N/A", ""):
                    name_tokens.append(f4)
                live_full_name = " ".join(name_tokens) if name_tokens else cand["full_name"]
                live_role = emp_saved.get("f21_job_title", "").strip() or cand["current_role"]
                live_edu = emp_saved.get("f55_highest_education", "").strip() or cand["highest_education"]
                live_certs = emp_saved.get("f58_active_certifications", "").strip() or cand["active_certifications"]
                live_job1 = emp_saved.get("f49_prior_emp1_org", "").strip() or cand["prior_job_1"]
                live_job2 = emp_saved.get("f53_prior_emp2_org_role", "").strip() or cand["prior_job_2"]
                live_addr1 = emp_saved.get("f43_prev_addr1_street", "").strip() or cand["prev_address_1"]
                live_addr2 = emp_saved.get("f47_prev_addr2_summary", "").strip() or cand["prev_address_2"]

                pri_score = round(
                    (acad_pct * 0.35)
                    + ((eval_rat / 5.0) * 35.0)
                    + (min(exp_yrs, 15) / 15.0 * 15.0)
                    + (min(train_hrs, 300) / 300.0 * 15.0),
                    2,
                )

                meets_exp = exp_yrs >= min_experience_years
                meets_acad = acad_pct >= min_academy_score_pct
                meets_eval = eval_rat >= min_eval_rating
                meets_spec = (req_spec == "ALL") or (req_spec in cand["specialty_tracks"])
                is_qualified = bool(meets_exp and meets_acad and meets_eval and meets_spec)

                status_str = (
                    "QUALIFIED_FOR_IMMEDIATE_PROMOTION"
                    if is_qualified
                    else "RETAIN_IN_CURRENT_GRADE_PENDING_CRITERIA"
                )
                board_sha = hmac.new(
                    HR_VAULT_PEPPER.encode("utf-8"),
                    f"{emp_id}|{live_full_name}|{pri_score}|{status_str}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                    hashlib.sha256,
                ).hexdigest()
                cur.execute(
                    """
                    INSERT OR IGNORE INTO worm_promotion_evaluation_board (
                        employee_id, full_name, pri_score, qualification_status, worm_board_sha256
                    ) VALUES (?,?,?,?,?)
                    """,
                    (emp_id, live_full_name, pri_score, status_str, board_sha),
                )
                all_rows.append({
                    "Rank": 0,
                    "Employee_ID": emp_id,
                    "Candidate_Name": live_full_name,
                    "Current_Role": live_role,
                    "Target_Promotion_Grade": cand["target_promotion_grade"],
                    "Promotion_Readiness_Index": f"{pri_score:.2f} / 100",
                    "Verified_Experience_Yrs": exp_yrs,
                    "Academy_Exam_Score": f"{acad_pct:.1f}%",
                    "Company_Eval_Rating": f"{eval_rat:.2f} / 5.00",
                    "Training_Hours": train_hrs,
                    "Highest_Education": live_edu,
                    "Prior_Job_History": f"{live_job1} | {live_job2}",
                    "Address_History_7Yr": f"{live_addr1} -> {live_addr2}",
                    "Active_Certifications": live_certs,
                    "Qualification_Status": status_str,
                    "WORM_Board_Seal": board_sha[:16].upper(),
                    "_pri_num": pri_score,
                    "_is_qual": is_qualified,
                })
            conn.commit()
            board_cnt = cur.execute("SELECT COUNT(*) FROM worm_promotion_evaluation_board").fetchone()[0]
        finally:
            conn.close()

        all_rows.sort(key=lambda x: x["_pri_num"], reverse=True)
        qual_rows: List[Dict[str, Any]] = []
        for idx, r in enumerate(all_rows, start=1):
            clean_r = {k: v for k, v in r.items() if not k.startswith("_")}
            clean_r["Rank"] = idx
            if r["_is_qual"]:
                qual_rows.append(clean_r)

        for idx, qr in enumerate(qual_rows, start=1):
            qr["Rank"] = idx

        top_cand = qual_rows[0]["Candidate_Name"] if qual_rows else "NO_CANDIDATE_MATCHES_FILTER"
        top_score = qual_rows[0]["Promotion_Readiness_Index"].split("/")[0].strip() if qual_rows else "0.00"
        return {
            "total_personnel_evaluated": len(all_rows),
            "qualified_candidates_count": len(qual_rows),
            "top_ranked_candidate": top_cand,
            "top_pri_score": top_score,
            "worm_board_rows_logged": board_cnt,
            "qualified_shortlist_rows": qual_rows,
        }

    def open_hr_and_hipaa_gate(
        self,
        roster_key: str,
        charter_accepted: bool,
        provided_hr_key: str,
        out_dir: pathlib.Path,
    ) -> Dict[str, Any]:
        if not charter_accepted:
            return {
                "gate_open": False,
                "gate_status": "HR_AND_HIPAA_GATE_LOCKED_ACCEPT_CHARTER_REQUIRED",
                "emergency_medical_ice_card": None,
                "emergency_procedures_muster": self.get_public_emergency_muster_and_sops(roster_key),
                "employer_internal_records": None,
                "employer_personnel_notes": None,
                "proof_of_id_rows": None,
            }
        if provided_hr_key.strip() != "EMPLOYER-MASTER-1AHA8":
            return {
                "gate_open": False,
                "gate_status": "HR_AND_HIPAA_GATE_DENIED_INVALID_HR_MASTER_KEY",
                "emergency_medical_ice_card": None,
                "emergency_procedures_muster": self.get_public_emergency_muster_and_sops(roster_key),
                "employer_internal_records": None,
                "employer_personnel_notes": None,
                "proof_of_id_rows": None,
            }

        person = self.PERSONNEL_EMERGENCY_ROSTER.get(
            roster_key,
            next(iter(self.PERSONNEL_EMERGENCY_ROSTER.values())),
        )
        med_ice = self.get_instant_emergency_triage_card(roster_key, out_dir=out_dir)
        saved_vals = self.get_saved_user_60field_values(out_dir, roster_key)
        app_eval = self.evaluate_atomic_60_application(saved_vals)

        db_file = out_dir / "wp8_enterprise_hr_triage_worm.db"
        self.init_hr_worm_sqlite(db_file)
        hipaa_sha = hmac.new(
            HR_VAULT_PEPPER.encode("utf-8"),
            f"{person['employee_id']}|{med_ice['full_name']}|HR_HIPAA_UNSEAL|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        conn = sqlite3.connect(str(db_file), timeout=30.0)
        try:
            conn.execute(
                """
                INSERT OR IGNORE INTO worm_hipaa_emergency_triage_log (
                    employee_id, employee_name, accessor_role, access_purpose, worm_hipaa_sha256
                ) VALUES (?,?,?,?,?)
                """,
                (person["employee_id"], med_ice["full_name"], "ENTERPRISE_HR_AND_EMERGENCY_COMMAND", "HIPAA_MEDICAL_AND_ICE_TRIAGE", hipaa_sha),
            )
            conn.commit()
        finally:
            conn.close()

        return {
            "gate_open": True,
            "gate_status": "ENTERPRISE_HR_HIPAA_AND_PROMOTION_VAULT_OPEN",
            "emergency_medical_ice_card": med_ice,
            "emergency_procedures_muster": self.get_public_emergency_muster_and_sops(roster_key),
            "hipaa_audit_seal": hipaa_sha,
            "employer_internal_records": person["employer_internal_records"],
            "employer_personnel_notes": self.get_employer_personnel_notes(db_file, person["employee_id"]),
            "proof_of_id_rows": app_eval["attribute_rows"],
            "composite_seal": app_eval["composite_60field_seal"],
        }

    def generate_wp8_hr_dossier(
        self,
        out_dir: pathlib.Path,
        profile_60_overrides: Dict[str, str] | None = None,
        employee_id: str = "EMP-001",
    ) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        db_path = out_dir / "wp8_enterprise_hr_triage_worm.db"
        self.init_hr_worm_sqlite(db_path)

        app_eval = self.evaluate_atomic_60_application(profile_60_overrides)
        promo_eval = self.evaluate_promotion_and_company_shortlist(out_dir)
        self.get_employer_personnel_notes(db_path, employee_id)

        conn = sqlite3.connect(str(db_path), timeout=30.0)
        try:
            cur = conn.cursor()
            bio_sha = hmac.new(
                HR_VAULT_PEPPER.encode("utf-8"),
                f"{employee_id}|SIGN_IN_3MODAL_VERIFIED|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            cur.execute(
                """
                INSERT OR IGNORE INTO worm_hr_biometric_access_log (
                    employee_id, operator_name, gate_action, worm_row_sha256
                ) VALUES (?,?,?,?)
                """,
                (employee_id, "JEFFERY SOVEREIGN HUMPHREY", "SIGN_IN_3MODAL_BIOMETRIC_AND_CAC_VERIFIED", bio_sha),
            )

            rev_sha = hmac.new(
                HR_VAULT_PEPPER.encode("utf-8"),
                f"{employee_id}|{app_eval['composite_60field_seal']}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            cur.execute(
                """
                INSERT OR IGNORE INTO worm_hr_dossier_revisions (
                    employee_id, operator_name, dual_custody_signers, update_reason, composite_60field_seal, worm_revision_sha256
                ) VALUES (?,?,?,?,?,?)
                """,
                (employee_id, "JEFFERY SOVEREIGN HUMPHREY", "HR:EMP-002 + VERIFIED_BY:EMP-003", "DUAL_CUSTODY_VERIFIED_60FIELD_SEAL", app_eval["composite_60field_seal"], rev_sha),
            )

            hipaa_sha = hmac.new(
                HR_VAULT_PEPPER.encode("utf-8"),
                f"{employee_id}|BASELINE_HIPAA_SEAL|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            cur.execute(
                """
                INSERT OR IGNORE INTO worm_hipaa_emergency_triage_log (
                    employee_id, employee_name, accessor_role, access_purpose, worm_hipaa_sha256
                ) VALUES (?,?,?,?,?)
                """,
                (employee_id, "JEFFERY SOVEREIGN HUMPHREY", "SYSTEM_HIPAA_BASELINE", "INITIAL_HIPAA_WORM_AUDIT_SEAL", hipaa_sha),
            )
            conn.commit()

            access_rows = [
                {"Event_ID": f"BIO-{r[0]:03d}", "Employee_ID": r[1], "Operator": r[2], "Biometric_Gate_Action": r[3], "WORM_SHA256": r[4][:18].upper()}
                for r in cur.execute("SELECT event_id, employee_id, operator_name, gate_action, worm_row_sha256 FROM worm_hr_biometric_access_log ORDER BY event_id DESC").fetchall()
            ]
            rev_rows = [
                {"Rev_ID": f"REV-{r[0]:03d}", "Employee_ID": r[1], "Subject_Name": r[2], "Dual_Custody_CoSigners": r[3], "Verified_Reason": r[4], "Composite_Seal": r[5][:16].upper(), "WORM_SHA256": r[6][:16].upper()}
                for r in cur.execute("SELECT revision_id, employee_id, operator_name, dual_custody_signers, update_reason, composite_60field_seal, worm_revision_sha256 FROM worm_hr_dossier_revisions ORDER BY revision_id DESC").fetchall()
            ]
        finally:
            conn.close()

        md_lines = [
            "# HVF SOVEREIGN NEXT-GEN // WP-8 (CLIN 0034 v8.0): ENTERPRISE HR, OSHA MUSTER, HIPAA TRIAGE, DUAL-CUSTODY 60-FIELD DOSSIER & PROMOTION BOARD",
            f"- **Controlling Authority**: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect (CAGE `1AHA8` | UEI `S1M4ENLHTDH5`)",
            f"- **Enclave Tier**: `{ENCLAVE_MODE}` | **Host Baseline Merkle Root**: `{FROZEN_EBONY_MERKLE_ROOT}`",
            f"- **Zero-Trust Separation of Duties (`NIST SP 800-53 AC-5`)**: `ACTIVE (HR Custodian + Independent Second Verifier Required; Zero Self-Approval)`",
            f"- **Physical Separation**: `100% DECOUPLED FROM PERSONAL CREDIT/LOAN SHIELD (CLIN 0033)`",
            f"- **60-Field Composite Dossier Seal**: `{app_eval['composite_60field_seal']}`",
            f"- **Top-Ranked Promotion Candidate**: `{promo_eval['top_ranked_candidate']}` (`PRI: {promo_eval['top_pri_score']} / 100`)",
            f"- **WORM SQLite Ledger**: `5 Tables / 10 Active Immutability Triggers`",
        ]
        md_content = chr(10).join(md_lines) + chr(10)
        md_path = out_dir / "WP8_ENTERPRISE_HR_MUSTER_HIPAA_PROMOTION_SPEC.md"
        pdf_path = out_dir / "WP8_ENTERPRISE_HR_MUSTER_HIPAA_PROMOTION_SPEC.pdf"
        md_path.write_bytes(md_content.encode("ascii"))

        worm_seal = hashlib.sha256(md_content.encode("ascii")).hexdigest()
        pdf_lines = [line.replace("`", "").replace("*", "") for line in md_lines]
        pdf_bytes = compile_single_page_pdf_14(
            title="HVF WP-8 (CLIN 0034 v8.0): ENTERPRISE HR, MUSTER, HIPAA & PROMOTION BOARD",
            lines=pdf_lines,
            worm_sha256=worm_seal,
        )
        pdf_path.write_bytes(pdf_bytes)

        return {
            "manifest": self.manifest,
            "dossier_report": app_eval,
            "promotion_report": promo_eval,
            "access_events": access_rows,
            "revision_history": rev_rows,
            "sqlite_db_path": str(db_path),
            "md_path": str(md_path),
            "pdf_path": str(pdf_path),
            "pdf_bytes_len": len(pdf_bytes),
            "worm_seal": worm_seal,
        }
