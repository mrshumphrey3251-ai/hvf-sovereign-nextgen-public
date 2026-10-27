"""
HVF Sovereign Next-Gen Work Package 9 (CLIN 0035 v8.0):
Automated Federal Capability Statement, 35-CLIN ($2,230,000/yr/Node) Custom Quote
Compiler, B2C Personal Shield Revenue Projections, & Contracting Officer Outreach Engine.
Controlling Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect (CAGE 1AHA8)
"""
from __future__ import annotations

import hashlib
import hmac
import pathlib
from typing import Any, Dict, List

from plugins.clin_0031_command_watchfloor_rbac_pdf_engine import compile_single_page_pdf_14
from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, PluginManifest, SovereignExpansionModule

ENCLAVE_MODE = "PUBLIC"
QUOTE_SIGNING_SECRET = "PUBLIC_QUOTE_SECRET_REDACTED_DFARS_252_227_7018"


class FederalCapabilityAndQuoteEngine(SovereignExpansionModule):
    """
    WP-9 (CLIN 0035 v8.0): Synthesizes official DoD/Federal Capability Statements,
    35-CLIN ($2,230,000/yr/Node) Firm-Fixed-Price Quotes, Day-1 WAWF Invoicing,
    and ready-to-send Contracting Officer / LinkedIn outreach packets.
    """

    CORPORATE_IDENTIFIERS: Dict[str, str] = {
        "Legal_Entity": "Humphrey Virtual Farms LLC",
        "Controlling_Authority": "Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect",
        "CAGE_Code": "1AHA8",
        "SAM_UEI": "S1M4ENLHTDH5",
        "Primary_Email": "humphreyvirtualfarm@gmail.com",
        "Tradewinds_Dockets": "DoD CDAO Tradewinds Awardable Dockets 10-26-3952 & 9-26-3703",
        "Primary_NAICS": "541512, 541330, 541715, 334511, 221114, 115112",
        "PSC_Codes": "DA01, DG10, R425, AC32, 6117",
        "Acquisition_Vehicles": "FAR Part 12 Commercial Item, FAR 13.5 Simplified ($7.5M), 10 U.S.C. 4022 Sole-Source OTA",
    }

    COMPLETE_35_CLIN_CATALOG: List[Dict[str, Any]] = [
        {
            "CLIN": "CLIN 0001 - CLIN 0026",
            "Package": "Frozen TRL 7 Tradewinds Core (Port 8501)",
            "Title": "26-CLIN Sovereign C2 Core (36.75ns SiC Guillotine, 60Hz Microgrid, Louhaichi GLI, Title 61 Retainage, 1,420-Q Academy & 380-File Vault)",
            "Annual_Price_Per_Node_USD": 1630000,
        },
        {
            "CLIN": "CLIN 0027",
            "Package": "WP-1",
            "Title": "Automated Day-1 Cryptographic Hardware-UUID License Key & WAWF Invoice Packet Generator",
            "Annual_Price_Per_Node_USD": 35000,
        },
        {
            "CLIN": "CLIN 0028",
            "Package": "WP-2",
            "Title": "36.75ns SiC MOSFET Solid-State Hardware Interlock Board & IPC-2221B BOM Generator",
            "Annual_Price_Per_Node_USD": 65000,
        },
        {
            "CLIN": "CLIN 0029",
            "Package": "WP-3",
            "Title": "Site-Specific PLC, 60Hz Microgrid SCADA (Modbus/DNP3), & 29-Bit SAE J1939 CAN-Bus Mapper",
            "Annual_Price_Per_Node_USD": 75000,
        },
        {
            "CLIN": "CLIN 0030",
            "Package": "WP-4",
            "Title": "UAS Optical Louhaichi GLI Feed, Gauss Shoelace Survey, & Oklahoma Title 61 (5.0% Retainage) GIS Engine",
            "Annual_Price_Per_Node_USD": 75000,
        },
        {
            "CLIN": "CLIN 0031",
            "Package": "WP-5",
            "Title": "Command Watch-Floor Bitwise RBAC (0x03/0x1F/0xFF), Callsign Provisioner, & WORM Shift-Handover PDF Engine",
            "Annual_Price_Per_Node_USD": 45000,
        },
        {
            "CLIN": "CLIN 0032",
            "Package": "WP-6",
            "Title": "DoD RMF / NIST 800-53 Rev 5 / eMASS ATO STIG Synthesizer & 50-Seat Field Academy Cohort Provisioner",
            "Annual_Price_Per_Node_USD": 125000,
        },
        {
            "CLIN": "CLIN 0033",
            "Package": "WP-7",
            "Title": "Standalone Personal Sovereign Identity, 7-Channel Credit/Loan/Deed/SIM Anti-Fraud Shield (50-Seat Pack + $350/yr B2C)",
            "Annual_Price_Per_Node_USD": 65000,
        },
        {
            "CLIN": "CLIN 0034",
            "Package": "WP-8",
            "Title": "Enterprise HR, Front-Screen OSHA Muster, HIPAA Medical/ICE Triage, Zero-Trust 2-Person 60-Field Dossier & Promotion Board",
            "Annual_Price_Per_Node_USD": 85000,
        },
        {
            "CLIN": "CLIN 0035",
            "Package": "WP-9",
            "Title": "Automated Federal Capability Statement, 35-CLIN Custom Quote Compiler & Outreach Engine",
            "Annual_Price_Per_Node_USD": 30000,
        },
    ]

    def __init__(self) -> None:
        super().__init__(
            plugin_id="HVF-NG-CLIN-0035",
            clin_number="CLIN 0035",
            title="Automated Federal Capability Statement, 35-CLIN ($2,230,000/yr) Custom Quote & Outreach Engine (v8.0)",
            version="8.0.0",
            target_trl="TRL 8/9",
            per_node_annual_gov_usd=30000,
            per_node_monthly_comm_usd=2800,
        )
        self.manifest = self.export_manifest()

    def build_custom_quote(
        self,
        customer_agency: str = "U.S. Department of Defense / CDAO Tradewinds Contracting Office",
        node_count: int = 1,
        include_frozen_core: bool = True,
        selected_nextgen_clins: List[str] | None = None,
    ) -> Dict[str, Any]:
        nodes = max(1, int(node_count))
        if selected_nextgen_clins is None:
            selected_nextgen_clins = [f"CLIN 00{k}" for k in range(27, 36)]

        line_items: List[Dict[str, Any]] = []
        single_node_total = 0

        for item in self.COMPLETE_35_CLIN_CATALOG:
            cid = item["CLIN"]
            if cid.startswith("CLIN 0001"):
                if not include_frozen_core:
                    continue
            else:
                if cid not in selected_nextgen_clins:
                    continue
            unit_p = int(item["Annual_Price_Per_Node_USD"])
            ext_p = unit_p * nodes
            single_node_total += unit_p
            line_items.append({
                "CLIN": cid,
                "Work_Package": item["Package"],
                "Capability_Description": item["Title"],
                "Unit_Price_Per_Node_USD": f"${unit_p:,.2f}",
                "Node_Qty": nodes,
                "Extended_Annual_FFP_USD": f"${ext_p:,.2f}",
            })

        grand_total = single_node_total * nodes
        day1_wawf = grand_total if grand_total <= 250000 else int(grand_total * 0.50)
        ceo_35pct = round(day1_wawf * 0.35, 2)

        quote_payload = f"{customer_agency}|{nodes}|{grand_total}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8")
        quote_hmac = hmac.new(QUOTE_SIGNING_SECRET.encode("utf-8"), quote_payload, hashlib.sha256).hexdigest()

        ko_email = chr(10).join([
            f"SUBJECT: Sole-Source / Commercial Firm-Fixed-Price Proposal -- Humphrey Virtual Farms LLC (CAGE 1AHA8 | UEI S1M4ENLHTDH5) -- {customer_agency}",
            "",
            f"TO: Contracting Officer / Procuring Activity ({customer_agency})",
            "FROM: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect | Humphrey Virtual Farms LLC",
            "CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5 | Email: humphreyvirtualfarm@gmail.com",
            "TRADEWINDS DOCKETS: DoD CDAO Awardable Dockets 10-26-3952 & 9-26-3703",
            "",
            f"1. EXECUTIVE SUMMARY & FIRM-FIXED-PRICE QUOTE (${grand_total:,.2f}/yr Across {nodes} Node(s)):",
            "   Humphrey Virtual Farms LLC submits this pre-engineered, TRL 7/8/9 air-gapped Sovereign C2 & Next-Gen",
            f"   Expansion Quote totaling ${grand_total:,.2f}/yr (${single_node_total:,.2f}/yr per physical node).",
            f"   - Day-1 WAWF Mobilization / COTS License Invoice: ${day1_wawf:,.2f}",
            "   - Frozen Core Merkle Root (Port 8501): cc1ee1c8d29b2ae5e856fc0fcb672a52e7e49d50369499febe14e18e9150949a",
            f"   - Cryptographic Quote HMAC-SHA256 Seal: {quote_hmac}",
            "",
            "2. KEY TECHNICAL & STATUTORY DIFFERENTIATORS:",
            "   - 36.75ns SiC MOSFET Hardware Interlock (0.055125 um stop @ 1,500 mm/s vs 225.0 mm legacy PLC).",
            "   - CLIN 0033 (WP-7): Standalone Personal 7-Channel Credit, Loan, Home Deed & SIM-Swap Shield ($65K/Node or $350/yr B2C).",
            "   - CLIN 0034 (WP-8): Enterprise HR, Front-Screen OSHA Muster, HIPAA Medical/ICE Triage, Zero-Trust 2-Person (NIST AC-5)",
            "     60-Field Personnel Dossier & Automated Promotion Shortlist Puller ($85K/Node).",
            "",
            "Respectfully submitted,",
            "Jeffery Humphrey",
            "Founder, CEO, & Principal Sovereign Architect | Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)",
        ])

        linkedin_post = chr(10).join([
            "HVF SOVEREIGN ARCHITECTURE UPDATE // 35-CLIN ($2,230,000/YR/NODE) ENTERPRISE & PERSONAL SHIELD SUITE LIVE",
            "",
            "Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5) has officially decoupled and sealed our",
            "Personal Anti-Fraud Shield and Enterprise HR / Emergency Triage Command Suite:",
            "",
            "1. WP-7 (CLIN 0033): Standalone Personal Sovereign Identity, 7-Channel Credit Bureau, Loan, Home Deed APN,",
            "   & SIM-Swap Anti-Fraud Shield -- 100% owned by the individual user ($29.99/mo | $350/yr B2C or $65K/yr 50-Seat Node)",
            "   with ZERO employer visibility.",
            "2. WP-8 (CLIN 0034): Enterprise HR, Zero-Second Front-Screen OSHA 1910.38 Muster SOPs, HIPAA 45 CFR 164.502",
            "   Medical/Allergy/Blood/ICE Triage, Zero-Trust Two-Person Integrity (NIST SP 800-53 AC-5) 60-Field Dossier,",
            "   & 1-Click Promotion Shortlist Puller ($85K/yr/Node).",
            "",
            "Contact: Jeffery Humphrey, Founder & CEO | humphreyvirtualfarm@gmail.com | CAGE: 1AHA8",
        ])

        return {
            "customer_agency": customer_agency,
            "node_count": nodes,
            "line_items": line_items,
            "single_node_annual_usd": single_node_total,
            "grand_total_annual_usd": grand_total,
            "day1_wawf_invoice_usd": day1_wawf,
            "ceo_day1_allocation_35pct_usd": ceo_35pct,
            "quote_hmac_sha256": quote_hmac,
            "contracting_officer_email_text": ko_email,
            "linkedin_executive_broadcast_text": linkedin_post,
        }

    def generate_wp8_capability_and_quote_packet(
        self,
        out_dir: pathlib.Path,
        customer_agency: str = "U.S. Department of Defense / CDAO Tradewinds Contracting Office",
        node_count: int = 1,
    ) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        q = self.build_custom_quote(customer_agency=customer_agency, node_count=node_count)

        md_lines = [
            "# HVF SOVEREIGN NEXT-GEN // WP-9 (CLIN 0035 v8.0): FEDERAL CAPABILITY STATEMENT & 35-CLIN ($2,230,000/YR) QUOTE",
            f"- **Legal Entity**: {self.CORPORATE_IDENTIFIERS['Legal_Entity']} (CAGE `{self.CORPORATE_IDENTIFIERS['CAGE_Code']}` | UEI `{self.CORPORATE_IDENTIFIERS['SAM_UEI']}`)",
            f"- **Controlling Authority**: {self.CORPORATE_IDENTIFIERS['Controlling_Authority']} (`{self.CORPORATE_IDENTIFIERS['Primary_Email']}`)",
            f"- **Target Procuring Agency**: {q['customer_agency']} (`{q['node_count']}` Node(s))",
            f"- **Single-Node 35-CLIN Catalog Value**: `${q['single_node_annual_usd']:,.2f}/yr` | **Extended Quote Total**: `${q['grand_total_annual_usd']:,.2f}/yr`",
            f"- **Day-1 WAWF Mobilization / License Invoice**: `${q['day1_wawf_invoice_usd']:,.2f}` (`35.0%` CEO Distribution: `${q['ceo_day1_allocation_35pct_usd']:,.2f}`)",
            f"- **Quote HMAC-SHA256 Seal**: `{q['quote_hmac_sha256']}`",
            "",
            "## 35-CLIN Firm-Fixed-Price Schedule",
            "| CLIN | Package | Capability_Description | Unit_Price | Qty | Extended_FFP |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for row in q["line_items"]:
            md_lines.append(
                f"| `{row['CLIN']}` | `{row['Work_Package']}` | {row['Capability_Description']} | {row['Unit_Price_Per_Node_USD']} | {row['Node_Qty']} | {row['Extended_Annual_FFP_USD']} |"
            )

        md_content = chr(10).join(md_lines) + chr(10)
        md_path = out_dir / "WP9_HVF_FEDERAL_CAPABILITY_STATEMENT_AND_QUOTE.md"
        pdf_path = out_dir / "WP9_HVF_FEDERAL_CAPABILITY_STATEMENT_AND_QUOTE.pdf"
        md_path.write_bytes(md_content.encode("ascii"))

        worm_seal = hashlib.sha256(md_content.encode("ascii")).hexdigest()
        pdf_lines = [line.replace("`", "").replace("*", "") for line in md_lines]
        pdf_bytes = compile_single_page_pdf_14(
            title="HVF WP-9 (CLIN 0035 v8.0): FEDERAL CAPABILITY STATEMENT & 35-CLIN QUOTE",
            lines=pdf_lines,
            worm_sha256=worm_seal,
        )
        pdf_path.write_bytes(pdf_bytes)

        return {
            "manifest": self.manifest,
            "quote": q,
            "md_path": str(md_path),
            "pdf_path": str(pdf_path),
            "pdf_bytes_len": len(pdf_bytes),
            "worm_seal": worm_seal,
        }
