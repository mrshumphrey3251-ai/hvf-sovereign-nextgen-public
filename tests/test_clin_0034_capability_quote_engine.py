"""
Unit Test Suite for WP-9 (CLIN 0035 v8.0):
Automated Federal Capability Statement, 35-CLIN ($2,230,000/yr) Custom Quote & Outreach Engine.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.clin_0034_federal_capability_and_quote_engine import FederalCapabilityAndQuoteEngine


def run_clin_0034_tests() -> None:
    eng = FederalCapabilityAndQuoteEngine()
            
    q1 = eng.build_custom_quote(node_count=1)
    assert q1["single_node_annual_usd"] == 2230000
    assert q1["grand_total_annual_usd"] == 2230000
    assert q1["day1_wawf_invoice_usd"] == 1115000

    artifacts_dir = ROOT / "artifacts"
    pkt = eng.generate_wp8_capability_and_quote_packet(artifacts_dir, node_count=1)
    pdf_bytes = pathlib.Path(pkt["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"CLIN 0035" in pdf_bytes
    print("[100% PASS] CLIN 0035 (WP-9 v8.0) Federal Capability Statement & 35-CLIN ($2,230,000/yr) Quote Engine Passed!")


if __name__ == "__main__":
    run_clin_0034_tests()
