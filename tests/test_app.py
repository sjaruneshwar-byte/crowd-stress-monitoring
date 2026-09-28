import io
import app as app_module


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Crowd Monitoring" in response.data


def test_history_empty(client):
    response = client.get("/api/history")
    assert response.status_code == 200
    assert response.get_json() == []


def test_analyze_requires_video(client):
    response = client.post("/api/analyze", data={})
    assert response.status_code == 400


def test_rejects_unsupported_file(client):
    response = client.post(
        "/api/analyze",
        data={"video": (io.BytesIO(b"hello"), "notes.txt")},
        content_type="multipart/form-data"
    )
    assert response.status_code == 400


def test_analysis_saved(client, monkeypatch):
    fake_result = {
        "frames_sampled": 2,
        "average_people_count": 3.5,
        "peak_people_count": 5,
        "risk_level": "Low",
        "timeline": [
            {"time_seconds": 0.0, "people_count": 2, "risk_level": "Low"},
            {"time_seconds": 1.0, "people_count": 5, "risk_level": "Low"}
        ],
        "duration_seconds": 1.0,
        "notice": "Test result"
    }
    monkeypatch.setattr(app_module, "analyze_video", lambda _path: fake_result)
    response = client.post(
        "/api/analyze",
        data={"video": (io.BytesIO(b"fake video bytes"), "sample.mp4")},
        content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert response.get_json()["id"] == 1
    history = client.get("/api/history").get_json()
    assert len(history) == 1
    assert history[0]["filename"] == "sample.mp4"
