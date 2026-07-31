import pytest
from pathlib import Path
from diffuzz.analysis.signature import SignatureDB
from diffuzz.analysis.differ import Differ

RESPONSES = Path(__file__).parent.parent / "fixtures" / "responses"

@pytest.fixture
def sig_db():
    return SignatureDB.load_from_yaml("data/fingerprints.yaml")

@pytest.mark.parametrize("filename,expected_vuln", [
    ("sqli/mysql_error.html",    "sqli"),
    ("sqli/postgres_error.html", "sqli"),
    ("sqli/oracle_error.html",   "sqli"),
    ("sqli/mssql_error.html",    "sqli"),
    ("ssti/jinja2_eval.html",    "ssti"),
    ("lfi/passwd_leak.html",     "lfi"),
])
def test_signature_detects_vuln(sig_db, filename, expected_vuln):
    body = (RESPONSES / filename).read_text()
    match = sig_db.match(body)
    assert match is not None
    assert match.vuln_type == expected_vuln

@pytest.mark.parametrize("filename", [
    "normal/normal_200.html",
    "normal/normal_json.json",
    "waf/cloudflare_block.html",   # WAF block != finding
    "waf/generic_403.html",
])
def test_no_false_positive(sig_db, filename):
    body = (RESPONSES / filename).read_text()
    match = sig_db.match(body)
    assert match is None

# ── diff tests ────────────────────────────────────────────

@pytest.fixture
def baseline():
    return (RESPONSES / "normal/normal_200.html").read_text()

def test_differ_flags_large_body_change(baseline):
    vuln_body = (RESPONSES / "sqli/mysql_error.html").read_text()
    differ = Differ(baseline=baseline, baseline_time=0.3)
    result = differ.compare(body=vuln_body, elapsed=0.35)
    assert result.is_interesting
    assert "similarity" in result.reason.lower() or "body" in result.reason.lower()

def test_differ_flags_timing_spike(baseline):
    differ = Differ(baseline=baseline, baseline_time=0.3)
    result = differ.compare(body=baseline, elapsed=6.5)  # 5x threshold
    assert result.is_interesting
    assert "time" in result.reason.lower() or "timing" in result.reason.lower()

def test_differ_ignores_normal_variance(baseline):
    differ = Differ(baseline=baseline, baseline_time=0.3)
    slightly_different = baseline.replace("laptop", "phone")
    result = differ.compare(body=slightly_different, elapsed=0.31)
    assert not result.is_interesting