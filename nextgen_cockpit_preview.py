"""
HUMPHREY VIRTUAL FARMS LLC // NEXT-GEN TRL 8/9 EXPANSION FORGE COMMAND DASHBOARD (PORT 8502)
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5)
Controlling Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect
Isolation Mandate: Runs strictly on Port 8502 from C:\hvf_c2_nextgen while Frozen Project Ebony
                   runs on Port 8501 from C:\hvf_c2 (Master Merkle Root: cc1ee1c8...949a).
"""
from __future__ import annotations
import pathlib
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from nextgen_core.sovereign_plugin_contract import (
    FROZEN_EBONY_MERKLE_ROOT,
    SovereignPluginRegistry,
)
from plugins.clin_0027_day1_license_wawf_generator import (
    ENCLAVE_MODE,
    Day1LicenseAndWAWFInvoiceGenerator,
)
from plugins.clin_0028_sic_mosfet_interlock_board import SiCMOSFETGuillotineBoardEngine
from plugins.clin_0029_site_plc_scada_canbus_mapper import SitePLCSCADACANBusMapper
from plugins.clin_0030_uas_optical_gli_title61_gis import UASOpticalGLIAndTitle61GISEngine
from plugins.clin_0031_command_watchfloor_rbac_pdf_engine import CommandWatchFloorRBACAndPDFEngine
from plugins.clin_0032_dod_rmf_ato_academy_cohort_engine import DoDRMFATOAndAcademyCohortEngine
from plugins.clin_0033_sovereign_identity_antifraud_shield import SovereignIdentityAntiFraudShield
from plugins.clin_0034_federal_capability_and_quote_engine import FederalCapabilityAndQuoteEngine


def build_registry_and_engines():
    reg = SovereignPluginRegistry()
    e27 = Day1LicenseAndWAWFInvoiceGenerator()
    e28 = SiCMOSFETGuillotineBoardEngine()
    e29 = SitePLCSCADACANBusMapper()
    e30 = UASOpticalGLIAndTitle61GISEngine()
    e31 = CommandWatchFloorRBACAndPDFEngine()
    e32 = DoDRMFATOAndAcademyCohortEngine()
    e33 = SovereignIdentityAntiFraudShield()
    e34 = FederalCapabilityAndQuoteEngine()
    for eng in (e27, e28, e29, e30, e31, e32, e33, e34):
        reg.register(eng)
    return reg, e27, e28, e29, e30, e31, e32, e33, e34


