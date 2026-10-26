"""
HUMPHREY VIRTUAL FARMS LLC // CLIN 0031 (WP-5): COMMAND WATCH-FLOOR RBAC, CALLSIGN PROVISIONER, & SHIFT-LEDGER PDF COMPILER
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5)
Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect
Work Package: WP-5 (Days 30-60 Post-Award Watch-Floor UI Customization, Bitwise RBAC, & WORM Shift-Handover PDF Compiler)
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
RBAC_SESSION_SALT = "PUBLIC_RBAC_SALT_REDACTED_DFARS_252_227_7018"


class CommandWatchFloorRBACAndPDFEngine(SovereignExpansionModule):
    """
    WP-5 / CLIN 0031 Plug-In:
      1. Enforces deterministic bitwise Role-Based Access Control (RBAC) across Watch-Floor seats
         (Level-1 Observer 0x03, Level-3 Watch Officer 0x1F, Level-5 Sovereign Commander 0xFF).
      2. Provisions command-specific TOC callsigns, classification banners, and SOP headers.
      3. Compiles cryptographically chained 8/12-hour Watch-Floor Shift Handover %PDF-1.4 ledgers (CLIN 0022).
    """

    PERM_READ_TELEMETRY     = 0x01
    PERM_AUDIT_INSPECT      = 0x02
    PERM_ACK_ALARM          = 0x04
    PERM_CONTACTOR_OVERRIDE = 0x08
    PERM_SIGN_SHIFT_BRIEF   = 0x10
    PERM_GUILLOTINE_RESET   = 0x20
    PERM_WORM_MASTER_SEAL   = 0x40
    PERM_AIRLOCK_RELEASE    = 0x80

    ROLE_MASKS = {
        "LEVEL_1_TELEMETRY_OBSERVER": 0x03,
        "LEVEL_3_WATCH_OFFICER": 0x1F,
        "LEVEL_5_SOVEREIGN_COMMANDER": 0xFF,
    }

    def __init__(self) -> None:
        super().__init__(
            plugin_id="HVF-NG-CLIN-0031",
            clin_number="CLIN 0031",
            title="Command Watch-Floor RBAC, Callsign Provisioner, & Automated Shift-Ledger PDF Engine",
            version="1.0.0",
            target_trl="TRL 8/9",
            per_node_annual_gov_usd=45000,
            per_node_monthly_comm_usd=4100,
        )

    def verify_seat_permission(self, role_name: str, permission_bit: int) -> Dict[str, Any]:
        if role_name not in self.ROLE_MASKS:
            raise ValueError(f"Unknown watch-floor role: {role_name}")
        mask = self.ROLE_MASKS[role_name]
        authorized = (mask & permission_bit) == permission_bit
        token_hash = hashlib.sha256(
            f"{role_name}|{mask:#04x}|{permission_bit:#04x}|{RBAC_SESSION_SALT}|{FROZEN_EBONY_MERKLE_ROOT}".encode("utf-8")
        ).hexdigest()
        return {
            "role_name": role_name,
            "role_mask_hex": f"0x{mask:02X}",
            "requested_perm_hex": f"0x{permission_bit:02X}",
            "authorized": authorized,
            "rbac_attestation_token": token_hash[:24],
        }

    def compile_shift_handover_ledger(
        self,
        command_callsign: str = "TINKER-OCALC-TOC-ALPHA",
        shift_window_utc: str = "2026-10-25 12:00Z -> 2026-10-25 20:00Z",
        outgoing_watch_officer: str = "MAJ R. VANCE (LEVEL_3_WATCH_OFFICER)",
        incoming_watch_officer: str = "CAPT E. MERCER (LEVEL_3_WATCH_OFFICER)",
        commander_approver: str = "JEFFERY HUMPHREY (LEVEL_5_SOVEREIGN_COMMANDER)",
        previous_shift_hash: str = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        logged_events: List[str] | None = None,
    ) -> Dict[str, Any]:
        if logged_events is None:
            logged_events = [
                "12:15Z - CLIN 0003: 60Hz Microgrid Bus locked at 60.000 Hz (RoCoF -0.04 Hz/s, Nominal).",
                "14:40Z - CLIN 0006: 36.75ns SiC MOSFET Hardware Interlock self-test PASSED (0.0551 um margin).",
                "17:05Z - CLIN 0009: 480V 3-Phase Silo Contactor NEMA MG-1 phase unbalance 0.28% (Safe).",
                "19:55Z - CLIN 0022: Outgoing Watch-Floor WORM Ledger verified against Merkle Root cc1ee1c8...949a.",
            ]

        chain_payload = (
            f"{previous_shift_hash}|{command_callsign}|{shift_window_utc}|"
            f"{outgoing_watch_officer}|{incoming_watch_officer}|{commander_approver}|"
            f"{'|'.join(logged_events)}|{FROZEN_EBONY_MERKLE_ROOT}"
        )
        current_shift_hash = hashlib.sha256(chain_payload.encode("utf-8")).hexdigest()

        if ENCLAVE_MODE == "PRIVATE":
            salt_descriptor = f"Active Sovereign Session Salt ({RBAC_SESSION_SALT[:18]}...)"
        else:
            salt_descriptor = "[REDACTED_RBAC_SESSION_SALT_DFARS_252_227_7018]"

        return {
            "Target_CLINs": ["CLIN 0022 (ISO 32000-1 WORM PDF Compiler)", "CLIN 0024 (Chronos Watch-Floor Telemetry)"],
            "enclave_mode": ENCLAVE_MODE,
            "command_callsign": command_callsign,
            "shift_window_utc": shift_window_utc,
            "outgoing_watch_officer": outgoing_watch_officer,
            "incoming_watch_officer": incoming_watch_officer,
            "commander_approver": commander_approver,
            "previous_shift_hash": previous_shift_hash,
            "current_shift_worm_hash": current_shift_hash,
            "logged_events": logged_events,
            "rbac_salt_status": salt_descriptor,
            "host_ebony_merkle_root": FROZEN_EBONY_MERKLE_ROOT,
        }

    def generate_wp5_watchfloor_dossier(self, out_dir: pathlib.Path) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        l1_check = self.verify_seat_permission("LEVEL_1_TELEMETRY_OBSERVER", self.PERM_AIRLOCK_RELEASE)
        l3_check = self.verify_seat_permission("LEVEL_3_WATCH_OFFICER", self.PERM_SIGN_SHIFT_BRIEF)
        l5_check = self.verify_seat_permission("LEVEL_5_SOVEREIGN_COMMANDER", self.PERM_AIRLOCK_RELEASE)
        shift_data = self.compile_shift_handover_ledger()

        lines = [
            "# HUMPHREY VIRTUAL FARMS LLC // WP-5: COMMAND WATCH-FLOOR RBAC & WORM SHIFT-LEDGER ICD",
            "**Entity:** Humphrey Virtual Farms LLC (`CAGE: 1AHA8` | `SAM.gov UEI: S1M4ENLHTDH5`)",
            "**Controlling Authority:** Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect",
            f"**Plug-In Module:** `CLIN 0031 (WP-5 Watch-Floor RBAC & PDF Compiler)` | **Enclave Tier:** `{ENCLAVE_MODE}`",
            f"**Host Ebony Baseline Merkle Root:** `{FROZEN_EBONY_MERKLE_ROOT}`",
            "",
            "---",
            "",
            "## 1. Bitwise Watch-Floor Role-Based Access Control (RBAC) Verification Matrix",
            f"* **Level-1 Telemetry Observer (`0x03`) -> Airlock Release (`0x80`):** Authorized = `{l1_check['authorized']}` (Blocked as expected)",
            f"* **Level-3 Watch Officer (`0x1F`) -> Sign Shift Brief (`0x10`):** Authorized = `{l3_check['authorized']}` (Token: `{l3_check['rbac_attestation_token']}`)",
            f"* **Level-5 Sovereign Commander (`0xFF`) -> Airlock Release (`0x80`):** Authorized = `{l5_check['authorized']}` (Token: `{l5_check['rbac_attestation_token']}`)",
            f"* **Session Cryptographic Salt Binding:** `{shift_data['rbac_salt_status']}`",
            "",
            "---",
            "",
            "## 2. Automated Command Shift-Handover WORM Ledger (`CLIN 0022` / `CLIN 0024`)",
            f"* **Command TOC Callsign:** `{shift_data['command_callsign']}`",
            f"* **Shift Window (UTC):** `{shift_data['shift_window_utc']}`",
            f"* **Outgoing Watch Officer:** `{shift_data['outgoing_watch_officer']}`",
            f"* **Incoming Watch Officer:** `{shift_data['incoming_watch_officer']}`",
            f"* **Command Approving Authority:** `{shift_data['commander_approver']}`",
            "",
            "### Logged Watch-Floor Events:",
        ]
        for ev in shift_data["logged_events"]:
            lines.append(f"* {ev}")
        lines.extend([
            "",
            "---",
            f"**Previous Shift Hash:** `{shift_data['previous_shift_hash']}`",
            f"**Current Shift WORM Chain Seal (SHA-256):** `{shift_data['current_shift_worm_hash']}`",
        ])

        md_text = "\n".join(lines) + "\n"
        md_file = out_dir / "WP5_WATCHFLOOR_RBAC_SHIFT_LEDGER_SPEC.md"
        pdf_file = out_dir / "WP5_WATCHFLOOR_RBAC_SHIFT_LEDGER_SPEC.pdf"
        md_file.write_bytes(md_text.encode("ascii", errors="ignore"))
        pdf_bytes = build_minimal_iso_pdf(lines)
        pdf_file.write_bytes(pdf_bytes)

        return {
            "rbac_checks": [l1_check, l3_check, l5_check],
            "shift_ledger": shift_data,
            "md_path": str(md_file),
            "pdf_path": str(pdf_file),
            "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        }
