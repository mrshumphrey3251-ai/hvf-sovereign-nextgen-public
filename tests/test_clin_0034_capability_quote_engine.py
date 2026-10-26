"""
Unit Test Suite for CLIN 0034 (WP-8): Automated Federal Capability Statement, 34-CLIN Quote Compiler, & Outreach Engine
"""
import pathlib, sys

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, SovereignPluginRegistry
from plugins.clin_0034_federal_capability_and_quote_engine import FederalCapabilityAndQuoteEngine


def run_clin_0034_tests() -> None:
    reg = SovereignPluginRegistry()
    eng = FederalCapabilityAndQuoteEngine()
    manifest = reg.register(eng)
    assert manifest.clin_number == "CLIN 0034"
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Verify 34-CLIN Catalog Math & Quote Builder
    assert eng.CORE_26_UNBUNDLED_ANNUAL_USD + eng.NEXTGEN_8_UNBUNDLED_ANNUAL_USD == 2175000
    q_small = eng.build_custom_quote(
        selected_clin_keys=["CLIN 0001 (Sovereign Command Base Entry Pilot - 1 Node)"],
        node_count=1,
    )
    assert q_small["total_annual_ffp_quote_usd"] == 24500.0
    assert q_small["day1_mobilization_invoice_usd"] == 24500.0

    q_large = eng.build_custom_quote(
        selected_clin_keys=["CLIN 1004-A (Turnkey 26-Module Single-Node TOC Enclave Bundle)"],
        node_count=1,
    )
    assert q_large["total_annual_ffp_quote_usd"] == 895000.0
    assert q_large["day1_mobilization_invoice_usd"] == 447500.0

    # 2. Verify Outreach Templates & Multi-Page WORM %PDF-1.4 Capability Statement Export
    artifacts_dir = here / "artifacts"
    exported = eng.generate_wp8_capability_and_quote_dossier(artifacts_dir)
    assert "1AHA8" in exported["outreach"]["linkedin_broadcast"]
    assert "S1M4ENLHTDH5" in exported["outreach"]["contracting_officer_email"]
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"**" not in pdf_bytes
    assert b"WORM WP-8 Capability Statement" in pdf_bytes
    assert b"%%EOF" in pdf_bytes


if __name__ == "__main__":
    run_clin_0034_tests()
    print("[100% PASS] CLIN 0034 (WP-8) Federal Capability Statement & 34-CLIN Quote Compiler Test Suite Passed!")