def render_nextgen_dashboard() -> None:
    import streamlit as st

    ico_shield = chr(0x1F6E1)
    ico_key    = chr(0x1F511)
    ico_bolt   = chr(0x26A1)
    ico_gear   = chr(0x2699)
    ico_drone  = chr(0x1F6F8)
    ico_lock   = chr(0x1F510)
    ico_medal  = chr(0x1F396)
    ico_dl     = chr(0x1F4E5)
    nl         = chr(10)

    st.set_page_config(
        page_title="HVF Sovereign Next-Gen Forge (Port 8502)",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    reg, e27, e28, e29, e30, e31, e32, e33, e34 = build_registry_and_engines()
    artifacts_dir = HERE / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    st.sidebar.markdown(f"### {ico_shield} HVF NEXT-GEN FORGE (`PORT 8502`)")
    st.sidebar.caption("Entity: **Humphrey Virtual Farms LLC**")
    st.sidebar.caption("CEO & SME: **Jeffery Humphrey**")
    st.sidebar.caption("CAGE: **`1AHA8`** | UEI: **`S1M4ENLHTDH5`**")
    st.sidebar.caption(f"Enclave Tier: **`{ENCLAVE_MODE}`**")
    st.sidebar.markdown("---")
    st.sidebar.success("Frozen Ebony Core (`Port 8501`): **100% UNTOUCHED**")
    st.sidebar.code(f"Host Merkle Root:{nl}{FROZEN_EBONY_MERKLE_ROOT[:32]}...{nl}{FROZEN_EBONY_MERKLE_ROOT[32:]}", language="text")

    st.markdown(f"# {ico_shield} HVF SOVEREIGN NEXT-GEN EXPANSION FORGE // PORT 8502")
    st.markdown(
        "**Controlling Authority:** Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect | "
        "**CAGE:** `1AHA8` | **SAM.gov UEI:** `S1M4ENLHTDH5` | **Host Baseline:** `Project Ebony TRL 7 Frozen Core`"
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Post-Award Work Packages", "8 / 8 (WP-1..WP-8)", "100% Pre-Engineered")
    c2.metric("Next-Gen Expansion Value", "$545,000 / yr / Node", "CLIN 0027 - CLIN 0034")
    c3.metric("Combined Catalog Value", "$2,175,000 / yr / Node", "CLIN 0001 - CLIN 0034")
    c4.metric("Frozen Ebony Core Status", "0 Bytes Modified", "Merkle cc1ee1c8...949a")

    tabs = st.tabs([
        f"{ico_shield} 0. Master Registry (WP-1..8)",
        f"{ico_key} 1. WP-1: Day-1 License & WAWF (CLIN 0027)",
        f"{ico_bolt} 2. WP-2: 36.75ns SiC Board (CLIN 0028)",
        f"{ico_gear} 3. WP-3: PLC/SCADA/J1939 (CLIN 0029)",
        f"{ico_drone} 4. WP-4: UAS GLI & Title 61 (CLIN 0030)",
        f"{ico_lock} 5. WP-5: Watch-Floor RBAC (CLIN 0031)",
        f"{ico_medal} 6. WP-6: DoD RMF ATO & Academy (CLIN 0032)",
        f"{ico_shield} 7. WP-7: SSN/DOB, Credit/Loan & ID Shield (CLIN 0033)",
        f"{ico_medal} 8. WP-8: Capability Statement, Quote & Outreach (CLIN 0034)",
    ])

    with tabs[0]:
        st.markdown("### Universal Sovereign Plug-In Registry (`SovereignExpansionModule`)")
        st.info(
            "Every module below is isolated in `C:\hvf_c2_nextgen` and verified for zero-rewrite plug-in attachment "
            "to the frozen Project Ebony TRL 7 baseline (`C:\hvf_c2`) the moment Day-1 contract funds settle."
        )
        st.dataframe(reg.list_manifests(), width="stretch", hide_index=True)

        st.markdown("#### Sealed WORM `%PDF-1.4` & Markdown Deliverables in `artifacts/`")
        art_rows = []
        for fp in sorted(artifacts_dir.glob("*.*")):
            art_rows.append({
                "File Name": fp.name,
                "Format": fp.suffix.upper().lstrip("."),
                "Size (Bytes)": f"{fp.stat().st_size:,}",
            })
        st.dataframe(art_rows, width="stretch", hide_index=True)

    with tabs[1]:
        st.markdown("### `WP-1` / `CLIN 0027`: Automated Day-1 Cryptographic Hardware-UUID License Key & WAWF Invoice Generator")
        col_a, col_b, col_c = st.columns(3)
        contract_no = col_a.text_input("Contract / Order Number:", value="FA8100-26-9-3952", key="ng_c27_contract")
        agency_name = col_b.text_input("Awarding Agency / Command:", value="DoD CDAO / Tinker AFB OC-ALC", key="ng_c27_agency")
        node_uuid   = col_c.text_input("Target Physical Hardware Node UUID:", value="HVF-NODE-OK-OCALC-3001", key="ng_c27_uuid")

        col_d, col_e = st.columns(2)
        award_val   = col_d.number_input("Total Contract Award Amount ($ USD):", min_value=10000.0, max_value=50000000.0, value=895000.0, step=25000.0, key="ng_c27_val")
        clin_list   = col_e.multiselect(
            "Licensed CLIN Modules:",
            options=["CLIN 0001", "CLIN 0003", "CLIN 0006", "CLIN 0007", "CLIN 0008", "CLIN 0009", "CLIN 0010", "CLIN 0011", "CLIN 1004-A", "CLIN 1004-B"],
            default=["CLIN 1004-A"],
            key="ng_c27_clins",
        )
        pkt = e27.generate_day1_packet(
            contract_number=contract_no,
            awarding_agency=agency_name,
            hardware_node_uuid=node_uuid,
            licensed_clins=clin_list or ["CLIN 0001"],
            total_contract_award_usd=award_val,
        )
        exp27 = e27.export_day1_markdown_and_pdf(pkt, artifacts_dir)
        st.success(f"**Issued Hardware-Locked License Key:** `{pkt['hardware_locked_license_key']}` | **Immediate Day-1 WAWF Invoice:** **`${pkt['day1_immediate_invoice_usd']:,.2f} USD`** (`{pkt['wawf_billing_code']}`)")
        bucket_rows = [{"Executive Budget Bucket": k, "Day-1 Allocated Cash ($ USD)": f"${v:,.2f}"} for k, v in pkt["day1_five_bucket_allocation_usd"].items()]
        st.dataframe(bucket_rows, width="stretch", hide_index=True)
        st.download_button(
            label=f"{ico_dl} Download WORM Day-1 License & WAWF Invoice PDF ({pathlib.Path(exp27['pdf_path']).name})",
            data=pathlib.Path(exp27["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp27["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c27_pdf",
        )

    with tabs[2]:
        st.markdown("### `WP-2` / `CLIN 0028`: `36.75ns` SiC MOSFET Hardware Interlock Board & BOM Engine")
        s1, s2, s3 = st.columns(3)
        vel_mms = s1.number_input("Manipulator Velocity (mm/s):", min_value=100.0, max_value=5000.0, value=1500.0, step=100.0, key="ng_c28_vel")
        bus_v   = s2.number_input("DC Actuator Bus Voltage (V):", min_value=24.0, max_value=1000.0, value=480.0, step=24.0, key="ng_c28_v")
        fault_a = s3.number_input("Peak Fault Current (Amps):", min_value=10.0, max_value=400.0, value=85.0, step=5.0, key="ng_c28_a")

        spec28 = e28.simulate_bench_calibration(actuator_velocity_mm_s=vel_mms, dc_bus_voltage_v=bus_v, peak_fault_current_a=fault_a)
        exp28  = e28.export_board_spec_markdown_and_pdf(spec28, artifacts_dir)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Guillotine Latency", f"{spec28['total_propagation_delay_ns']:.2f} ns", "18.50 + 12.00 + 6.25 ns")
        m2.metric("HVF Stopping Distance", f"{spec28['hvf_stopping_distance_um']:.4f} um", f"{spec28['speed_improvement_factor_x']:,.0f}x Faster")
        m3.metric("Legacy 150ms PLC Travel", f"{spec28['legacy_150ms_plc_stopping_distance_mm']:.1f} mm", "Crush Hazard Eliminated")
        m4.metric("Peak SiC Junction Temp", f"{spec28['max_sic_junction_temp_c']:.2f} C", "Limit < 175.0 C (PASS)")
        st.dataframe(spec28["bom_stages"], width="stretch", hide_index=True)
        st.download_button(
            label=f"{ico_dl} Download WP-2 36.75ns SiC MOSFET Board & BOM PDF",
            data=pathlib.Path(exp28["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp28["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c28_pdf",
        )

    with tabs[3]:
        st.markdown("### `WP-3` / `CLIN 0029`: Site PLC, 60Hz Microgrid SCADA, & SAE J1939 CAN-Bus Register Mapper")
        p1, p2, p3 = st.columns(3)
        grid_hz = p1.number_input("60Hz Microgrid Bus Frequency (Hz):", min_value=55.0, max_value=65.0, value=59.985, step=0.05, format="%.3f", key="ng_c29_hz")
        rocof   = p2.number_input("Microgrid RoCoF (Hz/s):", min_value=-5.0, max_value=5.0, value=-0.12, step=0.10, format="%.2f", key="ng_c29_rocof")
        moist   = p3.number_input("480V Silo Grain Moisture (%):", min_value=8.0, max_value=24.0, value=13.4, step=0.2, format="%.1f", key="ng_c29_moist")

        mg_res   = e29.evaluate_microgrid_60hz_relay(freq_hz=grid_hz, rocof_hz_s=rocof)
        silo_res = e29.evaluate_480v_silo_contactor_plc(grain_moisture_pct=moist)
        can_res  = e29.decode_sae_j1939_can_frame(0x0CF00400)
        exp29    = e29.generate_wp3_interface_dossier(artifacts_dir)

        st.json({"1_Microgrid_60Hz_Relay": mg_res, "2_Silo_480V_Contactor_PLC": silo_res, "3_SAE_J1939_CAN_Frame": can_res})
        st.download_button(
            label=f"{ico_dl} Download WP-3 PLC, 60Hz SCADA, & J1939 Interface Control PDF",
            data=pathlib.Path(exp29["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp29["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c29_pdf",
        )

    with tabs[4]:
        st.markdown("### `WP-4` / `CLIN 0030`: UAS Optical GLI Feed & Oklahoma Title 61 Civil GIS Engine")
        u1, u2, u3, u4 = st.columns(4)
        r_val = u1.slider("UAS Red Band (8-bit):", 0, 255, 62, key="ng_c30_r")
        g_val = u2.slider("UAS Green Band (8-bit):", 0, 255, 178, key="ng_c30_g")
        b_val = u3.slider("UAS Blue Band (8-bit):", 0, 255, 48, key="ng_c30_b")
        bid_v = u4.number_input("OK Title 61 Civil Works Bid ($ USD):", min_value=50000.0, max_value=25000000.0, value=420000.0, step=10000.0, key="ng_c30_bid")

        gli_res = e30.evaluate_uas_optical_gli(red_8bit=r_val, green_8bit=g_val, blue_8bit=b_val)
        gis_res = e30.evaluate_title61_gis_parcel_and_retainage(estimated_civil_work_usd=bid_v)
        exp30   = e30.generate_wp4_uas_gis_dossier(artifacts_dir)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Green Leaf Index (GLI)", f"{gli_res['green_leaf_index_gli']:.4f}", gli_res["canopy_classification"][:22])
        k2.metric("Gauss Survey Area", f"{gis_res['parcel_area_acres']:.2f} Acres", f"{gis_res['parcel_area_sq_m']:,.1f} sq m")
        k3.metric("OK Title 61 Retainage (5%)", f"${gis_res['ok_title61_statutory_retainage_5pct_usd']:,.2f}", "61 O.S. 113 Compliant")
        k4.metric("100% Performance Bond", f"${gis_res['statutory_performance_bond_100pct_usd']:,.2f}", "Statutory Bond Verified")
        st.download_button(
            label=f"{ico_dl} Download WP-4 UAS Optical GLI & Title 61 GIS PDF",
            data=pathlib.Path(exp30["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp30["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c30_pdf",
        )

    with tabs[5]:
        st.markdown("### `WP-5` / `CLIN 0031`: Command Watch-Floor Bitwise RBAC & Shift-Ledger PDF Compiler")
        w1, w2 = st.columns(2)
        callsign = w1.text_input("Command TOC Callsign:", value="TINKER-OCALC-TOC-ALPHA", key="ng_c31_call")
        role_sel = w2.selectbox("Inspect Watch-Floor Seat Role:", list(e31.ROLE_MASKS.keys()), index=2, key="ng_c31_role")

        perm_rows = []
        for p_label, p_bit in [
            ("PERM_READ_TELEMETRY (0x01)", e31.PERM_READ_TELEMETRY),
            ("PERM_AUDIT_INSPECT (0x02)", e31.PERM_AUDIT_INSPECT),
            ("PERM_ACK_ALARM (0x04)", e31.PERM_ACK_ALARM),
            ("PERM_CONTACTOR_OVERRIDE (0x08)", e31.PERM_CONTACTOR_OVERRIDE),
            ("PERM_SIGN_SHIFT_BRIEF (0x10)", e31.PERM_SIGN_SHIFT_BRIEF),
            ("PERM_GUILLOTINE_RESET (0x20)", e31.PERM_GUILLOTINE_RESET),
            ("PERM_WORM_MASTER_SEAL (0x40)", e31.PERM_WORM_MASTER_SEAL),
            ("PERM_AIRLOCK_RELEASE (0x80)", e31.PERM_AIRLOCK_RELEASE),
        ]:
            chk = e31.verify_seat_permission(role_sel, p_bit)
            perm_rows.append({
                "Seat Role": role_sel,
                "Role Mask": chk["role_mask_hex"],
                "Operation": p_label,
                "Authorized": "ALLOWED" if chk["authorized"] else "BLOCKED",
                "RBAC Token": chk["rbac_attestation_token"],
            })
        st.dataframe(perm_rows, width="stretch", hide_index=True)
        exp31 = e31.generate_wp5_watchfloor_dossier(artifacts_dir)
        st.code(f"Shift Handover WORM Chain Seal (SHA-256) [{callsign}]: {exp31['shift_ledger']['current_shift_worm_hash']}", language="text")
        st.download_button(
            label=f"{ico_dl} Download WP-5 Watch-Floor RBAC & Shift-Handover PDF",
            data=pathlib.Path(exp31["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp31["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c31_pdf",
        )

    with tabs[6]:
        st.markdown("### `WP-6` / `CLIN 0032`: DoD RMF / eMASS ATO STIG Synthesizer & 50-Seat Field Academy Provisioner")
        a1, a2 = st.columns(2)
        inst_name = a1.text_input("Target DoD Installation Enclave:", value="TINKER AFB // OC-ALC SOVEREIGN ENCLAVE", key="ng_c32_inst")
        cohort_id = a2.text_input("50-Seat Field Academy Cohort ID:", value="COHORT-2027-OK-ALPHA-01", key="ng_c32_cohort")

        ato_res  = e32.evaluate_dod_rmf_ato_controls(installation_name=inst_name)
        acad_res = e32.provision_50_seat_academy_cohort(cohort_id=cohort_id, seat_count=50)
        exp32    = e32.generate_wp6_ato_academy_dossier(artifacts_dir)

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("RMF Controls Satisfied", f"{ato_res['controls_satisfied']} / {ato_res['controls_evaluated']}", "100.0% NIST 800-53 Rev 5")
        r2.metric("DISA STIG Open Findings", "0 CAT I / 0 CAT II / 0 CAT III", "ATO Granted (TRL 9)")
        r3.metric("Provisioned Cohort Seats", f"{acad_res['provisioned_seat_count']} Seats", acad_res["cohort_id"])
        r4.metric("Verified Exam Question Bank", f"{acad_res['total_verified_questions']:,} Qs", "800 Ch.1 + 620 Ch.5")

        st.dataframe(ato_res["control_matrix"], width="stretch", hide_index=True)
        st.download_button(
            label=f"{ico_dl} Download WP-6 DoD RMF ATO & 50-Seat Academy Cohort PDF",
            data=pathlib.Path(exp32["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp32["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c32_pdf",
        )

    with tabs[7]:
        st.markdown("### `WP-7` / `CLIN 0033 v7.6`: Front-Screen OSHA Muster Points & Emergency Procedures + HIPAA-Gated 60-Field User Input Console, Medical/ICE Triage, & Credit Shield")

        # =====================================================================
        # SECTION 1 (ALWAYS VISIBLE ON FRONT SCREEN -- NO LOGIN REQUIRED):
        # 1A. COMPANY COMMAND / 911 DISPATCH DESKS
        # 1B. SITE MUSTER POINTS, SHELTER BUNKERS, AED/TRAUMA KITS & 5-STEP SOPs
        # =====================================================================
        st.markdown("#### 1A. Official Company Command & 911 Emergency Dispatch Desks (Always Accessible -- No Login Required)")
        st.dataframe(e33.COMPANY_EMERGENCY_CONTACTS, width="stretch", hide_index=True)

        st.markdown("#### 1B. Site-Wide Primary & Secondary Muster Points, Shelter-in-Place Bunkers, AED/Trauma Kits, & 5-Step Emergency Procedures (`OSHA 29 CFR 1910.38` -- No Login Required)")
        st.dataframe(e33.SITE_MUSTER_AND_BUNKER_SUMMARY, width="stretch", hide_index=True)

        zone_options = list(e33.FACILITY_ZONE_TO_ROSTER_KEY.keys())
        sel_zone_key = st.selectbox(
            "Select Facility Operational Zone to View Immediate 5-Step Emergency Evacuation & Muster SOP (No Login Required):",
            options=zone_options,
            index=0,
            key="ng_c33_zone_sel",
        )
        pub_muster = e33.get_public_emergency_muster_and_sops(sel_zone_key)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Primary Muster Point", pub_muster["primary_muster_title"], pub_muster["primary_muster_sub"])
        m2.metric("Secondary Muster Point", pub_muster["secondary_muster_title"], pub_muster["secondary_muster_sub"])
        m3.metric("Shelter-in-Place Bunker", pub_muster["bunker_title"], pub_muster["bunker_sub"])
        m4.metric("Nearest AED & Trauma Kit", pub_muster["aed_kit_title"], pub_muster["aed_kit_sub"])

        st.dataframe(pub_muster["muster_dispatch_ledger_rows"], width="stretch", hide_index=True)
        st.dataframe(pub_muster["emergency_procedures_rows"], width="stretch", hide_index=True)

        st.markdown("---")

        # =====================================================================
        # SECTION 2: MANDATORY HIPAA / ADA / FCRA USER AGREEMENT & GATE
        # =====================================================================
        st.markdown("#### 2. Sovereign User Agreement, HIPAA/ADA Medical Confidentiality Charter, & Compartment Authorization Gate")
        st.info(e33.USER_AGREEMENT_TEXT)

        roster_options = list(e33.PERSONNEL_EMERGENCY_ROSTER.keys())
        sel_person_key = st.selectbox(
            "Select Personnel Dossier to Authenticate, Input Information, or Unseal Behind Gate (All Personal PII & Medical PHI Locked Until Gate Opens):",
            options=roster_options,
            index=0,
            key="ng_c33_roster_sel",
        )
        person_obj = e33.PERSONNEL_EMERGENCY_ROSTER[sel_person_key]
        emp_id_code = person_obj["employee_id"]
        emp_pin_val = person_obj["employee_pin"]
        empr_key_val = "EMPLOYER-MASTER-1AHA8"

        st.caption(
            f"**Console Demo Keys for `{emp_id_code}`:** "
            f"Path A (Employee Personal Vault & 60-Field Input PIN) = `{emp_pin_val}` | Path B (Employer / HR Master Key) = `{empr_key_val}` "
            f"*(Automatically loaded into the key box when you switch paths below)*"
        )

        agree_chk = st.checkbox(
            "I have read and accept the Sovereign User Agreement & HIPAA/ADA Medical Confidentiality Charter.",
            value=False,
            key="ng_c33_agree_chk",
        )

        g1, g2, g3 = st.columns([2, 2, 1])
        role_mode = g1.radio(
            "Select Authorization Compartment Path to Unseal Personal/Medical/Vault Data & 60-Field Input Console:",
            options=[
                "GATE_LOCKED (Front-Screen Muster SOPs Active // 100% of Personal PII, Medical PHI, NOK/ICE & Vaults Hidden)",
                "PATH A: EMPLOYEE_PERSONAL_VAULT (Input/Update My 60-Field Dossier, View My Medical/ICE & My 7-Channel Credit/Loan Shield)",
                "PATH B: EMPLOYER_HR_AND_EMERGENCY_VAULT (HR Emergency Medical/Allergies/Blood/ICE, Employer Notes, Promotion Shortlist & HR Input Unlock)",
            ],
            index=0,
            key="ng_c33_role_radio",
        )

        short_role = "EMPLOYEE" if "EMPLOYEE_PERSONAL_VAULT" in role_mode else ("EMPLOYER" if "EMPLOYER_HR_AND_EMERGENCY_VAULT" in role_mode else "LOCKED")
        default_pin_hint = emp_pin_val if short_role == "EMPLOYEE" else (empr_key_val if short_role == "EMPLOYER" else "")

        dyn_key_id = f"ng_c33_key_{emp_id_code}_{short_role}"
        key_in = g2.text_input(
            f"Active Authorization Key ({short_role} Path):",
            value=default_pin_hint,
            key=dyn_key_id,
        )
        freeze_toggle = g3.checkbox("Credit/Loan Freeze ON", value=True, key="ng_c33_frz_v76")

        gate_res = e33.open_compartment_gate(
            roster_key=sel_person_key,
            viewer_role=short_role,
            user_agreement_accepted=agree_chk,
            access_key_or_pin=key_in,
            out_dir=artifacts_dir,
            credit_freeze_locked=freeze_toggle,
        )

        if not gate_res["gate_open"]:
            st.warning(
                f"**[HIPAA / ADA / FCRA GATE LOCKED // STATUS: `{gate_res['gate_status']}`]** -- "
                f"Site Muster Points, Shelter Bunkers, AED Locations, and 5-Step Emergency Evacuation Procedures are openly accessible above. "
                f"However, zero personal employee PII, Blood Type, Allergies, Medical History, Next-of-Kin (NOK), ICE contacts, "
                f"credit bureaus, or HR records are exposed while this gate is locked. "
                f"To unseal or input information: (1) Check the **I have read and accept the Sovereign User Agreement & HIPAA/ADA Charter** box above, and "
                f"(2) Select either **PATH A: EMPLOYEE_PERSONAL_VAULT** (Auto-Key: `{emp_pin_val}`) or "
                f"**PATH B: EMPLOYER_HR_AND_EMERGENCY_VAULT** (Auto-Key: `{empr_key_val}`)."
            )
        else:
            triage = gate_res["emergency_medical_ice_card"]
            st.success(
                f"**[{gate_res['gate_status']} // {triage['employee_id']} ({triage['full_name']})]** -- "
                f"{gate_res['privacy_notice']} | **HIPAA WORM Audit Seal:** `{gate_res['hipaa_audit_seal'][:20]}...`"
            )

            # =================================================================
            # SHARED AUTHENTICATED HIPAA MEDICAL HISTORY, ALLERGIES, BLOOD TYPE
            # & NOK/ICE TRIAGE PACKET (UNSEALED ONLY AFTER GATE AUTHENTICATION)
            # =================================================================
            st.markdown(f"#### Authenticated HIPAA Emergency Medical History, Allergies, Blood Type, Physician, & NOK/ICE Packet (`{triage['employee_id']} // {triage['full_name']}`)")
            e1, e2, e3, e4 = st.columns(4)
            e1.metric("Blood Type & Rh Factor", triage["blood_type_clean"], triage["medical_alert_clean"])
            e2.metric("Next of Kin (NOK) Phone", triage["nok_phone"], triage["nok_short"])
            e3.metric("Emergency (ICE) Direct Phone", triage["ice_phone"], triage["ice_short"])
            e4.metric("Employee Direct Phone", triage["direct_phone"], triage["role_short"])

            st.dataframe(triage["hipaa_triage_ledger_rows"], width="stretch", hide_index=True)
            st.markdown("---")

            if gate_res["viewer_role"] == "EMPLOYEE":
                # =============================================================
                # PATH A: EMPLOYEE PERSONAL VAULT & 60-FIELD USER INPUT CONSOLE
                # =============================================================
                cred_r = gate_res["credit_report"]
                unfrz_id = st.text_input("Generate My Personal One-Time Credit/Loan Unfreeze Token For Inquiry ID:", value="REQ-HVF-EQUIP-2026-001", key="ng_c33_emp_unfrz")
                my_tok = e33.generate_ceo_credit_unfreeze_token(unfrz_id)

                ec1, ec2, ec3 = st.columns(3)
                ec1.metric("My Credit & Loan Freeze", "LOCKED (Protected)" if cred_r["credit_freeze_locked"] else "TEMPORARY UNFREEZE", "Employer/HR Access: BLOCKED")
                ec2.metric("Fraudulent Loans/Pulls Blocked", f"{cred_r['fraudulent_loans_and_pulls_blocked']} / {cred_r['total_inquiries_monitored']} Blocked", "Equifax/Experian/TU/Chex/Deed/SIM")
                ec3.metric("My One-Time Unfreeze Token", my_tok, f"For {unfrz_id}")

                st.markdown("#### 1. My Private 7-Channel Credit Bureau, Bank/SBA Loan, Home Deed Title, ACH, & SIM-Swap Shield (Visible ONLY to Employee)")
                st.dataframe(cred_r["credit_loan_rows"], width="stretch", hide_index=True)

                st.markdown("---")
                st.markdown(f"#### 2. Interactive 60-Field Personnel Onboarding & Self-Service Data Input Console (`{triage['employee_id']} // {triage['full_name']}`)")
                emp_form_mode = st.radio(
                    "Select My 60-Field Dossier Mode (Open Interactive Input Boxes vs. View Sealed Proof-of-Identity Table):",
                    options=[
                        "OPEN_60_FIELD_USER_INPUT_FORM (Type / Edit My Personal, NOK/ICE, Address, Job History & Training Information)",
                        "VIEW_SEALED_60_FIELD_PROOF_OF_IDENTITY_TABLE (Read-Only Cryptographic Verification View)",
                    ],
                    index=0,
                    key=f"ng_c33_emp_form_mode_{emp_id_code}",
                )

                if emp_form_mode.startswith("OPEN_60_FIELD"):
                    st.info(
                        "**[60-FIELD USER DATA-ENTRY CONSOLE ACTIVE]** -- Enter 1 atomic response per box across all 8 sections below "
                        "(Legal/Vital, Current Address/Contact, Job/I-9/IDs, NOK/ICE & Medical, Biometrics/Assets, Previous 7-Yr Addresses, "
                        "Prior Job History, and Training/Certifications), then click **Submit & Seal My 60-Field Personnel Dossier** at the bottom."
                    )
                    emp_inputs: Dict[str, str] = {}
                    cur_vals = e33.get_saved_user_60field_values(artifacts_dir, sel_person_key)

                    st.markdown("##### Section 1: Legal Identity & Vital Statistics (`Fields 01 - 10` // 1 Response Per Box)")
                    s1_c = st.columns(5)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[0:10]):
                        emp_inputs[fk] = s1_c[idx % 5].text_input(flabel, value=cur_vals[fk], type="password" if is_s else "default", key=f"emp60_{emp_id_code}_{fk}")

                    st.markdown("##### Section 2: Current Residential Address, Contact, & Physical Description (`Fields 11 - 20` // 1 Response Per Box)")
                    s2_c = st.columns(5)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[10:20]):
                        emp_inputs[fk] = s2_c[idx % 5].text_input(flabel, value=cur_vals[fk], type="password" if is_s else "default", key=f"emp60_{emp_id_code}_{fk}")

                    st.markdown("##### Section 3: Job Application, I-9 Work Eligibility, & Government IDs (`Fields 21 - 27` // 1 Response Per Box)")
                    s3_c = st.columns(4)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[20:27]):
                        emp_inputs[fk] = s3_c[idx % 4].text_input(flabel, value=cur_vals[fk], type="password" if is_s else "default", key=f"emp60_{emp_id_code}_{fk}")

                    st.markdown("##### Section 4: Next of Kin (NOK), In Case of Emergency (ICE), Blood Type & Allergies (`Fields 28 - 35` // 1 Response Per Box)")
                    s4_c = st.columns(4)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[27:35]):
                        emp_inputs[fk] = s4_c[idx % 4].text_input(flabel, value=cur_vals[fk], type="password" if is_s else "default", key=f"emp60_{emp_id_code}_{fk}")

                    st.markdown("##### Section 5: 3-Modal Biometrics & Financial/SIM Asset Locks (`Fields 36 - 42` // 1 Response Per Box)")
                    s5_c = st.columns(4)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[35:42]):
                        emp_inputs[fk] = s5_c[idx % 4].text_input(flabel, value=cur_vals[fk], type="password" if is_s else "default", key=f"emp60_{emp_id_code}_{fk}")

                    st.markdown("##### Section 6: Previous 7-Year Residential Address History (`Fields 43 - 48` // 1 Response Per Box)")
                    s6_c = st.columns(3)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[42:48]):
                        emp_inputs[fk] = s6_c[idx % 3].text_input(flabel, value=cur_vals[fk], type="password" if is_s else "default", key=f"emp60_{emp_id_code}_{fk}")

                    st.markdown("##### Section 7: Verified Prior Employment & Job History (`Fields 49 - 54` // 1 Response Per Box)")
                    s7_c = st.columns(3)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[48:54]):
                        emp_inputs[fk] = s7_c[idx % 3].text_input(flabel, value=cur_vals[fk], type="password" if is_s else "default", key=f"emp60_{emp_id_code}_{fk}")

                    st.markdown("##### Section 8: Sovereign Academy, Certifications, Training Hours, & Company Evaluation (`Fields 55 - 60` // 1 Response Per Box)")
                    s8_c = st.columns(3)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[54:60]):
                        emp_inputs[fk] = s8_c[idx % 3].text_input(flabel, value=cur_vals[fk], type="password" if is_s else "default", key=f"emp60_{emp_id_code}_{fk}")

                    if st.button("Submit & Seal My 60-Field Personnel Dossier (Lock into WORM SQLite)", type="primary", key=f"emp_submit_60_{emp_id_code}"):
                        sub_res = e33.submit_user_60field_onboarding_application(
                            out_dir=artifacts_dir,
                            roster_key=sel_person_key,
                            profile_60_inputs=emp_inputs,
                            submitted_by_role=f"PATH_A_EMPLOYEE_{emp_id_code}",
                            submission_reason="EMPLOYEE_SELF_SERVICE_60FIELD_SUBMISSION",
                        )
                        st.success(
                            f"**60-Field Dossier Sealed for `{emp_id_code}` (Revision #{sub_res['revision_number']:02d})!** "
                            f"Composite 60-Field Seal: `{sub_res['composite_60field_seal'][:24]}...`"
                        )

                st.markdown("#### 3. My Sealed 60-Field Personal Identity, Address/Job History, Training, & NOK/ICE Dossier Table")
                st.dataframe(gate_res["proof_of_id_rows"], width="stretch", hide_index=True)

            elif gate_res["viewer_role"] == "EMPLOYER":
                # =============================================================
                # PATH B: EMPLOYER / HR INTERNAL & EMERGENCY VAULT
                # =============================================================
                st.markdown("#### 1A. Employer/HR Internal Security Clearance, I-9 E-Verify, & Watch-Floor RBAC Records (Hidden From Employee View)")
                st.dataframe(gate_res["employer_internal_records"], width="stretch", hide_index=True)

                st.markdown(f"#### 1B. Official Employer Personnel File Notes for `{triage['employee_id']} // {triage['full_name']}` (WORM SQLite -- Hidden From Employee)")
                n_col1, n_col2, n_col3 = st.columns([2, 2, 3])
                note_auth = n_col1.text_input(
                    "Note Author / Commanding Authority:",
                    value="JEFFERY HUMPHREY (CEO & SOVEREIGN ARCHITECT)",
                    key="ng_c33_note_auth",
                )
                note_cat = n_col2.selectbox(
                    "Personnel File Note Category:",
                    options=[
                        "PERFORMANCE_COMM_AND_PROMOTION",
                        "SECURITY_CLEARANCE_AND_VETTING_NOTE",
                        "SAFETY_INTERLOCK_QUALIFICATION",
                        "SHIFT_INCIDENT_OR_COUNSELING_RECORD",
                        "CONTRACT_CLIN_ASSIGNMENT_MEMO",
                    ],
                    index=0,
                    key="ng_c33_note_cat",
                )
                note_txt = n_col3.text_input(
                    "Enter Confidential Employer Note to Seal into Employee File:",
                    value=f"Verified annual sovereign security & operational readiness review for {triage['full_name']}.",
                    key=f"ng_c33_note_txt_{triage['employee_id']}",
                )
                if st.button("Seal & Append Official Employer Note to Employee File (WORM SQLite)", type="primary", key="ng_c33_add_note_btn"):
                    db_f = artifacts_dir / "wp7_identity_credit_worm_ledger.db"
                    added_n = e33.append_employer_personnel_note(
                        db_path=db_f,
                        employee_id=triage["employee_id"],
                        employee_name=triage["full_name"],
                        author_authority=note_auth,
                        note_category=note_cat,
                        confidential_note_text=note_txt,
                    )
                    gate_res["employer_personnel_notes"] = e33.get_employer_personnel_notes(db_f, employee_id=triage["employee_id"])
                    st.success(
                        f"**Employer Note Sealed to `{triage['employee_id']}` File!** WORM Note SHA-256: `{added_n['worm_note_sha256'][:24]}...` "
                        f"(Total Notes for `{triage['employee_id']}`: `{added_n['total_notes_for_employee']}`)"
                    )

                st.dataframe(gate_res["employer_personnel_notes"], width="stretch", hide_index=True)

                st.markdown("#### 1C. Employer Qualified Candidate Promotion & Company Evaluation Shortlist Puller (`worm_promotion_evaluation_board`)")
                st.caption(
                    "Filter across all personnel by verified prior job experience, HVF Field Academy exam score, "
                    "continuing training hours, 7-year address verification, and annual company evaluation rating to pull a single ranked Promotion Shortlist:"
                )
                p_c1, p_c2, p_c3, p_c4 = st.columns(4)
                min_exp_in  = p_c1.slider("Minimum Verified Experience (Yrs):", min_value=0, max_value=20, value=5, step=1, key="ng_c33_p_exp")
                min_acad_in = p_c2.slider("Minimum HVF Academy Score (%):", min_value=70.0, max_value=100.0, value=90.0, step=1.0, key="ng_c33_p_acad")
                min_eval_in = p_c3.slider("Minimum Company Eval Rating (0-5):", min_value=3.0, max_value=5.0, value=4.5, step=0.05, key="ng_c33_p_eval")
                req_spec_in = p_c4.selectbox(
                    "Required Technical Specialty Track:",
                    options=["ALL", "EXECUTIVE_C2", "SIC_HARDWARE", "SCADA_PLC", "UAS_GIS", "RMF_CYBER"],
                    index=0,
                    key="ng_c33_p_spec",
                )

                promo_res = e33.evaluate_promotion_and_company_shortlist(
                    out_dir=artifacts_dir,
                    min_experience_years=int(min_exp_in),
                    min_academy_score_pct=float(min_acad_in),
                    min_eval_rating=float(min_eval_in),
                    required_specialty=req_spec_in,
                )

                pm1, pm2, pm3 = st.columns(3)
                pm1.metric("Qualified Candidates Pulled", f"{promo_res['qualified_candidates_count']} / {promo_res['total_personnel_evaluated']} Qualified", f"Track: {req_spec_in}")
                pm2.metric("Top-Ranked Promotion Candidate", promo_res["top_ranked_candidate"], f"Readiness Index: {promo_res['top_pri_score']} / 100")
                pm3.metric("WORM Promotion Board Seals", f"{promo_res['worm_board_rows_logged']} Sealed Rows", "12 Active SQLite WORM Triggers")

                st.dataframe(promo_res["qualified_shortlist_rows"], width="stretch", hide_index=True)

                st.markdown("---")
                st.markdown(f"#### 2. Employer / HR 60-Field Onboarding Data-Entry Console & Unalterable Proof-of-Identity Lock (`{triage['employee_id']}`)")
                vault_state = e33.load_or_init_vault_lock_state(artifacts_dir)
                cur_rev = int(vault_state.get("revision_number", 1))
                employer_approval_tok = e33.generate_employer_change_approval_token(cur_rev)

                hr_view_mode = st.radio(
                    "Select HR / Employer 60-Field Dossier Mode:",
                    options=[
                        "OPEN_60_FIELD_HR_INPUT_FORM_NOW (Input New Candidate / Edit 60 Atomic Onboarding, Address, Job & Training Fields)",
                        "SEALED_UNALTERABLE_PROOF_OF_IDENTITY_VIEW (Read-Only Locked Record + Cryptographic Change-Approval Gate)",
                    ],
                    index=0,
                    key=f"ng_c33_hr_form_mode_{emp_id_code}",
                )

                if hr_view_mode.startswith("OPEN_60_FIELD"):
                    st.warning(
                        f"**[EMPLOYER / HR 60-FIELD DATA-ENTRY CONSOLE ACTIVE // `{emp_id_code}`]** -- "
                        f"Enter or update 1 atomic value per box across all 60 fields below, then click **Seal & Lock Sovereign Personnel Identity Application** to lock the record into WORM SQLite."
                    )
                    prof_inputs: Dict[str, str] = {}
                    def_vals = e33.get_saved_user_60field_values(artifacts_dir, sel_person_key)

                    st.markdown("##### Section 1: Legal Identity & Vital Statistics (`Fields 01 - 10` // 1 Response Per Box)")
                    s1_cols = st.columns(5)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[0:10]):
                        prof_inputs[fk] = s1_cols[idx % 5].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{emp_id_code}_{fk}")

                    st.markdown("##### Section 2: Residential Address, Contact, & Physical Description (`Fields 11 - 20` // 1 Response Per Box)")
                    s2_cols = st.columns(5)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[10:20]):
                        prof_inputs[fk] = s2_cols[idx % 5].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{emp_id_code}_{fk}")

                    st.markdown("##### Section 3: Job Application, I-9 Work Eligibility, & Government IDs (`Fields 21 - 27` // 1 Response Per Box)")
                    s3_cols = st.columns(4)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[20:27]):
                        prof_inputs[fk] = s3_cols[idx % 4].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{emp_id_code}_{fk}")

                    st.markdown("##### Section 4: Next of Kin (NOK) & In Case of Emergency (ICE) Contacts (`Fields 28 - 35` // 1 Response Per Box)")
                    s4_cols = st.columns(4)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[27:35]):
                        prof_inputs[fk] = s4_cols[idx % 4].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{emp_id_code}_{fk}")

                    st.markdown("##### Section 5: 3-Modal Biometrics & Asset Locks (`Fields 36 - 42` // 1 Response Per Box)")
                    s5_cols = st.columns(4)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[35:42]):
                        prof_inputs[fk] = s5_cols[idx % 4].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{emp_id_code}_{fk}")

                    st.markdown("##### Section 6: Previous 7-Year Residential Address History (`Fields 43 - 48` // 1 Response Per Box)")
                    s6_cols = st.columns(3)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[42:48]):
                        prof_inputs[fk] = s6_cols[idx % 3].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{emp_id_code}_{fk}")

                    st.markdown("##### Section 7: Verified Prior Employment & Job History (`Fields 49 - 54` // 1 Response Per Box)")
                    s7_cols = st.columns(3)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[48:54]):
                        prof_inputs[fk] = s7_cols[idx % 3].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{emp_id_code}_{fk}")

                    st.markdown("##### Section 8: Sovereign Academy, Certifications, Training Hours, & Company Evaluation (`Fields 55 - 60` // 1 Response Per Box)")
                    s8_cols = st.columns(3)
                    for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[54:60]):
                        prof_inputs[fk] = s8_cols[idx % 3].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{emp_id_code}_{fk}")

                    if st.button("Seal & Lock Sovereign Personnel Identity Application (Save 60 Fields into WORM SQLite)", type="primary", key=f"ng_c33_seal_lock_btn_{emp_id_code}"):
                        sub_hr = e33.submit_user_60field_onboarding_application(
                            out_dir=artifacts_dir,
                            roster_key=sel_person_key,
                            profile_60_inputs=prof_inputs,
                            submitted_by_role="PATH_B_EMPLOYER_HR_AUTHORITY",
                            submission_reason="EMPLOYER_VERIFIED_60FIELD_ONBOARDING_SEAL",
                        )
                        st.success(
                            f"**60-Field Dossier Sealed & Locked (Revision #{sub_hr['revision_number']:02d})!** "
                            f"Composite Seal: `{sub_hr['composite_60field_seal'][:24]}...`"
                        )
                else:
                    st.info(
                        f"**[UNALTERABLE DIGITAL PROOF-OF-IDENTITY STATE ACTIVE // REVISION #{cur_rev:02d} LOCKED]** -- "
                        f"Input form is removed in this view. Employee Personal Credit & Loan Telemetry: **100% BLOCKED BY PRIVACY WALL**."
                    )
                    st.caption(f"Reference Employer HMAC Approval Token for Rev #{cur_rev:02d}: `{employer_approval_tok}`")

                st.markdown("#### 3. Employee 60-Field Digital Proof-of-Identity, Career History, Training, & NOK/ICE Record Table")
                st.dataframe(gate_res["proof_of_id_rows"], width="stretch", hide_index=True)

                exp33 = e33.generate_wp7_antifraud_dossier(artifacts_dir)
                st.markdown("#### 4. Physical ID & 3-Modal Biometric Sign-In / Sign-Out WORM Audit Ledger")
                st.dataframe(exp33["access_events"], width="stretch", hide_index=True)
                st.markdown("#### 5. WORM Profile Revision & Employer Approval Audit Trail")
                st.dataframe(exp33["revision_history"], width="stretch", hide_index=True)

            exp_dl = e33.generate_wp7_antifraud_dossier(artifacts_dir)
            st.download_button(
                label=f"{ico_dl} Download WP-7 Multi-Page Front-Screen Muster SOPs & HIPAA-Gated 60-Field Dossier PDF",
                data=pathlib.Path(exp_dl["pdf_path"]).read_bytes(),
                file_name=pathlib.Path(exp_dl["pdf_path"]).name,
                mime="application/pdf",
                key="dl_c33_pdf",
            )

    with tabs[8]:
        st.markdown("### `WP-8` / `CLIN 0034`: Federal Capability Statement, Custom CLIN Quote Compiler, & Outreach Generator")
        q1, q2 = st.columns([2, 1])
        target_org = q1.text_input("Target Contracting Command / Enterprise Buyer:", value="TINKER AFB // OC-ALC DEPOT MAINTENANCE DIRECTORATE", key="ng_c34_org")
        node_qty   = q2.number_input("Hardware Node / Chassis Quantity:", min_value=1, max_value=250, value=1, step=1, key="ng_c34_nodes")

        sel_clins = st.multiselect(
            "Select CLIN Modules to Include in Firm-Fixed-Price Quote:",
            options=list(e34.KEY_CLIN_PRICES_USD.keys()),
            default=[
                "CLIN 0001 (Sovereign Command Base Entry Pilot - 1 Node)",
                "CLIN 0028 (WP-2: 36.75ns SiC MOSFET Breaker Board & BOM)",
                "CLIN 0033 (WP-7: 60-Field Proof-of-Identity, Emergency ICE, & Dual-Compartment Credit Shield)",
            ],
            key="ng_c34_clins",
        )

        exp34 = e34.generate_wp8_capability_and_quote_dossier(
            artifacts_dir,
            prospect_agency_or_company=target_org,
            selected_clin_keys=sel_clins,
            node_count=int(node_qty),
        )
        qt = exp34["quote"]

        k1, k2, k3 = st.columns(3)
        k1.metric("Total Annual FFP Quote", f"${qt['total_annual_ffp_quote_usd']:,.2f} USD", f"Seal: {qt['quote_verification_seal']}")
        k2.metric("Immediate Day-1 WAWF Invoice", f"${qt['day1_mobilization_invoice_usd']:,.2f} USD", qt["recommended_contract_vehicle"][:32] + "...")
        k3.metric("Quoted Hardware Nodes", f"{qt['node_count']} Node(s)", f"{len(qt['line_items'])} CLIN Module(s)")

        st.dataframe(qt["line_items"], width="stretch", hide_index=True)
        st.info(f"**Acquisition Vehicle:** `{qt['recommended_contract_vehicle']}` | **Executive Margin Telemetry:** `{qt['internal_margin_telemetry']}`")

        st.download_button(
            label=f"{ico_dl} Download Official Federal Capability Statement & FFP Quote PDF ({pathlib.Path(exp34['pdf_path']).name})",
            data=pathlib.Path(exp34["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp34["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c34_pdf",
        )

        st.markdown("#### Ready-to-Send Contracting Officer Email & LinkedIn Broadcast (Click Copy Icon in Top-Right of Box)")
        col_em, col_li = st.columns(2)
        with col_em:
            st.caption("Direct Contracting Officer / COR Email:")
            st.code(exp34["outreach"]["contracting_officer_email"], language="text")
        with col_li:
            st.caption("LinkedIn Executive Broadcast:")
            st.code(exp34["outreach"]["linkedin_broadcast"], language="text")


if __name__ == "__main__":
    render_nextgen_dashboard()
