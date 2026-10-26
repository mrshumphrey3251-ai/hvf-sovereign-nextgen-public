"""
Unit Test Suite for CLIN 0030 (WP-4): UAS Optical GLI Feed & Oklahoma Title 61 GIS Boundary Engine
"""
import pathlib, sys

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_core.sovereign_plugin_contract import FROZEN_EBONY_MERKLE_ROOT, SovereignPluginRegistry
from plugins.clin_0030_uas_optical_gli_title61_gis import UASOpticalGLIAndTitle61GISEngine


def run_clin_0030_tests() -> None:
    reg = SovereignPluginRegistry()
    eng = UASOpticalGLIAndTitle61GISEngine()
    manifest = reg.register(eng)
    assert manifest.clin_number == "CLIN 0030"
    assert manifest.compatible_host_merkle_root == FROZEN_EBONY_MERKLE_ROOT

    # 1. Test Healthy Canopy vs Bare Soil Erosion GLI
    healthy = eng.evaluate_uas_optical_gli(red_8bit=62, green_8bit=178, blue_8bit=48)
    assert healthy["green_leaf_index_gli"] > 0.45
    assert healthy["canopy_classification"] == "HEALTHY_VEGETATIVE_CANOPY_OR_ROW_GROWTH"

    erosion = eng.evaluate_uas_optical_gli(red_8bit=190, green_8bit=110, blue_8bit=95)
    assert erosion["green_leaf_index_gli"] < 0.0
    assert erosion["canopy_classification"] == "BARE_SOIL_EROSION_OR_HARDPAN_ALERT"

    # 2. Test 10.00-Acre UTM Polygon & Oklahoma Title 61 5% Retainage
    gis_res = eng.evaluate_title61_gis_parcel_and_retainage(estimated_civil_work_usd=420000.00)
    assert abs(gis_res["parcel_area_acres"] - 10.0000) < 1e-4
    assert gis_res["ok_title61_statutory_retainage_5pct_usd"] == 21000.00
    assert gis_res["net_progress_disbursement_95pct_usd"] == 399000.00
    assert gis_res["statutory_performance_bond_100pct_usd"] == 420000.00

    # 3. Export WORM %PDF-1.4 ICD Artifact
    artifacts_dir = here / "artifacts"
    exported = eng.generate_wp4_uas_gis_dossier(artifacts_dir)
    pdf_bytes = pathlib.Path(exported["pdf_path"]).read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes


if __name__ == "__main__":
    run_clin_0030_tests()
    print("[100% PASS] CLIN 0030 (WP-4) UAS Optical GLI & Oklahoma Title 61 GIS Test Suite Passed!")
