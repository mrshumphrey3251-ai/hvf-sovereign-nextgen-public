"""
Unit Test Suite for Stage 13j: Port 8502 Next-Gen Command Dashboard (nextgen_cockpit_preview.py)
"""
import pathlib, py_compile, sys

sys.dont_write_bytecode = True
here = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here))

from nextgen_cockpit_preview import build_registry_and_engines


def run_nextgen_cockpit_ui_tests() -> None:
    cockpit_file = here / "nextgen_cockpit_preview.py"
    assert cockpit_file.exists()
    py_compile.compile(str(cockpit_file), doraise=True)
    raw_txt = cockpit_file.read_text(encoding="utf-8")
    assert "??" not in raw_txt, "Zero encoding-artifact check failed"
    assert " ? " not in raw_txt, "Zero mangled em-dash check failed"

    reg, e27, e28, e29, e30, e31, e32, e33 = build_registry_and_engines()
    manifests = reg.list_manifests()
    assert len(manifests) == 7
    assert [m["clin_number"] for m in manifests] == [
        "CLIN 0027",
        "CLIN 0028",
        "CLIN 0029",
        "CLIN 0030",
        "CLIN 0031",
        "CLIN 0032",
        "CLIN 0033",
    ]


if __name__ == "__main__":
    run_nextgen_cockpit_ui_tests()
    print("[100% PASS] Next-Gen Cockpit Preview UI (Port 8502) Unit Test Suite Passed!")
