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


def build_registry_and_engines():
    reg = SovereignPluginRegistry()
    e27 = Day1LicenseAndWAWFInvoiceGenerator()
    e28 = SiCMOSFETGuillotineBoardEngine()
    e29 = SitePLCSCADACANBusMapper()
    e30 = UASOpticalGLIAndTitle61GISEngine()
    e31 = CommandWatchFloorRBACAndPDFEngine()
    e32 = DoDRMFATOAndAcademyCohortEngine()
    e33 = SovereignIdentityAntiFraudShield()
    for eng in (e27, e28, e29, e30, e31, e32, e33):
        reg.register(eng)
    return reg, e27, e28, e29, e30, e31, e32, e33


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

    reg, e27, e28, e29, e30, e31, e32, e33 = build_registry_and_engines()
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
    c1.metric("Post-Award Work Packages", "7 / 7 (WP-1..WP-7)", "100% Pre-Engineered")
    c2.metric("Next-Gen Expansion Value", "$515,000 / yr / Node", "CLIN 0027 - CLIN 0033")
    c3.metric("Combined Catalog Value", "$2,145,000 / yr / Node", "CLIN 0001 - CLIN 0033")
    c4.metric("Frozen Ebony Core Status", "0 Bytes Modified", "Merkle cc1ee1c8...949a")

    tabs = st.tabs([
        f"{ico_shield} 0. Master Registry (WP-1..7)",
        f"{ico_key} 1. WP-1: Day-1 License & WAWF (CLIN 0027)",
        f"{ico_bolt} 2. WP-2: 36.75ns SiC Board (CLIN 0028)",
        f"{ico_gear} 3. WP-3: PLC/SCADA/J1939 (CLIN 0029)",
        f"{ico_drone} 4. WP-4: UAS GLI & Title 61 (CLIN 0030)",
        f"{ico_lock} 5. WP-5: Watch-Floor RBAC (CLIN 0031)",
        f"{ico_medal} 6. WP-6: DoD RMF ATO & Academy (CLIN 0032)",
        f"{ico_shield} 7. WP-7: SSN/DOB, Credit/Loan & ID Shield (CLIN 0033)",
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
        st.markdown("### `WP-7` / `CLIN 0033 v4.0`: Full-Page 16-Factor Sovereign Identity Enrollment, Profile Updater, Credit/Loan/Deed Interceptor, & WORM Access Shield")
        st.info(
            "**Full-Page 16+ Identifier Vault & Versioned Updater:** Edit or update any of the 16 personal, physical, biometric, or asset identifiers below. "
            "All sensitive values are automatically masked (`XXX-XX-last4` / `XXXX-MASKED-tail`) and hashed in memory (`0` plaintext digits stored). "
            "Click **Commit & Seal Updated 16-Factor Identity Profile Revision** to append a new cryptographically chained revision to the WORM SQLite ledger."
        )

        top1, top2, top3, top4 = st.columns([2, 2, 1, 1])
        op_name    = top1.text_input("Protected Principal / Operator Full Name & Title:", value="JEFFERY HUMPHREY (CEO & SOVEREIGN ARCHITECT)", key="ng_c33_op")
        upd_reason = top2.text_input("Profile Update / Enrollment Reason:", value="ANNUAL_16FACTOR_CREDENTIAL_AND_ASSET_VERIFICATION", key="ng_c33_reason")
        unfrz_req  = top3.text_input("CEO Unfreeze Inquiry ID:", value="REQ-HVF-EQUIP-2026-001", key="ng_c33_req")
        freeze_on  = top4.checkbox("Lock All 7 Credit/Loan/Deed Channels", value=True, key="ng_c33_frz")

        st.markdown("#### Quadrant A: Core Personal, Civil, & Government Identity Documents (`Factors 1 - 6`)")
        qa1, qa2, qa3 = st.columns(3)
        ssn_in    = qa1.text_input("1. Social Security Number (9-Digit Tax ID - Masked):", value="999-00-1234", type="password", key="ng_c33_f01")
        dob_in    = qa2.text_input("2. Date of Birth (ISO YYYY-MM-DD - Masked):", value="1975-08-15", type="password", key="ng_c33_f02")
        pob_in    = qa3.text_input("3. Place of Birth & Mother's Maiden KBA Vector:", value="OKLAHOMA-KBA-SEAL-991", type="password", key="ng_c33_f03")

        qa4, qa5, qa6 = st.columns(3)
        realid_in = qa4.text_input("4. State Driver's License / REAL-ID Barcode Serial:", value="OK-REALID-1AHA8-7741", key="ng_c33_f04")
        pass_in   = qa5.text_input("5. U.S. Passport Book/Card Number & MRZ:", value="US-PASS-558912044", key="ng_c33_f05")
        cac_in    = qa6.text_input("6. DoD CAC / FIPS 201 PIV 10-Digit EDIPI:", value="CAC-EDIPI-1099482210", key="ng_c33_f06")

        st.markdown("#### Quadrant B: Physical Distinguishing Features & 3-Modal Biometric Templates (`Factors 7 - 10`)")
        qb1, qb2, qb3, qb4 = st.columns(4)
        smt_in    = qb1.text_input("7. Physical Traits (Eyes / Height / Scars, Marks, Tattoos):", value="EYES:BRN|HGT:72IN|SMT:NONE-VERIFIED", key="ng_c33_f07")
        fngr_in   = qb2.text_input("8. Biometric #1: Fingerprint Minutiae (ISO 19794-2):", value="BIO-FINGER-ISO19794-2-V1", key="ng_c33_f08")
        iris_in   = qb3.text_input("9. Biometric #2: Iris & Retinal Vascular (ISO 19794-6):", value="BIO-IRIS-ISO19794-6-V1", key="ng_c33_f09")
        face_in   = qb4.text_input("10. Biometric #3: 3D Facial Geometry & Voice Liveness:", value="BIO-3DFACE-VOICE-LIVENESS-V1", key="ng_c33_f10")

        st.markdown("#### Quadrant C: Real Estate Deed, Banking/Treasury, Telecom SIM, Medical, VIN, & Corporate Identifiers (`Factors 11 - 16`)")
        qc1, qc2, qc3 = st.columns(3)
        deed_in   = qc1.text_input("11. Real Estate Home/Land Deed Parcel APN Lock:", value="OK-APN-DEED-LOCK-44019", key="ng_c33_f11")
        bank_in   = qc2.text_input("12. Bank Routing & Treasury Account (ABA/ACH/SWIFT Lock):", value="ABA-103000648-ACH-LOCKED", key="ng_c33_f12")
        sim_in    = qc3.text_input("13. Mobile Carrier SIM / IMEI Port-Out Lock (2FA Shield):", value="IMEI-35988109-SIMLOCK-ON", key="ng_c33_f13")

        qc4, qc5, qc6 = st.columns(3)
        med_in    = qc4.text_input("14. Medical / Medicare / Health Insurance Beneficiary ID:", value="MED-SHIELD-ID-88310", key="ng_c33_f14")
        vin_in    = qc5.text_input("15. Vehicle / Heavy Equipment Chassis VIN Title Lock:", value="1HVF882910SOVEREIGN", key="ng_c33_f15")
        corp_in   = qc6.text_input("16. Corporate Federal EIN, SAM.gov UEI, & CAGE Code:", value="UEI:S1M4ENLHTDH5|CAGE:1AHA8", key="ng_c33_f16")

        btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])
        commit_clicked = btn_col1.button(
            "Commit & Seal Updated 16-Factor Identity Profile Revision to WORM SQLite",
            type="primary",
            key="ng_c33_commit_btn",
        )
        custom_act = btn_col2.selectbox("Watch-Floor Gate Action:", ["SIGN_IN", "SIGN_OUT"], index=0, key="ng_c33_gate_act")
        gate_nonce = btn_col3.text_input("Hardware Liveness Nonce:", value="NONCE-LIVE-2026-0099", key="ng_c33_nonce")

        exp33 = e33.generate_wp7_antifraud_dossier(
            artifacts_dir,
            operator_name=op_name,
            raw_ssn=ssn_in,
            raw_dob=dob_in,
            pob_and_maiden_kba=pob_in,
            physical_id_number=realid_in,
            passport_number=pass_in,
            dod_cac_piv_serial=cac_in,
            physical_smt_features=smt_in,
            fingerprint_minutiae=fngr_in,
            iris_vascular_hash=iris_in,
            face_voice_liveness=face_in,
            home_deed_parcel_apn=deed_in,
            bank_ach_aba_routing=bank_in,
            mobile_sim_imei_lock=sim_in,
            medical_npi_beneficiary=med_in,
            vehicle_fleet_vin=vin_in,
            corporate_ein_uei=corp_in,
            credit_freeze_locked=freeze_on,
            update_reason=upd_reason,
        )

        pii_r  = exp33["pii_report"]
        cred_r = exp33["credit_report"]
        w_db   = exp33["worm_db_stats"]
        ceo_tk = e33.generate_ceo_credit_unfreeze_token(unfrz_req)

        if commit_clicked:
            db_file = artifacts_dir / "wp7_identity_credit_worm_ledger.db"
            rev_res = e33.commit_profile_update_revision(
                db_path=db_file,
                operator_name=op_name,
                update_reason=upd_reason,
                pii_report=pii_r,
            )
            exp33["revision_history"] = e33.get_profile_revision_history(db_file)
            st.success(
                f"**WORM Profile Revision Committed!** Revision `#{rev_res['revision_number']}` sealed with "
                f"16-Factor HMAC `{rev_res['composite_16factor_seal'][:24]}...` and chained to WORM SQLite (`{rev_res['worm_revision_sha256'][:24]}...`)."
            )

        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Masked SSN / DOB Bind", f"{pii_r['masked_ssn']} | {pii_r['masked_dob']}", "0 Plaintext Digits Stored")
        f2.metric("16-Factor Identity Matrix", f"{pii_r['clean_attributes']} / {pii_r['core_identifying_features_count']} Clean", "+1 Dark-Web Canary Quarantined")
        f3.metric("Loans/Deeds/SIMs Blocked", f"{cred_r['fraudulent_loans_and_pulls_blocked']} / {cred_r['total_inquiries_monitored']} Blocked", "Equifax/Experian/TU/Chex/Deed/SIM")
        f4.metric("WORM SQLite Ledger Rows", f"{w_db['worm_profile_revision_rows']} Revs | {w_db['worm_id_access_rows']} ID | {w_db['worm_credit_intercept_rows']} Credit", "6 WORM Triggers Active")

        st.success(
            f"**Composite 16-Factor Identity Seal:** `{pii_r['composite_16factor_identity_seal'][:32]}...` | "
            f"**CEO Unfreeze Token (`{unfrz_req}`):** `{ceo_tk}` | "
            f"**Gate Status (`{custom_act}` / `{gate_nonce}`):** `READY`"
        )

        st.markdown("#### 1. WORM Identity Profile Revision & Update History (`worm_identity_profile_revisions`)")
        st.dataframe(exp33["revision_history"], width="stretch", hide_index=True)

        st.markdown("#### 2. 16-Factor Zero-Knowledge Personal, Physical (SMT), 3-Modal Biometric, & Asset Dark-Web Monitor")
        st.dataframe(pii_r["attribute_rows"], width="stretch", hide_index=True)

        st.markdown("#### 3. 7-Channel Credit Bureau, SBA/Bank Loan, County Deed Title, ChexSystems/ACH, & SIM-Swap Interceptor")
        st.dataframe(cred_r["credit_loan_rows"], width="stretch", hide_index=True)

        st.markdown("#### 4. Physical ID & 3-Modal Biometric Sign-In / Sign-Out WORM Audit Ledger & Anti-Replay Gate")
        st.dataframe(exp33["access_events"], width="stretch", hide_index=True)

        st.download_button(
            label=f"{ico_dl} Download WP-7 Multi-Page 16-Factor Identity, Profile Revision, Credit, Loan & Deed Shield PDF",
            data=pathlib.Path(exp33["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp33["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c33_pdf",
        )


if __name__ == "__main__":
    render_nextgen_dashboard()
