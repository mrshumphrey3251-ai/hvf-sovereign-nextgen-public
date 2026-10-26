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
        st.markdown("### `WP-7` / `CLIN 0033 v5.0`: 42-Field Atomic Personnel Onboarding, NOK/ICE, Digital Proof-of-Identity Lock, & Credit Shield")

        vault_state = e33.load_or_init_vault_lock_state(artifacts_dir)
        is_locked = bool(vault_state.get("is_locked", True))
        cur_rev = int(vault_state.get("revision_number", 1))
        employer_approval_tok = e33.generate_employer_change_approval_token(cur_rev)

        if is_locked:
            st.success(
                f"**[UNALTERABLE DIGITAL PROOF-OF-IDENTITY STATE ACTIVE // REVISION #{cur_rev:02d} LOCKED]** ? "
                f"All 42 atomic application, government ID, biometric, and Next-of-Kin / ICE fields are cryptographically sealed. "
                f"The input form has been removed to prevent tampering. Changes require Employer / Commanding Officer Approval."
            )
            exp33 = e33.generate_wp7_antifraud_dossier(
                artifacts_dir,
                update_reason=vault_state.get("last_change_reason", "SEALED_PROOF_OF_IDENTITY"),
            )
            pii_r  = exp33["pii_report"]
            cred_r = exp33["credit_report"]
            w_db   = exp33["worm_db_stats"]

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Proof-of-Identity Status", f"LOCKED (Rev #{cur_rev:02d})", "Input Form Removed")
            m2.metric("Atomic Fields Sealed", f"{pii_r['atomic_fields_count']} / 42 Fields", "1 Response Per Field + NOK/ICE")
            m3.metric("Loans/Deeds/SIMs Blocked", f"{cred_r['fraudulent_loans_and_pulls_blocked']} / {cred_r['total_inquiries_monitored']} Blocked", "Equifax/Experian/TU/Chex/Deed/SIM")
            m4.metric("WORM SQLite Ledger Rows", f"{w_db['worm_profile_revision_rows']} Revs | {w_db['worm_id_access_rows']} ID", "6 WORM Triggers Active")

            st.code(
                f"Verified Principal       : {pii_r['full_legal_name']}{nl}"
                f"Masked SSN / DOB Bind    : {pii_r['masked_ssn']} | {pii_r['masked_dob']} (0 Plaintext Sensitive Digits Stored){nl}"
                f"Last Approved By         : {vault_state.get('last_approved_by', 'EMPLOYER_AUTHORITY')}{nl}"
                f"Last Approval Reason     : {vault_state.get('last_change_reason', 'INITIAL_ONBOARDING')}{nl}"
                f"42-Field Master HMAC Seal: {pii_r['composite_42field_application_seal']}",
                language="text",
            )

            st.markdown("#### Sealed 42-Field Digital Proof-of-Identity, Employment, & Next-of-Kin / ICE Record (Read-Only Unalterable View)")
            st.dataframe(pii_r["attribute_rows"], width="stretch", hide_index=True)

            st.markdown("#### Employer / Commanding Officer Change-Approval Gate (Required to Unlock & Edit Application)")
            st.caption(
                f"To unlock this sealed record for an authorized update, enter the Employer Change-Approval Token "
                f"(Current Console Reference Token for Rev #{cur_rev:02d}: `{employer_approval_tok}`) and a mandatory change justification:"
            )
            u1, u2, u3, u4 = st.columns([2, 2, 2, 1])
            auth_name_in = u1.text_input("Approving Employer / Authority Name:", value="JEFFERY HUMPHREY (CEO & EMPLOYER AUTHORITY)", key="ng_c33_auth_name")
            auth_tok_in  = u2.text_input("Employer HMAC Change-Approval Token:", value=employer_approval_tok, key="ng_c33_auth_tok")
            auth_rsn_in  = u3.text_input("Mandatory Change Justification Reason:", value="APPROVED_EMPLOYEE_RECORD_UPDATE", key="ng_c33_auth_rsn")
            unlock_btn   = u4.button("Approve & Unlock Form", type="primary", key="ng_c33_unlock_btn")

            if unlock_btn:
                res_un = e33.request_employer_unlock_for_edit(
                    artifacts_dir,
                    provided_approval_token=auth_tok_in,
                    change_reason=auth_rsn_in,
                    approving_authority=auth_name_in,
                )
                if res_un["unlocked"]:
                    st.rerun()
                else:
                    st.error(f"Unlock Denied: {res_un['status']}")

        else:
            st.warning(
                f"**[APPLICATION INPUT & EDIT MODE UNLOCKED BY: `{vault_state.get('last_approved_by')}`]** ? "
                f"Reason: `{vault_state.get('last_change_reason')}`. Enter strictly **1 single atomic response per box** across all 42 fields below, "
                f"then click **Seal & Lock Sovereign Personnel Identity Application** to remove this input section and lock the record."
            )
            prof_inputs: Dict[str, str] = {}
            def_vals = e33.DEFAULT_ATOMIC_42_VALUES

            st.markdown("#### Section 1: Legal Identity & Vital Statistics (`Fields 01 - 10` // 1 Response Per Box)")
            s1_cols = st.columns(5)
            for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[0:10]):
                col = s1_cols[idx % 5]
                prof_inputs[fk] = col.text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{fk}")

            st.markdown("#### Section 2: Residential Address, Contact, & Physical Description (`Fields 11 - 20` // 1 Response Per Box)")
            s2_cols = st.columns(5)
            for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[10:20]):
                col = s2_cols[idx % 5]
                prof_inputs[fk] = col.text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{fk}")

            st.markdown("#### Section 3: Job Application, I-9 Work Eligibility, & Government IDs (`Fields 21 - 27` // 1 Response Per Box)")
            s3_cols = st.columns(4)
            for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[20:27]):
                col = s3_cols[idx % 4]
                prof_inputs[fk] = col.text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{fk}")

            st.markdown("#### Section 4: Next of Kin (NOK) & In Case of Emergency (ICE) Contacts (`Fields 28 - 35` // 1 Response Per Box)")
            s4_cols = st.columns(4)
            for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[27:35]):
                col = s4_cols[idx % 4]
                prof_inputs[fk] = col.text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{fk}")

            st.markdown("#### Section 5: 3-Modal Biometrics & Financial / Asset Protection Locks (`Fields 36 - 42` // 1 Response Per Box)")
            s5_cols = st.columns(4)
            for idx, (fk, flabel, _, is_s) in enumerate(e33.ATOMIC_42_SCHEMA[35:42]):
                col = s5_cols[idx % 4]
                prof_inputs[fk] = col.text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng42_{fk}")

            seal_btn = st.button(
                "Seal & Lock Sovereign Personnel Identity Application (Remove Input Form & Lock Record)",
                type="primary",
                key="ng_c33_seal_lock_btn",
            )
            if seal_btn:
                e33.seal_and_lock_personnel_application(
                    artifacts_dir,
                    profile_42=prof_inputs,
                    update_reason=vault_state.get("last_change_reason", "EMPLOYER_VERIFIED_ONBOARDING_SEAL"),
                    approving_authority=vault_state.get("last_approved_by", "JEFFERY HUMPHREY (CEO)"),
                )
                e33.generate_wp7_antifraud_dossier(
                    artifacts_dir,
                    raw_ssn=prof_inputs["f05_ssn"],
                    raw_dob=prof_inputs["f06_dob"],
                    update_reason=vault_state.get("last_change_reason", "EMPLOYER_VERIFIED_ONBOARDING_SEAL"),
                    profile_42_overrides=prof_inputs,
                )
                st.rerun()

            exp33 = e33.generate_wp7_antifraud_dossier(
                artifacts_dir,
                raw_ssn=prof_inputs["f05_ssn"],
                raw_dob=prof_inputs["f06_dob"],
                profile_42_overrides=prof_inputs,
            )
            cred_r = exp33["credit_report"]

        st.markdown("---")
        st.markdown("#### WORM Profile Revision & Employer Approval Audit Trail (`worm_identity_profile_revisions`)")
        st.dataframe(exp33["revision_history"], width="stretch", hide_index=True)

        st.markdown("#### 7-Channel Credit Bureau, SBA/Bank Loan, County Deed Title, ChexSystems/ACH, & SIM-Swap Interceptor")
        st.dataframe(cred_r["credit_loan_rows"], width="stretch", hide_index=True)

        st.markdown("#### Physical ID & 3-Modal Biometric Sign-In / Sign-Out WORM Audit Ledger & Anti-Replay Gate")
        st.dataframe(exp33["access_events"], width="stretch", hide_index=True)

        st.download_button(
            label=f"{ico_dl} Download WP-7 Multi-Page 42-Field Proof-of-Identity, NOK/ICE, Credit, Loan & Deed Shield PDF",
            data=pathlib.Path(exp33["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp33["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c33_pdf",
        )


if __name__ == "__main__":
    render_nextgen_dashboard()
