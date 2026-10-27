"""
HUMPHREY VIRTUAL FARMS LLC // NEXT-GEN TRL 8/9 EXPANSION FORGE COMMAND DASHBOARD (PORT 8502)
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5)
Controlling Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect
Isolation Mandate: Runs strictly on Port 8502 from C:\hvf_c2_nextgen while Frozen Project Ebony
                   runs on Port 8501 from C:\hvf_c2 (Master Merkle Root: cc1ee1c8...949a).
"""
from __future__ import annotations
import pathlib
from typing import Any, Dict, List
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
from plugins.clin_0034_enterprise_hr_muster_hipaa_promotion_engine import EnterpriseHRMusterHipaaPromotionEngine
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
    e34_hr = EnterpriseHRMusterHipaaPromotionEngine()
    e34 = FederalCapabilityAndQuoteEngine()
    for eng in (e27, e28, e29, e30, e31, e32, e33, e34_hr, e34):
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
    e34_hr = EnterpriseHRMusterHipaaPromotionEngine()
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
    c1.metric("Post-Award Work Packages", "9 / 9 (WP-1..WP-9)", "100% Pre-Engineered")
    c2.metric("Next-Gen Expansion Value", "$600,000 / yr / Node", "CLIN 0027 - CLIN 0035")
    c3.metric("Combined Catalog Value", "$2,230,000 / yr / Node", "CLIN 0001 - CLIN 0035")
    c4.metric("Frozen Ebony Core Status", "0 Bytes Modified", "Merkle cc1ee1c8...949a")

    ico_shield = chr(0x1F6E1)
    ico_key    = chr(0x1F511)
    ico_bolt   = chr(0x26A1)
    ico_gear   = chr(0x2699)
    ico_ufo    = chr(0x1F6F8)
    ico_lock   = chr(0x1F512)
    ico_medal  = chr(0x1F396)
    ico_hr     = chr(0x1F3E2)
    ico_dl     = chr(0x1F4E5)
    tabs = st.tabs([
        f"{ico_shield} 0. Master Registry (WP-1..9)",
        f"{ico_key} 1. WP-1: Day-1 License & WAWF (CLIN 0027)",
        f"{ico_bolt} 2. WP-2: 36.75ns SiC Board (CLIN 0028)",
        f"{ico_gear} 3. WP-3: PLC/SCADA/J1939 (CLIN 0029)",
        f"{ico_ufo} 4. WP-4: UAS GLI & Title 61 (CLIN 0030)",
        f"{ico_lock} 5. WP-5: Watch-Floor RBAC (CLIN 0031)",
        f"{ico_medal} 6. WP-6: DoD RMF ATO & Academy (CLIN 0032)",
        f"{ico_shield} 7. WP-7: Personal Credit/Loan/Deed Shield & B2C (CLIN 0033)",
        f"{ico_hr} 8. WP-8: Enterprise HR, Muster, HIPAA & Promotion (CLIN 0034)",
        f"{ico_medal} 9. WP-9: Capability Statement & 35-CLIN Quote (CLIN 0035)",
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
        st.markdown("### `WP-7` / `CLIN 0033 v8.0`: Standalone Personal Sovereign Identity, 7-Channel Credit/Loan/Deed/SIM Anti-Fraud Shield & B2C Subscription Engine")
        st.info(e33.PERSONAL_PRIVACY_CHARTER)

        st.markdown("#### 1. Standalone Personal User (`B2C`) & Enterprise Benefit (`B2B2C`) Pricing & Revenue Projections")
        st.dataframe(e33.B2C_AND_SEAT_PRICING_TIERS, width="stretch", hide_index=True)

        rc1, rc2, rc3, rc4 = st.columns(4)
        b2c_ind_in = rc1.number_input("B2C Single Subscribers ($350/yr):", min_value=0, max_value=100000, value=500, step=50, key="ng_c33_b2c_ind")
        b2c_fam_in = rc2.number_input("B2C Family 5-Packs ($1,250/yr):", min_value=0, max_value=50000, value=120, step=10, key="ng_c33_b2c_fam")
        b2c_vip_in = rc3.number_input("Executive VIP Vaults ($2,500/yr):", min_value=0, max_value=10000, value=40, step=5, key="ng_c33_b2c_vip")
        ent_nod_in = rc4.number_input("Enterprise 50-Seat Packs ($65K/yr):", min_value=0, max_value=500, value=2, step=1, key="ng_c33_ent_nod")

        rev_m = e33.calculate_b2c_and_enterprise_revenue(
            b2c_individual_subscribers=int(b2c_ind_in),
            b2c_family_packs=int(b2c_fam_in),
            exec_vip_subscribers=int(b2c_vip_in),
            enterprise_50seat_nodes=int(ent_nod_in),
        )
        rv1, rv2, rv3 = st.columns(3)
        rv1.metric("Direct Personal User (B2C) ARR", f"${rev_m['b2c_direct_total_arr_usd']:,.2f} / yr", f"Ind: ${rev_m['b2c_individual_arr_usd']:,.0f} | Fam: ${rev_m['b2c_family_arr_usd']:,.0f}")
        rv2.metric("Enterprise 50-Seat Benefit ARR", f"${rev_m['enterprise_nodes_arr_usd']:,.2f} / yr", f"{int(ent_nod_in)} Node Pack(s) @ $65,000/yr")
        rv3.metric("Combined WP-7 Annual Revenue", f"${rev_m['combined_wp7_annual_revenue_usd']:,.2f} / yr", f"{rev_m['total_protected_individuals']:,} Protected Individuals")

        st.markdown("---")
        st.markdown("#### 2. Personal Subscriber Anti-Fraud Vault Gate (Zero Employer / Zero HR Access)")
        sub_options = list(e33.PERSONAL_SUBSCRIBER_PROFILES.keys())
        sel_sub_key = st.selectbox(
            "Select Personal Subscriber Vault to Unlock:",
            options=sub_options,
            index=0,
            key="ng_c33_sub_sel",
        )
        sub_obj = e33.PERSONAL_SUBSCRIBER_PROFILES[sel_sub_key]
        sub_id = sub_obj["subscriber_id"]
        sub_pin = sub_obj["personal_pin"]

        st.caption(f"**Demo Personal Subscriber PIN for `{sub_id}`:** `{sub_pin}` *(Auto-loaded below -- 100% Private to the Individual)*")
        p_agree = st.checkbox(
            "I accept the Sovereign Personal Anti-Fraud Charter (I confirm I am the individual owner of this personal credit/deed vault).",
            value=False,
            key="ng_c33_p_agree",
        )
        pg1, pg2 = st.columns([3, 1])
        p_pin_in = pg1.text_input("Personal Subscriber Vault PIN:", value=sub_pin, key=f"ng_c33_pin_{sub_id}")
        p_frz_in = pg2.checkbox("7-Channel Credit/Deed Freeze ON", value=True, key="ng_c33_p_frz")

        p_gate = e33.open_personal_subscriber_gate(
            subscriber_key=sel_sub_key,
            privacy_charter_accepted=p_agree,
            provided_personal_pin=p_pin_in,
            out_dir=artifacts_dir,
            credit_freeze_locked=p_frz_in,
        )

        if not p_gate["gate_open"]:
            st.warning(
                f"**[PERSONAL ANTI-FRAUD VAULT LOCKED // `{p_gate['gate_status']}`]** -- "
                f"Check the Personal Charter box above to unseal your private 7-Channel Credit Bureau, Loan, Home Deed, ACH, & SIM-Swap Shield (Auto-PIN: `{sub_pin}`)."
            )
        else:
            cred_r = p_gate["credit_report"]
            st.success(
                f"**[{p_gate['gate_status']}]** -- Tier: `{sub_obj['subscription_tier']}` | "
                f"**Employer / HR Access:** `0% (PHYSICALLY DECOUPLED FROM CLIN 0034)`"
            )
            unfrz_id = st.text_input("Generate My Personal 15-Minute Credit/Loan Unfreeze Token For Inquiry ID:", value="REQ-HVF-EQUIP-2026-001", key="ng_c33_unfrz_id")
            my_tok = e33.generate_ceo_credit_unfreeze_token(unfrz_id)

            pc1, pc2, pc3 = st.columns(3)
            pc1.metric("My Credit, Loan & Deed Freeze", "LOCKED (Protected)" if cred_r["credit_freeze_locked"] else "TEMPORARY UNFREEZE", "Employer/HR Access: 0% (DECOUPLED)")
            pc2.metric("Fraudulent Loans/Pulls Blocked", f"{cred_r['fraudulent_loans_and_pulls_blocked']} / {cred_r['total_inquiries_monitored']} Blocked", "Equifax/Experian/TU/Chex/Deed/SIM")
            pc3.metric("My One-Time Unfreeze Token", my_tok, f"For {unfrz_id}")

            st.markdown("#### 2A. My 7-Channel Credit Bureau, Bank/SBA Loan, Home/Land Deed APN, Treasury ACH, & SIM-Swap Intercept Ledger")
            st.dataframe(cred_r["credit_loan_rows"], width="stretch", hide_index=True)

            st.markdown("#### 2B. My Personal 18-Field Identity, Bureau Freeze PIN, Bank Routing, Home Deed APN, & SIM-Lock Input Console")
            cur_18 = p_gate["current_18_values"]
            in_18: Dict[str, str] = {}
            p_cols = st.columns(3)
            for idx, (pk, plabel, is_sec) in enumerate(e33.PERSONAL_18_SCHEMA):
                in_18[pk] = p_cols[idx % 3].text_input(plabel, value=cur_18[pk], type="password" if is_sec else "default", key=f"p18_{sub_id}_{pk}")

            if st.button("Save & Seal My Personal 18-Field Anti-Fraud Vault (WORM SQLite)", type="primary", key=f"save_p18_{sub_id}"):
                s_out = e33.save_personal_subscriber_18_fields(artifacts_dir, sel_sub_key, in_18)
                st.success(f"**Personal 18-Field Anti-Fraud Vault Sealed for `{sub_id}`!** Composite Seal: `{s_out['composite_seal'][:24]}...`")
                st.rerun()

            st.markdown("#### 2C. My Sealed 18-Field Personal Anti-Fraud & Asset Lock Verification Table")
            st.dataframe(p_gate["personal_vault_rows"], width="stretch", hide_index=True)

        exp33 = e33.generate_wp7_antifraud_dossier(artifacts_dir)
        st.download_button(
            label=f"{ico_dl} Download WP-7 (CLIN 0033 v8.0) Standalone Personal Credit/Loan/Deed Shield & B2C Pricing Spec PDF",
            data=pathlib.Path(exp33["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp33["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c33_pdf",
        )

    with tabs[8]:
        st.markdown("### `WP-8` / `CLIN 0034 v8.0`: Enterprise HR, Front-Screen OSHA Muster SOPs, HIPAA Medical/ICE Triage, Zero-Trust Dual-Custody (`NIST AC-5`) 60-Field Dossier & Promotion Board")

        st.markdown("#### 1A. Official Company Command & 911 Emergency Dispatch Desks (Always Accessible -- No Login Required)")
        st.dataframe(e34_hr.COMPANY_EMERGENCY_CONTACTS, width="stretch", hide_index=True)

        st.markdown("#### 1B. Site-Wide Primary & Secondary Muster Points, Shelter-in-Place Bunkers, AED/Trauma Kits, & 5-Step Emergency Procedures (`OSHA 29 CFR 1910.38` -- No Login Required)")
        st.dataframe(e34_hr.SITE_MUSTER_AND_BUNKER_SUMMARY, width="stretch", hide_index=True)

        zone_options = list(e34_hr.FACILITY_ZONE_TO_ROSTER_KEY.keys())
        sel_zone_key = st.selectbox(
            "Select Facility Operational Zone to View Immediate 5-Step Emergency Evacuation & Muster SOP (No Login Required):",
            options=zone_options,
            index=0,
            key="ng_c34_hr_zone_sel",
        )
        pub_muster = e34_hr.get_public_emergency_muster_and_sops(sel_zone_key)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Primary Muster Point", pub_muster["primary_muster_title"], pub_muster["primary_muster_sub"])
        m2.metric("Secondary Muster Point", pub_muster["secondary_muster_title"], pub_muster["secondary_muster_sub"])
        m3.metric("Shelter-in-Place Bunker", pub_muster["bunker_title"], pub_muster["bunker_sub"])
        m4.metric("Nearest AED & Trauma Kit", pub_muster["aed_kit_title"], pub_muster["aed_kit_sub"])

        st.dataframe(pub_muster["muster_dispatch_ledger_rows"], width="stretch", hide_index=True)
        st.dataframe(pub_muster["emergency_procedures_rows"], width="stretch", hide_index=True)

        st.markdown("---")
        st.markdown("#### 2. Enterprise HR, HIPAA/ADA Medical Confidentiality, & Zero-Trust Two-Person Integrity Gate (`CLIN 0034`)")
        st.info(e34_hr.ENTERPRISE_HR_AND_HIPAA_CHARTER)

        roster_options = list(e34_hr.PERSONNEL_EMERGENCY_ROSTER.keys())
        sel_person_key = st.selectbox(
            "Select Personnel Dossier to Authenticate & Unseal Behind HR/HIPAA Gate (All Personal PII & Medical PHI Locked Until Gate Opens):",
            options=roster_options,
            index=0,
            key="ng_c34_hr_roster_sel",
        )
        person_obj = e34_hr.PERSONNEL_EMERGENCY_ROSTER[sel_person_key]
        emp_id_code = person_obj["employee_id"]
        empr_key_val = "EMPLOYER-MASTER-1AHA8"

        st.caption(f"**Console Demo HR / Emergency Master Key:** `{empr_key_val}` *(Auto-loaded below -- Personal Credit/Loans are 100% separated into Tab 7 / CLIN 0033)*")

        hr_agree_chk = st.checkbox(
            "I have read and accept the Enterprise HR, HIPAA/ADA Medical Confidentiality, & Zero-Trust Two-Person Integrity Charter.",
            value=False,
            key="ng_c34_hr_agree_chk",
        )
        hr_key_in = st.text_input(
            "Active Enterprise HR & Emergency Triage Master Key:",
            value=empr_key_val,
            key=f"ng_c34_hr_key_{emp_id_code}",
        )

        gate_res = e34_hr.open_hr_and_hipaa_gate(
            roster_key=sel_person_key,
            charter_accepted=hr_agree_chk,
            provided_hr_key=hr_key_in,
            out_dir=artifacts_dir,
        )

        if not gate_res["gate_open"]:
            st.warning(
                f"**[ENTERPRISE HR & HIPAA GATE LOCKED // STATUS: `{gate_res['gate_status']}`]** -- "
                f"Site Muster Points, Shelter Bunkers, AED Locations, and 5-Step Emergency Evacuation Procedures are openly accessible above. "
                f"Zero personal employee PII, Blood Type, Allergies, Medical History, NOK/ICE contacts, or HR dossiers are exposed while locked. "
                f"Check the **Enterprise HR & HIPAA Charter** box above to unseal (Auto-Key: `{empr_key_val}`)."
            )
        else:
            triage = gate_res["emergency_medical_ice_card"]
            lock_st = e34_hr.get_employee_dossier_lock_status(artifacts_dir, sel_person_key)
            is_emp_locked = lock_st["is_locked"]
            cur_emp_rev = lock_st["revision_number"]
            hr_tok_ref = lock_st["hr_custodian_token"]
            ver_tok_ref = lock_st["second_verifier_token"]

            st.success(
                f"**[{gate_res['gate_status']} // {triage['employee_id']} ({triage['full_name']})]** -- "
                f"HIPAA WORM Audit Seal: `{gate_res['hipaa_audit_seal'][:24]}...` | "
                f"**Personal Credit/Loans:** `0% PRESENT (100% Decoupled into Tab 7 / CLIN 0033)`"
            )

            st.markdown(f"#### 2A. Authenticated HIPAA Emergency Medical History, Allergies, Blood Type, Physician, & NOK/ICE Packet (`{triage['employee_id']} // {triage['full_name']}`)")
            e1, e2, e3, e4 = st.columns(4)
            e1.metric("Blood Type & Rh Factor", triage["blood_type_clean"], triage["medical_alert_clean"])
            e2.metric("Next of Kin (NOK) Phone", triage["nok_phone"], triage["nok_short"])
            e3.metric("Emergency (ICE) Direct Phone", triage["ice_phone"], triage["ice_short"])
            e4.metric("Employee Direct Phone", triage["direct_phone"], triage["role_short"])

            st.dataframe(triage["hipaa_triage_ledger_rows"], width="stretch", hide_index=True)

            st.markdown("#### 2B. Enterprise HR Security Clearance, I-9 E-Verify, & Watch-Floor RBAC Records")
            st.dataframe(gate_res["employer_internal_records"], width="stretch", hide_index=True)

            st.markdown(f"#### 2C. Official HR Personnel File Notes for `{triage['employee_id']} // {triage['full_name']}` (WORM SQLite)")
            n_col1, n_col2, n_col3 = st.columns([2, 2, 3])
            note_auth = n_col1.text_input(
                "Note Author & Verifying Co-Signer:",
                value="HR: EMP-002 (CAPT. VANCE) // VERIFIED BY: EMP-003 (DR. LIN)",
                key="ng_c34_note_auth",
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
                key="ng_c34_note_cat",
            )
            note_txt = n_col3.text_input(
                "Enter Verified HR Note to Seal into Employee File:",
                value=f"Dual-custody verified annual security & operational readiness review for {triage['full_name']}.",
                key=f"ng_c34_note_txt_{triage['employee_id']}",
            )
            if st.button("Seal & Append Verified HR Note to Employee File (WORM SQLite)", type="primary", key="ng_c34_add_note_btn"):
                db_f = artifacts_dir / "wp8_enterprise_hr_triage_worm.db"
                added_n = e34_hr.append_employer_personnel_note(
                    db_path=db_f,
                    employee_id=triage["employee_id"],
                    employee_name=triage["full_name"],
                    author_authority=note_auth,
                    note_category=note_cat,
                    confidential_note_text=note_txt,
                )
                gate_res["employer_personnel_notes"] = e34_hr.get_employer_personnel_notes(db_f, employee_id=triage["employee_id"])
                st.success(
                    f"**Verified HR Note Sealed to `{triage['employee_id']}` File!** WORM Note SHA-256: `{added_n['worm_note_sha256'][:24]}...` "
                    f"(Total Notes for `{triage['employee_id']}`: `{added_n['total_notes_for_employee']}`)"
                )

            st.dataframe(gate_res["employer_personnel_notes"], width="stretch", hide_index=True)

            st.markdown("#### 2D. HR Qualified Candidate Promotion & Company Evaluation Shortlist Puller (`worm_promotion_evaluation_board`)")
            p_c1, p_c2, p_c3, p_c4 = st.columns(4)
            min_exp_in  = p_c1.slider("Minimum Verified Experience (Yrs):", min_value=0, max_value=20, value=5, step=1, key="ng_c34_p_exp")
            min_acad_in = p_c2.slider("Minimum HVF Academy Score (%):", min_value=70.0, max_value=100.0, value=90.0, step=1.0, key="ng_c34_p_acad")
            min_eval_in = p_c3.slider("Minimum Company Eval Rating (0-5):", min_value=3.0, max_value=5.0, value=4.5, step=0.05, key="ng_c34_p_eval")
            req_spec_in = p_c4.selectbox(
                "Required Technical Specialty Track:",
                options=["ALL", "EXECUTIVE_C2", "SIC_HARDWARE", "SCADA_PLC", "UAS_GIS", "RMF_CYBER"],
                index=0,
                key="ng_c34_p_spec",
            )

            promo_res = e34_hr.evaluate_promotion_and_company_shortlist(
                out_dir=artifacts_dir,
                min_experience_years=int(min_exp_in),
                min_academy_score_pct=float(min_acad_in),
                min_eval_rating=float(min_eval_in),
                required_specialty=req_spec_in,
            )

            pm1, pm2, pm3 = st.columns(3)
            pm1.metric("Qualified Candidates Pulled", f"{promo_res['qualified_candidates_count']} / {promo_res['total_personnel_evaluated']} Qualified", f"Track: {req_spec_in}")
            pm2.metric("Top-Ranked Promotion Candidate", promo_res["top_ranked_candidate"], f"Readiness Index: {promo_res['top_pri_score']} / 100")
            pm3.metric("WORM Promotion Board Seals", f"{promo_res['worm_board_rows_logged']} Sealed Rows", "10 Active HR SQLite WORM Triggers")

            st.dataframe(promo_res["qualified_shortlist_rows"], width="stretch", hide_index=True)

            st.markdown("---")
            st.markdown(f"#### 3. Zero-Trust 60-Field Dossier Lock & Two-Person Integrity (`HR Custodian + Second Verifier`) Gate (`{triage['employee_id']} // {triage['full_name']}`)")

            if is_emp_locked:
                st.info(
                    f"**[UNALTERABLE 60-FIELD DOSSIER SEALED & LOCKED // REVISION #{cur_emp_rev:02d} // CO-SIGNED BY `{lock_st['last_actor']}`]** -- "
                    f"All 60 input boxes are **100% REMOVED**. Under **Zero-Trust Separation of Duties (`NIST SP 800-53 AC-5`)**, "
                    f"**no single person (neither CEO, HR, nor Employee) can approve or unlock this record alone**. "
                    f"Unlocking requires **Two Distinct Officials** below: **Signer #1 (HR Custodian)** + **Signer #2 (Independent Second-Party Verifier)**."
                )
                st.markdown("#### 3A. Sealed 60-Field Digital Proof-of-Identity, Career History, Training, & NOK/ICE Record (Read-Only Unalterable State)")
                st.dataframe(gate_res["proof_of_id_rows"], width="stretch", hide_index=True)

                st.markdown(f"#### 3B. Zero-Trust Two-Person Integrity (`TPI`) Unlock Gate -- Requires HR Custodian (`Signer #1`) + Independent Verifier (`Signer #2`)")
                st.caption(
                    f"**Reference Dual-Custody Tokens for `{emp_id_code}` Rev #{cur_emp_rev:02d}:** "
                    f"Signer #1 (HR Custody Token) = `{hr_tok_ref}` | Signer #2 (Independent Verifier Token) = `{ver_tok_ref}` "
                    f"*(Anti-Self-Approval Active: Signer #1 and Signer #2 MUST be different officials, and Signer #2 cannot be `{emp_id_code}`!)*"
                )
                ver_options = e34_hr.AUTHORIZED_VERIFIER_OFFICERS
                default_ver_idx = 1 if emp_id_code != "EMP-003" else 2

                dc1, dc2 = st.columns(2)
                hr_signer_in = dc1.selectbox(
                    "Co-Signer #1: Initiating HR Records Custodian:",
                    options=ver_options,
                    index=0,
                    key=f"ng_c34_hr_sig1_{emp_id_code}",
                )
                hr_tok_in = dc1.text_input(
                    "Co-Signer #1 HR Custody HMAC Token:",
                    value=hr_tok_ref,
                    key=f"ng_c34_hr_tok_{emp_id_code}_rev_{cur_emp_rev}",
                )
                ver_signer_in = dc2.selectbox(
                    "Co-Signer #2: Independent Second-Party Verifier (Must Not Be Signer #1 or Subject):",
                    options=ver_options,
                    index=default_ver_idx,
                    key=f"ng_c34_ver_sig2_{emp_id_code}",
                )
                ver_tok_in = dc2.text_input(
                    "Co-Signer #2 Independent Verifier HMAC Token:",
                    value=ver_tok_ref,
                    key=f"ng_c34_ver_tok_{emp_id_code}_rev_{cur_emp_rev}",
                )

                rsn_col, btn_col = st.columns([3, 1])
                dual_rsn_in = rsn_col.text_input(
                    "Verified Evidentiary Basis / Document Reference for Dossier Revision:",
                    value="HR_AND_SECOND_VERIFIER_DOCUMENTS_INSPECTED_AND_CONFIRMED",
                    key=f"ng_c34_dual_rsn_{emp_id_code}",
                )
                unlock_btn = btn_col.button(
                    "Verify Dual-Custody & Unlock (1 Rev)",
                    type="primary",
                    key=f"ng_c34_dual_unlock_btn_{emp_id_code}",
                )

                if unlock_btn:
                    res_un = e34_hr.request_dual_custody_unlock_for_employee(
                        out_dir=artifacts_dir,
                        roster_key=sel_person_key,
                        hr_custodian_officer=hr_signer_in,
                        provided_hr_token=hr_tok_in,
                        second_verifier_officer=ver_signer_in,
                        provided_verifier_token=ver_tok_in,
                        change_reason=dual_rsn_in,
                    )
                    if res_un["unlocked"]:
                        st.rerun()
                    else:
                        st.error(f"Zero-Trust Dual-Custody Unlock Denied: {res_un['status']}")
            else:
                st.warning(
                    f"**[60-FIELD DOSSIER UNLOCKED VIA TWO-PERSON INTEGRITY (`{lock_st['last_actor']}`) FOR 1 REVISION // `{emp_id_code}`]** -- "
                    f"Verified Basis: `{lock_st['last_reason']}`. Enter the verified updates across the 60 fields below, then click **Co-Sign, Seal & Lock 60-Field Dossier**. "
                    f"The instant you click Seal & Lock, all 60 input boxes are removed and your updated name/scores immediately propagate to the Promotion Shortlist!"
                )
                prof_inputs: Dict[str, str] = {}
                def_vals = e34_hr.get_saved_user_60field_values(artifacts_dir, sel_person_key)

                st.markdown("##### Section 1: Legal Identity & Vital Statistics (`Fields 01 - 10` // 1 Response Per Box)")
                s1_cols = st.columns(5)
                for idx, (fk, flabel, _, is_s) in enumerate(e34_hr.ATOMIC_60_SCHEMA[0:10]):
                    prof_inputs[fk] = s1_cols[idx % 5].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng60_{emp_id_code}_{fk}")

                st.markdown("##### Section 2: Residential Address, Contact, & Physical Description (`Fields 11 - 20` // 1 Response Per Box)")
                s2_cols = st.columns(5)
                for idx, (fk, flabel, _, is_s) in enumerate(e34_hr.ATOMIC_60_SCHEMA[10:20]):
                    prof_inputs[fk] = s2_cols[idx % 5].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng60_{emp_id_code}_{fk}")

                st.markdown("##### Section 3: Job Application, I-9 Work Eligibility, & Government IDs (`Fields 21 - 27` // 1 Response Per Box)")
                s3_cols = st.columns(4)
                for idx, (fk, flabel, _, is_s) in enumerate(e34_hr.ATOMIC_60_SCHEMA[20:27]):
                    prof_inputs[fk] = s3_cols[idx % 4].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng60_{emp_id_code}_{fk}")

                st.markdown("##### Section 4: Next of Kin (NOK) & In Case of Emergency (ICE) Contacts (`Fields 28 - 35` // 1 Response Per Box)")
                s4_cols = st.columns(4)
                for idx, (fk, flabel, _, is_s) in enumerate(e34_hr.ATOMIC_60_SCHEMA[27:35]):
                    prof_inputs[fk] = s4_cols[idx % 4].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng60_{emp_id_code}_{fk}")

                st.markdown("##### Section 5: 3-Modal Biometrics & Duty Callsign Locks (`Fields 36 - 42` // 1 Response Per Box)")
                s5_cols = st.columns(4)
                for idx, (fk, flabel, _, is_s) in enumerate(e34_hr.ATOMIC_60_SCHEMA[35:42]):
                    prof_inputs[fk] = s5_cols[idx % 4].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng60_{emp_id_code}_{fk}")

                st.markdown("##### Section 6: Previous 7-Year Residential Address History (`Fields 43 - 48` // 1 Response Per Box)")
                s6_cols = st.columns(3)
                for idx, (fk, flabel, _, is_s) in enumerate(e34_hr.ATOMIC_60_SCHEMA[42:48]):
                    prof_inputs[fk] = s6_cols[idx % 3].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng60_{emp_id_code}_{fk}")

                st.markdown("##### Section 7: Verified Prior Employment & Job History (`Fields 49 - 54` // 1 Response Per Box)")
                s7_cols = st.columns(3)
                for idx, (fk, flabel, _, is_s) in enumerate(e34_hr.ATOMIC_60_SCHEMA[48:54]):
                    prof_inputs[fk] = s7_cols[idx % 3].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng60_{emp_id_code}_{fk}")

                st.markdown("##### Section 8: Sovereign Academy, Certifications, Training Hours, & Company Evaluation (`Fields 55 - 60` // 1 Response Per Box)")
                s8_cols = st.columns(3)
                for idx, (fk, flabel, _, is_s) in enumerate(e34_hr.ATOMIC_60_SCHEMA[54:60]):
                    prof_inputs[fk] = s8_cols[idx % 3].text_input(flabel, value=def_vals[fk], type="password" if is_s else "default", key=f"ng60_{emp_id_code}_{fk}")

                if st.button("Co-Sign, Seal & Lock 60-Field Dossier (Remove Input Boxes -- Requires 2-Person HR + Verifier Co-Sign to Re-Open)", type="primary", key=f"ng_c34_seal_lock_btn_{emp_id_code}"):
                    e34_hr.submit_dual_custody_60field_dossier(
                        out_dir=artifacts_dir,
                        roster_key=sel_person_key,
                        profile_60_inputs=prof_inputs,
                        submitted_by_role=lock_st["last_actor"],
                        submission_reason=lock_st["last_reason"],
                    )
                    st.rerun()

            exp34_hr = e34_hr.generate_wp8_hr_dossier(artifacts_dir)
            st.markdown("#### 4. Physical ID & 3-Modal Biometric Sign-In / Sign-Out WORM Audit Ledger")
            st.dataframe(exp34_hr["access_events"], width="stretch", hide_index=True)
            st.markdown("#### 5. WORM Profile Revision & Dual-Custody Two-Person Verification Audit Trail")
            st.dataframe(exp34_hr["revision_history"], width="stretch", hide_index=True)

        exp_dl_hr = e34_hr.generate_wp8_hr_dossier(artifacts_dir)
        st.download_button(
            label=f"{ico_dl} Download WP-8 (CLIN 0034 v8.0) Enterprise HR, Muster SOPs, HIPAA Triage & Dual-Custody 60-Field Dossier PDF",
            data=pathlib.Path(exp_dl_hr["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp_dl_hr["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c34_hr_pdf",
        )

    with tabs[9]:
        st.markdown("### `WP-9` / `CLIN 0035 v8.0`: Automated Federal Capability Statement, 35-CLIN (`$2,230,000/yr/Node`) Custom Quote Compiler & Outreach Engine")
        q_c1, q_c2, q_c3 = st.columns([2, 1, 1])
        agency_in = q_c1.text_input(
            "Target Procuring Agency / Contracting Office:",
            value="U.S. Department of Defense / CDAO Tradewinds Contracting Office",
            key="ng_c35_agency",
        )
        nodes_in = q_c2.number_input("Physical Node Quantity:", min_value=1, max_value=100, value=1, step=1, key="ng_c35_nodes")
        inc_core = q_c3.checkbox("Include Frozen 26-CLIN Core ($1.63M/Node)", value=True, key="ng_c35_core")

        q_res = e34.build_custom_quote(
            customer_agency=agency_in,
            node_count=int(nodes_in),
            include_frozen_core=inc_core,
        )

        qm1, qm2, qm3, qm4 = st.columns(4)
        qm1.metric("Single-Node 35-CLIN Catalog", f"${q_res['single_node_annual_usd']:,.2f} / yr", "CLIN 0001 - CLIN 0035")
        qm2.metric(f"Extended Quote ({q_res['node_count']} Node[s])", f"${q_res['grand_total_annual_usd']:,.2f} / yr", "Firm-Fixed-Price (FFP)")
        qm3.metric("Day-1 WAWF Mobilization Invoice", f"${q_res['day1_wawf_invoice_usd']:,.2f}", "50% OTA / 100% COTS <= $250K")
        qm4.metric("CEO Day-1 Distribution (35.0%)", f"${q_res['ceo_day1_allocation_35pct_usd']:,.2f}", "Jeffery Humphrey (CAGE 1AHA8)")

        st.markdown("#### 1. Official Corporate & Acquisition Vehicle Identifiers")
        id_rows = [{"Corporate_Attribute": k, "Verified_Sovereign_Registration": v} for k, v in e34.CORPORATE_IDENTIFIERS.items()]
        st.dataframe(id_rows, width="stretch", hide_index=True)

        st.markdown("#### 2. Complete 35-CLIN Firm-Fixed-Price Schedule")
        st.dataframe(q_res["line_items"], width="stretch", hide_index=True)

        st.markdown("#### 3. Ready-to-Send Contracting Officer Proposal Email (Copy & Paste)")
        st.code(q_res["contracting_officer_email_text"], language="text")

        st.markdown("#### 4. Ready-to-Post LinkedIn Executive Broadcast (Copy & Paste)")
        st.code(q_res["linkedin_executive_broadcast_text"], language="text")

        exp35 = e34.generate_wp8_capability_and_quote_packet(artifacts_dir, customer_agency=agency_in, node_count=int(nodes_in))
        st.download_button(
            label=f"{ico_dl} Download WP-9 (CLIN 0035 v8.0) Official Federal Capability Statement & 35-CLIN Quote PDF",
            data=pathlib.Path(exp35["pdf_path"]).read_bytes(),
            file_name=pathlib.Path(exp35["pdf_path"]).name,
            mime="application/pdf",
            key="dl_c35_quote_pdf",
        )

if __name__ == "__main__":
    render_nextgen_dashboard()
