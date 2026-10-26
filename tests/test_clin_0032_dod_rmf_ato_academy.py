"""
Unit Test Suite for CLIN 0032 (WP-6): DoD RMF / eMASS ATO STIG Synthesizer & 50-Seat Field Academy Cohort Provisioner
"""
import pathlib, sys

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, SovereignPluginRegistry
from plugins.clin_0032_dod_rmf_ato_academy_cohort_engine import DoDRMFATOAndAcademyCohortEngine


def run_clin_0032_tests() -> None:
    reg = SovereignPluginRegistry()
    eng = DoDRMFATOAndAcademyCohortEngine()
    manifest = reg.register(eng)
    assert manifest.clin_number == "CLIN 0032"
    assert manifest.target_trl == "TRL 9"
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Verify DoD RMF / NIST 800-53 Rev 5 Zero-Finding ATO Matrix
    ato = eng.evaluate_dod_rmf_ato_controls()
    assert ato["cat_i_open_findings"] == 0
    assert ato["cat_ii_open_findings"] == 0
    assert ato["cat_iii_open_findings"] == 0
    assert ato["controls_satisfied"] == ato["controls_evaluated"] == 6
    assert ato["ato_authorization_decision"] == "ATO_GRANTED_TRL_9_FULL_OPERATIONAL_CAPABILITY"

    # 2. Verify 50-Seat Field Academy Cohort & 1,420 Verified Questions
    cohort = eng.provision_50_seat_academy_cohort(seat_count=50)
    assert cohort["provisioned_seat_count"] == 50
    assert cohort["total_verified_questions"] == 1420
    assert cohort["all_seat_tokens_unique"] is True

    # 3. Export WORM %PDF-1.4 ICD Artifact
    artifacts_dir = here / "artifacts"
    exported = eng.generate_wp6_ato_academy_dossier(artifacts_dir)
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes


if __name__ == "__main__":
    run_clin_0032_tests()
    print("[100% PASS] CLIN 0032 (WP-6) DoD RMF ATO & 50-Seat Field Academy Test Suite Passed!")
