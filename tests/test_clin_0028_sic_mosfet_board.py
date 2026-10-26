"""
Unit Test Suite for CLIN 0028 (WP-2): 36.75ns SiC MOSFET Hardware Interlock Board & BOM Engine
"""
import pathlib, sys

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, SovereignPluginRegistry
from plugins.clin_0028_sic_mosfet_interlock_board import SiCMOSFETGuillotineBoardEngine


def run_clin_0028_tests() -> None:
    reg = SovereignPluginRegistry()
    eng = SiCMOSFETGuillotineBoardEngine()
    manifest = reg.register(eng)
    assert manifest.clin_number == "CLIN 0028"
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    spec = eng.simulate_bench_calibration(
        actuator_velocity_mm_s=1500.0,
        dc_bus_voltage_v=480.0,
        peak_fault_current_a=85.0,
        bus_inductance_uh=12.0,
    )
    assert spec["total_propagation_delay_ns"] == 36.75
    assert abs(spec["hvf_stopping_distance_um"] - 0.055125) < 1e-6
    assert spec["legacy_150ms_plc_stopping_distance_mm"] == 225.0
    assert spec["thermal_safety_margin_pass"] is True

    artifacts_dir = here / "artifacts"
    exported = eng.export_board_spec_markdown_and_pdf(spec, artifacts_dir)
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes


if __name__ == "__main__":
    run_clin_0028_tests()
    print("[100% PASS] CLIN 0028 (WP-2) 36.75ns SiC MOSFET Board Test Suite Passed!")
