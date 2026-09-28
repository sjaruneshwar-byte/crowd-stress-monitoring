from detector import classify_risk


def test_risk_thresholds():
    assert classify_risk(0) == "Low"
    assert classify_risk(5) == "Low"
    assert classify_risk(6) == "Moderate"
    assert classify_risk(15) == "Moderate"
    assert classify_risk(16) == "High"
