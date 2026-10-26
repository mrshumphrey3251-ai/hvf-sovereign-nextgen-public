"""
HUMPHREY VIRTUAL FARMS LLC // CLIN 0034 (WP-8): FEDERAL CAPABILITY STATEMENT, 34-CLIN QUOTE COMPILER, & OUTREACH ENGINE
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5)
Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect
Work Package: WP-8 (Automated SAM.gov / CDAO Tradewinds Capability Statement, Firm-Fixed-Price Quote & Outreach Generator)
Host Compatibility: Frozen Project Ebony TRL 7 Baseline (cc1ee1c8d29b2ae5e856fc0fcb672a52e7e49d50369499febe14e18e9150949a)
"""
from __future__ import annotations
import hashlib
import pathlib
from typing import Any, Dict, List

from nextgen_core.sovereign_plugin_contract import (
    FROZEN_EBONY_MERKLE_ROOT,
    SovereignExpansionModule,
)
from plugins.clin_0027_day1_license_wawf_generator import build_minimal_iso_pdf

ENCLAVE_MODE = "PUBLIC"
QUOTE_SIGNING_SEED = "PUBLIC_QUOTE_SEED_REDACTED_DFARS_252_227_7018"


class FederalCapabilityAndQuoteEngine(SovereignExpansionModule):
    """
    WP-8 / CLIN 0034 Plug-In:
      1. Maintains the complete Per-Node Commercial & Federal Price Schedule across Project Ebony Core
         ($1,630,000/yr CLIN 0001-0026) and the Next-Gen Expansion Forge ($545,000/yr CLIN 0027-0034).
      2. Synthesizes customized Firm-Fixed-Price (FFP) Government & Commercial Quotes, Day-1 WAWF
         mobilization schedules, and Multi-Page Federal Capability Statements (%PDF-1.4).
      3. Generates copy-and-paste LinkedIn Executive Broadcasts and Contracting Officer Outreach Emails.
    """

    KEY_CLIN_PRICES_USD = {
        "CLIN 0001 (Sovereign Command Base Entry Pilot - 1 Node)": 24500,
        "CLIN 0003 (60Hz Microgrid SCADA & Islanding Relay)": 85000,
        "CLIN 0006 (36.75ns SiC MOSFET Kinetic Guillotine Software Core)": 95000,
        "CLIN 0007 (UAS Multispectral GLI & Autonomous Flight C2)": 70000,
        "CLIN 0008 (SAE J1939 Heavy-Equipment CAN-Bus Telemetry)": 65000,
        "CLIN 0009 (480V 3-Phase Silo & Industrial Contactor Matrix)": 60000,
        "CLIN 0010 (Oklahoma Title 61 Civil Works & 5% Retainage Engine)": 55000,
        "CLIN 0011 (Sovereign Field Academy - 50-Seat Cohort & 1,420 Qs)": 125000,
        "CLIN 0022 (ISO 32000-1 WORM PDF Audit Ledger Compiler)": 35000,
        "CLIN 0027 (WP-1: Day-1 Hardware-UUID License & WAWF Generator)": 35000,
        "CLIN 0028 (WP-2: 36.75ns SiC MOSFET Breaker Board & BOM)": 65000,
        "CLIN 0029 (WP-3: Site PLC, 60Hz SCADA, & J1939 Register Mapper)": 75000,
        "CLIN 0030 (WP-4: UAS Optical GLI & Title 61 GIS Boundary Engine)": 75000,
        "CLIN 0031 (WP-5: Command Watch-Floor Bitwise RBAC & Shift PDF)": 45000,
        "CLIN 0032 (WP-6: DoD RMF / eMASS ATO & 50-Seat Cohort Provisioner)": 125000,
        "CLIN 0033 (WP-7: 60-Field Proof-of-Identity, Emergency ICE, & Dual-Compartment Credit Shield)": 95000,
        "CLIN 0034 (WP-8: Federal Capability Statement & FFP Quote Compiler)": 30000,
        "CLIN 1004-A (Turnkey 26-Module Single-Node TOC Enclave Bundle)": 895000,
        "CLIN 1004-B (25-Node Military Base / Enterprise Fleet License)": 2450000,
    }

    CORE_26_UNBUNDLED_ANNUAL_USD = 1630000
    NEXTGEN_8_UNBUNDLED_ANNUAL_USD = 545000
    TOTAL_34_UNBUNDLED_ANNUAL_USD = 2175000

    def __init__(self) -> None:
        super().__init__(
            plugin_id="HVF-NG-CLIN-0034",
            clin_number="CLIN 0034",
            title="Automated Federal Capability Statement, 34-CLIN Quote Compiler, & Outreach Engine",
            version="1.0.0",
            target_trl="TRL 8/9",
            per_node_annual_gov_usd=30000,
            per_node_monthly_comm_usd=2800,
        )

    def build_custom_quote(
        self,
        prospect_agency_or_company: str = "TINKER AFB // OC-ALC DEPOT MAINTENANCE DIRECTORATE",
        solicitation_or_docket: str = "CDAO Tradewinds Docket 10-26-3952 / FAR Part 13",
        selected_clin_keys: List[str] | None = None,
        node_count: int = 1,
    ) -> Dict[str, Any]:
        assert self.CORE_26_UNBUNDLED_ANNUAL_USD + self.NEXTGEN_8_UNBUNDLED_ANNUAL_USD == self.TOTAL_34_UNBUNDLED_ANNUAL_USD
        if not selected_clin_keys:
            selected_clin_keys = [
                "CLIN 0001 (Sovereign Command Base Entry Pilot - 1 Node)",
                "CLIN 0028 (WP-2: 36.75ns SiC MOSFET Breaker Board & BOM)",
                "CLIN 0033 (WP-7: 60-Field Proof-of-Identity, Emergency ICE, & Dual-Compartment Credit Shield)",
            ]

        line_items: List[Dict[str, Any]] = []
        annual_subtotal = 0
        for k in selected_clin_keys:
            unit_p = self.KEY_CLIN_PRICES_USD.get(k, 24500)
            ext_p = unit_p * max(1, node_count)
            annual_subtotal += ext_p
            line_items.append({
                "CLIN_Item": k,
                "Per_Node_Annual_USD": f"${unit_p:,.2f}",
                "Node_Qty": max(1, node_count),
                "Extended_Annual_USD": f"${ext_p:,.2f}",
            })

        if annual_subtotal <= 250000:
            vehicle = "FAR Part 13 Simplified Acquisition / FAR Part 12 Commercial COTS (100% Day-1 WAWF)"
            day1_cash = float(annual_subtotal)
        else:
            vehicle = "10 U.S.C. 4022 Defense Prototype OTA / FAR Part 12 Contract (50% Day-1 Milestone #01)"
            day1_cash = round(annual_subtotal * 0.50, 2)

        if ENCLAVE_MODE == "PRIVATE":
            ceo_comp_usd = round(day1_cash * 0.35, 2)
            warchest_usd = round(day1_cash * 0.15, 2)
            margin_note = f"Day-1 CEO Draw (35%): ${ceo_comp_usd:,.2f} | Day-1 Corporate War Chest (15%): ${warchest_usd:,.2f}"
        else:
            margin_note = "[REDACTED_INTERNAL_MARGIN_SPLIT_DFARS_252_227_7018]"

        quote_seal = hashlib.sha256(
            f"{prospect_agency_or_company}|{solicitation_or_docket}|{annual_subtotal}|{QUOTE_SIGNING_SEED}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8")
        ).hexdigest().upper()

        return {
            "prospect_agency_or_company": prospect_agency_or_company,
            "solicitation_or_docket": solicitation_or_docket,
            "node_count": max(1, node_count),
            "line_items": line_items,
            "total_annual_ffp_quote_usd": float(annual_subtotal),
            "recommended_contract_vehicle": vehicle,
            "day1_mobilization_invoice_usd": day1_cash,
            "internal_margin_telemetry": margin_note,
            "quote_verification_seal": f"HVF-QUOTE-{quote_seal[:16]}",
        }

    def generate_outreach_templates(
        self,
        prospect_agency_or_company: str = "TINKER AFB // OC-ALC DEPOT MAINTENANCE DIRECTORATE",
    ) -> Dict[str, str]:
        linkedin_post = (
            "SOVEREIGN C2, 36.75NS ROBOTICS SAFETY, & DUAL-COMPARTMENT IDENTITY/CREDIT SHIELD: TRL 7 CORE + TRL 8/9 FORGE\n\n"
            "As Founder, CEO, and Principal Sovereign Architect of Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5), "
            "I am proud to announce that alongside our frozen TRL 7 Project Ebony Operating Console (DoD CDAO Tradewinds Dockets 10-26-3952 & 9-26-3703), "
            "we have completed and sealed our Post-Award TRL 8/9 Expansion Forge (WP-1 through WP-8 / CLIN 0027 - CLIN 0034).\n\n"
            "1. 36.75ns SiC MOSFET Kinetic Guillotine (CLIN 0006 & CLIN 0028): Stops a 1,500 mm/s robotic arm in 0.0551 microns (vs. 225.0 mm on a 150ms PLC).\n"
            "2. Zero-Second Emergency ICE Triage & Dual-Compartment Identity/Credit Vault (CLIN 0033 v7.7): Provides 0-click Next-of-Kin (NOK) and ICE medical triage "
            "during site emergencies, while locking Employee personal credit/loan protection and Employer internal HR/I-9/clearance records into mutually isolated cryptographic compartments.\n"
            "3. 100% Air-Gapped Bare-Metal Sovereignty: 631 Core Modules (Merkle: cc1ee1c8...949a), 83 Core + 8 Next-Gen Unit Test Suites, & 1,420 Field Academy Exam Questions.\n\n"
            "Public Verification Mirrors:\n"
            "* TRL 7 Core Console: https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public\n"
            "* TRL 8/9 Next-Gen Forge: https://github.com/mrshumphrey3251-ai/hvf-sovereign-nextgen-public\n"
            "Contact: Jeffery Humphrey, CEO | humphreyvirtualfarm@gmail.com | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5"
        )
        co_email = (
            f"Subject: CAGE 1AHA8 / UEI S1M4ENLHTDH5 // Sovereign C2, 36.75ns Robotics Safety, & Dual-Compartment Identity/Credit Vault for {prospect_agency_or_company}\n\n"
            f"Dear Contracting Officer / Technical Evaluation Lead ({prospect_agency_or_company}),\n\n"
            "Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5) is pleased to submit our Federal Capability Statement and Per-Node Commercial Price Schedule "
            "for the HVF Level-5 Sovereign Command & Control Operating Console (Project Ebony - Tradewinds Dockets 10-26-3952 & 9-26-3703) and our TRL 8/9 Expansion Suite (CLIN 0027 - CLIN 0034).\n\n"
            "- Frozen TRL 7 Core Baseline (Port 8501): 631 Compiled Modules, 83 Passing Test Suites, 54 WORM SQLite Tables, 36.75ns SiC MOSFET Hardware Interlock, & 1,420 Field Academy Questions.\n"
            "- Pre-Engineered TRL 8/9 Expansion Suite (Port 8502): Day-1 License & WAWF Generator (CLIN 0027), 36.75ns SiC Board (CLIN 0028), PLC/60Hz SCADA/J1939 Mapper (CLIN 0029), "
            "UAS GLI & OK Title 61 GIS (CLIN 0030), Watch-Floor Bitwise RBAC (CLIN 0031), DoD RMF ATO & 50-Seat Academy (CLIN 0032), and 60-Field Proof-of-Identity, Emergency ICE Triage, & Dual-Compartment Credit Shield (CLIN 0033 v7.7).\n\n"
            "Every individual module is licensed per physical hardware node strictly below the $250,000 Simplified Acquisition Threshold (with CLIN 0001 Entry Pilot at $24,500/yr).\n\n"
            "Respectfully,\nJeffery Humphrey -- Founder, CEO, & Principal Sovereign Architect\nHumphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | humphreyvirtualfarm@gmail.com"
        )
        return {"linkedin_broadcast": linkedin_post, "contracting_officer_email": co_email}

    def generate_wp8_capability_and_quote_dossier(
        self,
        out_dir: pathlib.Path,
        prospect_agency_or_company: str = "TINKER AFB // OC-ALC DEPOT MAINTENANCE DIRECTORATE",
        selected_clin_keys: List[str] | None = None,
        node_count: int = 1,
    ) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        quote = self.build_custom_quote(
            prospect_agency_or_company=prospect_agency_or_company,
            selected_clin_keys=selected_clin_keys,
            node_count=node_count,
        )
        outreach = self.generate_outreach_templates(prospect_agency_or_company=prospect_agency_or_company)

        seal_str = f"WP8|{quote['quote_verification_seal']}|{quote['total_annual_ffp_quote_usd']}|{FROZEN_EBONY_MERKLE_ROOT}"
        worm_seal = hashlib.sha256(seal_str.encode("utf-8")).hexdigest()

        lines = [
            "# HUMPHREY VIRTUAL FARMS LLC // FEDERAL CAPABILITY STATEMENT & FIRM-FIXED-PRICE QUOTE",
            "**Entity:** Humphrey Virtual Farms LLC (`CAGE: 1AHA8` | `SAM.gov UEI: S1M4ENLHTDH5`)",
            "**Controlling Authority:** Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect (`humphreyvirtualfarm@gmail.com`)",
            "**Procurement Vehicles:** DoD CDAO Tradewinds (`10-26-3952` & `9-26-3703`), `10 U.S.C. 4022 OTA`, `FAR Part 12 / Part 13`, `OK Title 61`",
            f"**Host Ebony Baseline Merkle Root:** `{FROZEN_EBONY_MERKLE_ROOT}`",
            "",
            "---",
            "",
            "## 1. Core Competencies & Sovereign Technical Differentiators",
            "* **100% Bare-Metal Air-Gapped C2 (`Project Ebony` TRL 7):** `631` compiled Python modules, `83` test suites, `54` WORM SQLite audit tables, `0` cloud dependencies (`>42.5%` 5-year lifecycle cost avoidance).",
            "* **36.75ns SiC MOSFET Hardware Interlock (`CLIN 0006` & `CLIN 0028`):** `18.50ns + 12.00ns + 6.25ns = 36.75ns` physical actuator cutoff (`0.0551 um` stop at `1,500 mm/s` vs `225.0 mm` legacy PLC).",
            "* **60-Field Proof-of-Identity, Emergency ICE Triage, & Dual-Compartment Credit Shield (`CLIN 0033 v7.7`):** 0-click Emergency ICE Triage Roster, User Agreement Gate, Employee Personal Credit/Loan Compartment (hidden from Employer), & Employer Internal HR/I-9/Clearance Compartment (unalterable lock).",
            "* **Sovereign Field Academy (`CLIN 0011` & `CLIN 0032`):** `1,420` verified exam questions (`800` Ch.1 + `620` Ch.5), `4` offline textbooks, and DoD RMF / NIST 800-53 Rev 5 ATO (`0` CAT I/II/III findings).",
            "",
            "---",
            "",
            f"## 2. Custom Firm-Fixed-Price (FFP) Quote for `{quote['prospect_agency_or_company']}`",
            f"* **Quote Verification Seal:** `{quote['quote_verification_seal']}` | **Node Quantity:** `{quote['node_count']}`",
            f"* **Recommended Acquisition Vehicle:** `{quote['recommended_contract_vehicle']}`",
            f"* **Total Annual FFP Quote:** **`${quote['total_annual_ffp_quote_usd']:,.2f} USD`**",
            f"* **Immediate Day-1 WAWF Mobilization Invoice:** **`${quote['day1_mobilization_invoice_usd']:,.2f} USD`**",
            f"* **Executive Allocation Telemetry:** `{quote['internal_margin_telemetry']}`",
            "",
            "### Quoted CLIN Line Items:",
        ]
        for li in quote["line_items"]:
            lines.append(f"* **{li['CLIN_Item']}:** `{li['Per_Node_Annual_USD']}` x `{li['Node_Qty']} Node(s)` = **`{li['Extended_Annual_USD']}`**")
        lines.extend([
            "",
            "---",
            f"**WORM WP-8 Capability Statement & Quote Seal (SHA-256):** `{worm_seal}`",
        ])

        md_text = "\n".join(lines) + "\n"
        md_file = out_dir / "WP8_HVF_FEDERAL_CAPABILITY_STATEMENT_AND_QUOTE.md"
        pdf_file = out_dir / "WP8_HVF_FEDERAL_CAPABILITY_STATEMENT_AND_QUOTE.pdf"
        md_file.write_bytes(md_text.encode("ascii", errors="ignore"))
        pdf_bytes = build_minimal_iso_pdf(lines)
        pdf_file.write_bytes(pdf_bytes)

        return {
            "quote": quote,
            "outreach": outreach,
            "worm_seal": worm_seal,
            "md_path": str(md_file),
            "pdf_path": str(pdf_file),
            "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        }
