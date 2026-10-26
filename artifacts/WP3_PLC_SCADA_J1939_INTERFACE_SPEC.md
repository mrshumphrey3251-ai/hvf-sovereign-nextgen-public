# HUMPHREY VIRTUAL FARMS LLC // WP-3: SITE PLC, 60HZ SCADA, & SAE J1939 CAN-BUS ICD
**Entity:** Humphrey Virtual Farms LLC (`CAGE: 1AHA8` | `SAM.gov UEI: S1M4ENLHTDH5`)
**Controlling Authority:** Jeffery Humphrey, Founder, CEO, & Principal Sovereign Architect
**Plug-In Module:** `CLIN 0029 (WP-3 Site Interface Adapter)` | **Enclave Tier:** `PUBLIC`
**Host Ebony Baseline Merkle Root:** `cc1ee1c8d29b2ae5e856fc0fcb672a52e7e49d50369499febe14e18e9150949a`

---

## 1. 60Hz Microgrid Substation Relay Binding (`CLIN 0003` -- IEEE C37.118 / Modbus / DNP3)
* **Measured Bus Frequency:** `59.985 Hz` (Deviation: `0.0150 Hz` | Limit: `<= 0.50 Hz`)
* **Rate-of-Change-of-Frequency (RoCoF):** `-0.12 Hz/s` (Limit: `<= 1.50 Hz/s`)
* **PCC Islanding Breaker Trip State:** `False`
* **Hardware Register Map:** `[REDACTED_MODBUS_DNP3_REGISTER_MAP_DFARS_252_227_7018]`

---

## 2. 480V 3-Phase Grain Silo Contactor & Plenum PLC Binding (`CLIN 0009` -- NEMA MG-1)
* **3-Phase RMS Voltage Average:** `480.00 V AC`
* **NEMA MG-1 Phase Voltage Unbalance:** `0.2500%` (Limit: `<= 2.00%`)
* **Contactor Interlock Safe:** `True` | **Command:** `ENERGIZE_480V_CONTACTOR`
* **PLC Coil & Register Map:** `[REDACTED_480V_PLC_COIL_MAP_DFARS_252_227_7018]`

---

## 3. SAE J1939 29-Bit Tactical CAN-Bus Decoder (`CLIN 0008` -- PGN 61444 EEC1)
* **29-Bit Extended CAN Identifier:** `0x0CF00400` (`Priority: 3` | `PGN: 61444` | `Source: 0`)
* **Decoded Engine Speed (SPN 190):** **`1800.00 RPM`**
* **CAN-Bus Physical & Scaling Binding:** `[REDACTED_J1939_SPN_SCALING_DFARS_252_227_7018]`

---
**WORM WP-3 Interface Control Document Seal (SHA-256):** `3a7f92d1f670ff1dbdc9e4259d1b60e0fa14c54e46c1ed37ad484fbcb042a343`
