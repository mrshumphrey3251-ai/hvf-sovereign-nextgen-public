"""
Unit Test Suite for CLIN 0029 (WP-3): Site PLC, 60Hz SCADA, & SAE J1939 CAN-Bus Register Mapper
"""
import pathlib, sys

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, SovereignPluginRegistry
from plugins.clin_0029_site_plc_scada_canbus_mapper import SitePLCSCADACANBusMapper


def run_clin_0029_tests() -> None:
    reg = SovereignPluginRegistry()
    mapper = SitePLCSCADACANBusMapper()
    manifest = reg.register(mapper)
    assert manifest.clin_number == "CLIN 0029"
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Test 60Hz Microgrid Nominal vs Fault Islanding
    nominal_grid = mapper.evaluate_microgrid_60hz_relay(freq_hz=59.985, rocof_hz_s=-0.12)
    assert nominal_grid["pcc_islanding_breaker_trip"] is False
    fault_grid = mapper.evaluate_microgrid_60hz_relay(freq_hz=59.100, rocof_hz_s=-2.40)
    assert fault_grid["pcc_islanding_breaker_trip"] is True

    # 2. Test 480V 3-Phase Silo Contactor Phase Balance
    silo_ok = mapper.evaluate_480v_silo_contactor_plc(481.2, 479.8, 479.0, grain_moisture_pct=14.2)
    assert silo_ok["contactor_interlock_safe"] is True
    assert silo_ok["aeration_contactor_command"] == "ENERGIZE_480V_CONTACTOR"
    silo_fault = mapper.evaluate_480v_silo_contactor_plc(480.0, 480.0, 430.0, grain_moisture_pct=14.2)
    assert silo_fault["contactor_interlock_safe"] is False
    assert silo_fault["aeration_contactor_command"] == "STANDBY_LOCKOUT"

    # 3. Test SAE J1939 29-Bit Extended CAN Frame Decoder (0x0CF00400 -> PGN 61444, 1800.0 RPM)
    can_decoded = mapper.decode_sae_j1939_can_frame(0x0CF00400)
    assert can_decoded["pgn"] == 61444
    assert can_decoded["priority"] == 3
    assert can_decoded["decoded_engine_rpm"] == 1800.0

    # 4. Export WORM %PDF-1.4 ICD Artifact
    artifacts_dir = here / "artifacts"
    exported = mapper.generate_wp3_interface_dossier(artifacts_dir)
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes


if __name__ == "__main__":
    run_clin_0029_tests()
    print("[100% PASS] CLIN 0029 (WP-3) PLC, 60Hz SCADA, & SAE J1939 CAN-Bus Test Suite Passed!")
