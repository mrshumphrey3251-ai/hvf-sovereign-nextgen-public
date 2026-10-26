"""
Unit Test Suite for CLIN 0031 (WP-5): Command Watch-Floor RBAC, Callsign Provisioner, & Shift-Ledger PDF Compiler
"""
import pathlib, sys

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, SovereignPluginRegistry
from plugins.clin_0031_command_watchfloor_rbac_pdf_engine import CommandWatchFloorRBACAndPDFEngine


def run_clin_0031_tests() -> None:
    reg = SovereignPluginRegistry()
    eng = CommandWatchFloorRBACAndPDFEngine()
    manifest = reg.register(eng)
    assert manifest.clin_number == "CLIN 0031"
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Verify Bitwise RBAC Enforcement Across Watch-Floor Seats
    assert eng.verify_seat_permission("LEVEL_1_TELEMETRY_OBSERVER", eng.PERM_READ_TELEMETRY)["authorized"] is True
    assert eng.verify_seat_permission("LEVEL_1_TELEMETRY_OBSERVER", eng.PERM_CONTACTOR_OVERRIDE)["authorized"] is False
    assert eng.verify_seat_permission("LEVEL_3_WATCH_OFFICER", eng.PERM_SIGN_SHIFT_BRIEF)["authorized"] is True
    assert eng.verify_seat_permission("LEVEL_3_WATCH_OFFICER", eng.PERM_AIRLOCK_RELEASE)["authorized"] is False
    assert eng.verify_seat_permission("LEVEL_5_SOVEREIGN_COMMANDER", eng.PERM_AIRLOCK_RELEASE)["authorized"] is True

    # 2. Verify Shift-Handover Hash Chain & WORM %PDF-1.4 Compilation
    artifacts_dir = here / "artifacts"
    exported = eng.generate_wp5_watchfloor_dossier(artifacts_dir)
    assert len(exported["shift_ledger"]["current_shift_worm_hash"]) == 64
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes


if __name__ == "__main__":
    run_clin_0031_tests()
    print("[100% PASS] CLIN 0031 (WP-5) Command Watch-Floor RBAC & Shift-Ledger PDF Test Suite Passed!")
