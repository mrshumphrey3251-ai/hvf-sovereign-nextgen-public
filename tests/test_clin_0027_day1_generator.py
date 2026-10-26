"""
Unit Test Suite for CLIN 0027: Automated Day-1 Cryptographic Hardware-UUID License Key & WAWF Invoice Generator
"""
import pathlib, sys, tempfile

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, SovereignPluginRegistry
from plugins.clin_0027_day1_license_wawf_generator import Day1LicenseAndWAWFInvoiceGenerator


def run_clin_0027_tests() -> None:
    reg = SovereignPluginRegistry()
    gen = Day1LicenseAndWAWFInvoiceGenerator()
    manifest = reg.register(gen)
    assert manifest.clin_number == "CLIN 0027"
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # Test Case 1: Simplified Acquisition Award (<= $250,000) -> 100% Day-1 Invoicing
    pkt_small = gen.generate_day1_packet(
        contract_number="W912BV-26-P-0001",
        awarding_agency="DoD CDAO Tradewinds / USACE Tulsa District",
        hardware_node_uuid="HVF-NODE-OK-TINKER-0001",
        licensed_clins=["CLIN 0001", "CLIN 0006"],
        total_contract_award_usd=209500.00,
    )
    assert pkt_small["day1_immediate_invoice_usd"] == 209500.00
    assert pkt_small["wawf_billing_code"] == "COTS-100PCT-DAY1"
    assert round(sum(pkt_small["day1_five_bucket_allocation_usd"].values()), 2) == 209500.00

    # Test Case 2: Enterprise Console Award (> $250,000) -> 50% Day-1 OTA Milestone #01
    pkt_large = gen.generate_day1_packet(
        contract_number="FA8100-26-9-3952",
        awarding_agency="DoD CDAO / Tinker AFB OC-ALC Depot",
        hardware_node_uuid="HVF-NODE-OK-OCALC-3001",
        licensed_clins=["CLIN 1004-A"],
        total_contract_award_usd=895000.00,
    )
    assert pkt_large["day1_immediate_invoice_usd"] == 447500.00
    assert pkt_large["wawf_billing_code"] == "OTA-MILESTONE-01-50PCT"
    assert round(sum(pkt_large["day1_five_bucket_allocation_usd"].values()), 2) == 447500.00

    # Test Case 3: Export WORM-Sealed %PDF-1.4 & Markdown Day-1 Packet
    artifacts_dir = here / "artifacts"
    exported = gen.export_day1_markdown_and_pdf(pkt_large, artifacts_dir)
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes


if __name__ == "__main__":
    run_clin_0027_tests()
    print("[100% PASS] CLIN 0027 Unit Test Suite Passed (100% Day-1 COTS, 50% OTA Milestone #01, & %PDF-1.4 Verified)!")
