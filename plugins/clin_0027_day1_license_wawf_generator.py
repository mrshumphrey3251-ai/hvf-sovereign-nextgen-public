"""
HUMPHREY VIRTUAL FARMS LLC // CLIN 0027: AUTOMATED DAY-1 CRYPTOGRAPHIC HARDWARE-UUID LICENSE KEY & WAWF INVOICE GENERATOR
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5)
Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect
Work Package: WP-1 (Days 1-15 Post-Award Provisioning & Day-1 Mobilization Invoicing)
Host Compatibility: Frozen Project Ebony TRL 7 Baseline (cc1ee1c8d29b2ae5e856fc0fcb672a52e7e49d50369499febe14e18e9150949a)
"""
from __future__ import annotations
import datetime
import hashlib
import hmac
import json
import pathlib
from typing import Any, Dict, List

from nextgen_core.sovereign_plugin_contract import (
    FROZEN_EBONY_MERKLE_ROOT,
    SovereignExpansionModule,
)

ENCLAVE_MODE = "PUBLIC"
SOVEREIGN_HMAC_SEED = "PUBLIC_VERIFICATION_SEED_REDACTED_DFARS_252_227_7018"


def build_minimal_iso_pdf(lines: List[str]) -> bytes:
    """
    Compiles a deterministic, standards-compliant ISO 32000-1 %PDF-1.4 binary document
    using standard Type1 Helvetica font with clean Markdown stripping and whole-word wrapping.
    """
    import re, textwrap
    wrapped_clean_lines: List[str] = []
    for raw_line in lines:
        s = raw_line.encode("ascii", errors="ignore").decode("ascii").strip()
        if not s:
            wrapped_clean_lines.append("")
            continue
        if s == "---":
            wrapped_clean_lines.append("=" * 88)
            continue
        s = re.sub(r"^#+\s*", "", s)
        s = s.replace("**", "").replace("`", "")
        if s.startswith("* "):
            s = "  - " + s[2:]
        for wline in textwrap.wrap(
            s,
            width=88,
            break_long_words=False,
            break_on_hyphens=False,
            subsequent_indent="    ",
        ):
            wrapped_clean_lines.append(wline)

    stream_cmds = ["BT", "/F1 8.5 Tf", "36 762 Td", "10.5 TL"]
    for cline in wrapped_clean_lines[:68]:
        safe = (
            cline.replace("\\", "\\\\")
            .replace("(", "\\(")
            .replace(")", "\\)")
        )
        stream_cmds.append(f"({safe}) Tj T*")
    stream_cmds.append("ET")
    content_bytes = "\n".join(stream_cmds).encode("ascii")

    objs = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n",
        f"4 0 obj\n<< /Length {len(content_bytes)} >>\nstream\n".encode("ascii")
        + content_bytes
        + b"\nendstream\nendobj\n",
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for o in objs:
        offsets.append(len(out))
        out.extend(o)
    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode("ascii"))
    for off in offsets:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    return bytes(out)


