"""
HUMPHREY VIRTUAL FARMS LLC // CLIN 0029 (WP-3): SITE PLC, 60HZ MICROGRID SCADA, & SAE J1939 CAN-BUS REGISTER MAPPER
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5)
Authority: Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect
Work Package: WP-3 (Days 15-45 Post-Award Site-Specific Modbus-TCP, DNP3, 480V Contactor, & J1939 CAN-Bus Binding)
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


class SitePLCSCADACANBusMapper(SovereignExpansionModule):
    """
    WP-3 / CLIN 0029 Plug-In:
      Unifies site-specific register translation across three core Project Ebony domains:
        1. CLIN 0003: 60Hz Microgrid Substation Relay (Modbus-TCP / DNP3 IEEE C37.118 Synchrophasor)
        2. CLIN 0009: 480V 3-Phase Grain Silo Contactor & Plenum Aeration PLC (NEMA MG-1 Phase Balance)
        3. CLIN 0008: SAE J1939 29-Bit Tactical Vehicle & Generator CAN-Bus Decoder (PGN 61444 / 65262)
    """

    def __init__(self) -> None:
        super().__init__(
            plugin_id="HVF-NG-CLIN-0029",
            clin_number="CLIN 0029",
            title="Site-Specific PLC, 60Hz Microgrid SCADA, & SAE J1939 CAN-Bus Register Mapper",
            version="1.0.0",
            target_trl="TRL 8",
            per_node_annual_gov_usd=75000,
            per_node_monthly_comm_usd=6800,
        )

    def evaluate_microgrid_60hz_relay(
        self,
        freq_hz: float = 59.985,
        rocof_hz_s: float = -0.12,
        bus_kv: float = 13.8,
    ) -> Dict[str, Any]:
        freq_dev_hz = round(abs(freq_hz - 60.000), 4)
        island_trip = (freq_dev_hz > 0.50) or (abs(rocof_hz_s) > 1.50)
        if ENCLAVE_MODE == "PRIVATE":
            reg_map = "Modbus Holding Reg 40001 (Freq mHz) | Reg 40003 (RoCoF mHz/s) | DNP3 CROB Point 0x0012 (PCC Breaker Trip)"
        else:
            reg_map = "[REDACTED_MODBUS_DNP3_REGISTER_MAP_DFARS_252_227_7018]"
        return {
            "Target_CLIN": "CLIN 0003 (60Hz Microgrid C2)",
            "freq_hz": freq_hz,
            "freq_deviation_hz": freq_dev_hz,
            "rocof_hz_s": rocof_hz_s,
            "substation_bus_kv": bus_kv,
            "pcc_islanding_breaker_trip": island_trip,
            "register_binding": reg_map,
        }

    def evaluate_480v_silo_contactor_plc(
        self,
        phase_a_v: float = 481.2,
        phase_b_v: float = 479.8,
        phase_c_v: float = 479.0,
        grain_moisture_pct: float = 13.4,
    ) -> Dict[str, Any]:
        v_avg = (phase_a_v + phase_b_v + phase_c_v) / 3.0
        max_dev = max(abs(phase_a_v - v_avg), abs(phase_b_v - v_avg), abs(phase_c_v - v_avg))
        unbalance_pct = round((max_dev / v_avg) * 100.0, 4)
        contactor_safe = (unbalance_pct <= 2.00) and (v_avg >= 440.0)
        aeration_fan_cmd = "ENERGIZE_480V_CONTACTOR" if (contactor_safe and grain_moisture_pct > 13.0) else "STANDBY_LOCKOUT"
        if ENCLAVE_MODE == "PRIVATE":
            plc_map = "Allen-Bradley/Siemens Coil 00017 (480V Main Contactor) | Input Reg 30041-30043 (L1/L2/L3 RMS Volts)"
        else:
            plc_map = "[REDACTED_480V_PLC_COIL_MAP_DFARS_252_227_7018]"
        return {
            "Target_CLIN": "CLIN 0009 (480V Grain Silo Contactor C2)",
            "v_avg_volts": round(v_avg, 2),
            "nema_mg1_phase_unbalance_pct": unbalance_pct,
            "contactor_interlock_safe": contactor_safe,
            "grain_moisture_pct": grain_moisture_pct,
            "aeration_contactor_command": aeration_fan_cmd,
            "plc_register_binding": plc_map,
        }

    def decode_sae_j1939_can_frame(
        self,
        can_id_29bit: int = 0x0CF00400,
        payload_8bytes: List[int] | None = None,
    ) -> Dict[str, Any]:
        if payload_8bytes is None:
            # Bytes 3 & 4 (0-indexed) in PGN 61444 encode Engine Speed at 0.125 RPM/bit
            # 0x3840 = 14400 * 0.125 = 1800.0 RPM
            payload_8bytes = [0xF0, 0x7D, 0x7D, 0x40, 0x38, 0xFF, 0xFF, 0xFF]
        priority = (can_id_29bit >> 26) & 0x07
        pgn = (can_id_29bit >> 8) & 0x3FFFF
        source_addr = can_id_29bit & 0xFF
        raw_rpm_word = (payload_8bytes[4] << 8) | payload_8bytes[3]
        engine_rpm = round(raw_rpm_word * 0.125, 2)
        if ENCLAVE_MODE == "PRIVATE":
            j1939_scaling = "SPN 190 (Bytes 4-5 Little-Endian * 0.125 RPM/bit) | CAN-FD Bridge SocketCAN can0 @ 500kbps"
        else:
            j1939_scaling = "[REDACTED_J1939_SPN_SCALING_DFARS_252_227_7018]"
        return {
            "Target_CLIN": "CLIN 0008 (Sovereign Auto & SAE J1939 CAN-Bus C2)",
            "can_id_hex": f"0x{can_id_29bit:08X}",
            "priority": priority,
            "pgn": pgn,
            "source_address": source_addr,
            "decoded_engine_rpm": engine_rpm,
            "j1939_bus_binding": j1939_scaling,
        }

    def generate_wp3_interface_dossier(self, out_dir: pathlib.Path) -> Dict[str, Any]:
        out_dir.mkdir(parents=True, exist_ok=True)
        m_res = self.evaluate_microgrid_60hz_relay()
        s_res = self.evaluate_480v_silo_contactor_plc()
        c_res = self.decode_sae_j1939_can_frame()

        seal_str = (
            f"WP3|{m_res['freq_deviation_hz']}|{s_res['nema_mg1_phase_unbalance_pct']}|"
            f"{c_res['pgn']}|{c_res['decoded_engine_rpm']}|{FROZEN_EBONY_MERKLE_ROOT}"
        )
        worm_seal = hashlib.sha256(seal_str.encode("utf-8")).hexdigest()

        lines = [
            "# HUMPHREY VIRTUAL FARMS LLC // WP-3: SITE PLC, 60HZ SCADA, & SAE J1939 CAN-BUS ICD",
            "**Entity:** Humphrey Virtual Farms LLC (`CAGE: 1AHA8` | `SAM.gov UEI: S1M4ENLHTDH5`)",
            "**Controlling Authority:** Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect",
            f"**Plug-In Module:** `CLIN 0029 (WP-3 Site Interface Adapter)` | **Enclave Tier:** `{ENCLAVE_MODE}`",
            f"**Host Ebony Baseline Merkle Root:** `{FROZEN_EBONY_MERKLE_ROOT}`",
            "",
            "---",
            "",
            "## 1. 60Hz Microgrid Substation Relay Binding (`CLIN 0003` -- IEEE C37.118 / Modbus / DNP3)",
            f"* **Measured Bus Frequency:** `{m_res['freq_hz']:.3f} Hz` (Deviation: `{m_res['freq_deviation_hz']:.4f} Hz` | Limit: `<= 0.50 Hz`)",
            f"* **Rate-of-Change-of-Frequency (RoCoF):** `{m_res['rocof_hz_s']:.2f} Hz/s` (Limit: `<= 1.50 Hz/s`)",
            f"* **PCC Islanding Breaker Trip State:** `{m_res['pcc_islanding_breaker_trip']}`",
            f"* **Hardware Register Map:** `{m_res['register_binding']}`",
            "",
            "---",
            "",
            "## 2. 480V 3-Phase Grain Silo Contactor & Plenum PLC Binding (`CLIN 0009` -- NEMA MG-1)",
            f"* **3-Phase RMS Voltage Average:** `{s_res['v_avg_volts']:.2f} V AC`",
            f"* **NEMA MG-1 Phase Voltage Unbalance:** `{s_res['nema_mg1_phase_unbalance_pct']:.4f}%` (Limit: `<= 2.00%`)",
            f"* **Contactor Interlock Safe:** `{s_res['contactor_interlock_safe']}` | **Command:** `{s_res['aeration_contactor_command']}`",
            f"* **PLC Coil & Register Map:** `{s_res['plc_register_binding']}`",
            "",
            "---",
            "",
            "## 3. SAE J1939 29-Bit Tactical CAN-Bus Decoder (`CLIN 0008` -- PGN 61444 EEC1)",
            f"* **29-Bit Extended CAN Identifier:** `{c_res['can_id_hex']}` (`Priority: {c_res['priority']}` | `PGN: {c_res['pgn']}` | `Source: {c_res['source_address']}`)",
            f"* **Decoded Engine Speed (SPN 190):** **`{c_res['decoded_engine_rpm']:.2f} RPM`**",
            f"* **CAN-Bus Physical & Scaling Binding:** `{c_res['j1939_bus_binding']}`",
            "",
            "---",
            f"**WORM WP-3 Interface Control Document Seal (SHA-256):** `{worm_seal}`",
        ]

        md_text = "\n".join(lines) + "\n"
        md_file = out_dir / "WP3_PLC_SCADA_J1939_INTERFACE_SPEC.md"
        pdf_file = out_dir / "WP3_PLC_SCADA_J1939_INTERFACE_SPEC.pdf"
        md_file.write_bytes(md_text.encode("ascii", errors="ignore"))
        pdf_bytes = build_minimal_iso_pdf(lines)
        pdf_file.write_bytes(pdf_bytes)

        return {
            "microgrid": m_res,
            "silo_plc": s_res,
            "j1939_can": c_res,
            "worm_seal": worm_seal,
            "md_path": str(md_file),
            "pdf_path": str(pdf_file),
            "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        }