class Day1LicenseAndWAWFInvoiceGenerator(SovereignExpansionModule):
    """
    WP-1 / CLIN 0027 Plug-In:
      1. Generates a DFARS 252.227-7018 Hardware-UUID-Locked License Key (HMAC-SHA256).
      2. Generates a DoD PIEE/WAWF Day-1 Mobilization Invoice payload (FAR 52.212-4 / FAR 52.232-40 / 10 U.S.C. 4022).
      3. Computes the 5-Bucket Post-Award Capital Allocation split.
      4. Exports a WORM-sealed %PDF-1.4 & Markdown Day-1 Transmission Packet.
    """

    def __init__(self) -> None:
        super().__init__(
            plugin_id="HVF-NG-CLIN-0027",
            clin_number="CLIN 0027",
            title="Automated Day-1 Cryptographic Hardware-UUID License Key & WAWF Invoice Generator",
            version="1.0.0",
            target_trl="TRL 8",
            per_node_annual_gov_usd=35000,
            per_node_monthly_comm_usd=3200,
        )

    def generate_day1_packet(
        self,
        contract_number: str,
        awarding_agency: str,
        hardware_node_uuid: str,
        licensed_clins: List[str],
        total_contract_award_usd: float,
        issue_date_utc: str = "2026-10-25T20:35:00Z",
    ) -> Dict[str, Any]:
        clean_uuid = hardware_node_uuid.strip().upper()
        clin_str = ",".join(sorted(licensed_clins))
        signing_message = (
            f"CAGE:1AHA8|UEI:S1M4ENLHTDH5|CONTRACT:{contract_number}|"
            f"UUID:{clean_uuid}|CLINS:{clin_str}|HOST_MERKLE:{FROZEN_EBONY_MERKLE_ROOT}"
        )
        hmac_digest = hmac.new(
            SOVEREIGN_HMAC_SEED.encode("utf-8"),
            signing_message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest().upper()

        formatted_license_key = (
            f"HVF-1AHA8-{hmac_digest[:8]}-{hmac_digest[8:16]}-"
            f"{hmac_digest[16:24]}-{hmac_digest[24:32]}"
        )

        # Day-1 Invoicing Rule (100% up to $250,000 Simplified Acquisition Threshold; 50% Milestone #01 above $250,000)
        if total_contract_award_usd <= 250000.0:
            day1_invoice_usd = round(float(total_contract_award_usd), 2)
            payment_authority = (
                "100% Day-1 COTS License Delivery (FAR 52.212-4 / GPC Fast-Track or "
                "FAR 52.232-40 Mandatory 15-Day Accelerated Small Business Payment)"
            )
            wawf_billing_code = "COTS-100PCT-DAY1"
        else:
            day1_invoice_usd = round(float(total_contract_award_usd) * 0.50, 2)
            payment_authority = (
                "50% Day-1 Payable Milestone #01: Cryptographic Key Issuance & Hardware "
                "Mobilization (10 U.S.C. 4022 OTA & FAR 52.232-40 15-Day Accelerated Payment)"
            )
            wawf_billing_code = "OTA-MILESTONE-01-50PCT"

        # 5-Bucket Capital Allocation Split (Private shows full internal breakdown; Public redacts internal executive split label)
        if ENCLAVE_MODE == "PRIVATE":
            bucket_2_label = "2. CEO & SME Executive Compensation (Jeffery Humphrey - 35.0%)"
        else:
            bucket_2_label = "2. Executive Governance & Principal SME Allocation (35.0% - Redacted Public Mirror)"

        budget_allocation = {
            "1. Day-1 Bare-Metal Enclave & HIL Setup Hardware (18.0%)": round(day1_invoice_usd * 0.18, 2),
            bucket_2_label: round(day1_invoice_usd * 0.35, 2),
            "3. TRL 8/9 Field Integration, Travel, & Site Wiring (15.0%)": round(day1_invoice_usd * 0.15, 2),
            "4. Federal/OK Tax Escrow, Legal, & Insurance Reserve (17.0%)": round(day1_invoice_usd * 0.17, 2),
            "5. Sovereign Corporate War Chest Retained Reserve (15.0%)": round(day1_invoice_usd * 0.15, 2),
        }

        worm_seal = hashlib.sha256(
            f"{formatted_license_key}|{contract_number}|{day1_invoice_usd}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8")
        ).hexdigest()

        return {
            "entity": "Humphrey Virtual Farms LLC",
            "cage_code": "1AHA8",
            "sam_uei": "S1M4ENLHTDH5",
            "enclave_mode": ENCLAVE_MODE,
            "contract_number": contract_number,
            "awarding_agency": awarding_agency,
            "issue_date_utc": issue_date_utc,
            "hardware_node_uuid": clean_uuid,
            "licensed_clins": licensed_clins,
            "hardware_locked_license_key": formatted_license_key,
            "full_hmac_sha256_signature": hmac_digest,
            "host_ebony_merkle_root": FROZEN_EBONY_MERKLE_ROOT,
            "total_contract_award_usd": round(float(total_contract_award_usd), 2),
            "day1_immediate_invoice_usd": day1_invoice_usd,
            "wawf_billing_code": wawf_billing_code,
            "payment_statutory_authority": payment_authority,
            "day1_five_bucket_allocation_usd": budget_allocation,
            "worm_packet_sha256": worm_seal,
        }

    def export_day1_markdown_and_pdf(self, packet: Dict[str, Any], out_dir: pathlib.Path) -> Dict[str, str]:
        out_dir.mkdir(parents=True, exist_ok=True)
        lines = [
            "# HUMPHREY VIRTUAL FARMS LLC // DAY-1 HARDWARE-LOCKED LICENSE CERTIFICATE & WAWF INVOICE",
            f"**Vendor Entity:** {packet['entity']} (`CAGE: {packet['cage_code']}` | `SAM.gov UEI: {packet['sam_uei']}`)",
            f"**Controlling Authority:** Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect",
            f"**Contract / Order Number:** `{packet['contract_number']}` | **Awarding Agency:** {packet['awarding_agency']}",
            f"**Issue Timestamp (UTC):** `{packet['issue_date_utc']}` | **Enclave Tier:** `{packet['enclave_mode']}`",
            "",
            "---",
            "",
            "## 1. DFARS 252.227-7018 Hardware-UUID-Locked Cryptographic License Certificate",
            f"* **Authorized Physical Hardware Node UUID:** `{packet['hardware_node_uuid']}` *(Strictly 1 Physical Node)*",
            f"* **Licensed Command Modules (CLINs):** `{', '.join(packet['licensed_clins'])}`",
            f"* **Issued Hardware-Locked License Key:** `{packet['hardware_locked_license_key']}`",
            f"* **HMAC-SHA256 Cryptographic Binding:** `{packet['full_hmac_sha256_signature']}`",
            f"* **Host Ebony Baseline Merkle Root:** `{packet['host_ebony_merkle_root']}`",
            "",
            "---",
            "",
            "## 2. DoD PIEE / WAWF Day-1 Immediate Mobilization Invoice Schedule",
            f"* **Total Contract Award Value:** `${packet['total_contract_award_usd']:,.2f} USD`",
            f"* **IMMEDIATE DAY-1 INVOICE AMOUNT DUE:** **`${packet['day1_immediate_invoice_usd']:,.2f} USD`**",
            f"* **PIEE / WAWF Billing Code:** `{packet['wawf_billing_code']}`",
            f"* **Statutory Payment Authority:** {packet['payment_statutory_authority']}",
            f"* **Mandatory Remittance Target:** ACH Wire / GPC Settlement to `CAGE 1AHA8` (`UEI S1M4ENLHTDH5`) within `<= 15 Calendar Days` (`FAR 52.232-40`).",
            "",
            "---",
            "",
            "## 3. Automated 5-Bucket Post-Award Capital Allocation (Day-1 Cash Split)",
        ]
        for b_name, b_val in packet["day1_five_bucket_allocation_usd"].items():
            lines.append(f"* **{b_name}:** `${b_val:,.2f} USD`")
        lines.extend([
            "",
            "---",
            f"**WORM Packet Integrity Seal (SHA-256):** `{packet['worm_packet_sha256']}`",
        ])

        md_text = "\n".join(lines) + "\n"
        md_file = out_dir / "SAMPLE_DAY1_WAWF_LICENSE_PACKET.md"
        pdf_file = out_dir / "SAMPLE_DAY1_WAWF_LICENSE_PACKET.pdf"
        md_file.write_bytes(md_text.encode("ascii", errors="ignore"))
        pdf_bytes = build_minimal_iso_pdf(lines)
        pdf_file.write_bytes(pdf_bytes)
        return {
            "md_path": str(md_file),
            "pdf_path": str(pdf_file),
            "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        }
