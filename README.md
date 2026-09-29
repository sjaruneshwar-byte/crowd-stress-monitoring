# Crowd Stress Monitoring System

A Software Engineering project prototype for video-based crowd monitoring. The application uses OpenCV's built-in HOG pedestrian detector to estimate people counts in sampled video frames, assigns an illustrative congestion-risk level, displays a timeline dashboard, and stores analysis history in SQLite.

> **Scope and safety:** This prototype estimates visible people counts as a congestion-related indicator. It does not directly measure psychological stress, infer emotions, identify people, or provide certified crowd-safety advice. Demo thresholds are illustrative and are not validated safety limits.

## Dashboard Features

The dashboard allows users to upload crowd videos and view
crowd count, risk level, analysis duration, and analysis history.
## Features

- Upload MP4, AVI, MOV, or MKV video (up to 100 MB size)
- Sample video frames and detect pedestrians with OpenCV HOG.
- Show average and peak detected people per sampled frame.
- Assign Low, Moderate, or High congestion-risk labels using configurable demo thresholds.
- Display a timeline chart and recent analysis history.
- Save records in a local SQLite database.
- Run automated tests with pytest.

## Requirements

- Python 3.10 or newer
- Git
- Internet connection for installing Python dependencies (the app itself does not require external APIs)

## Setup

### Windows (PowerShell)

```powershell
git clone https://github.com/USERNAME/crowd-stress-monitoring.git
cd crowd-stress-monitoring
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` instead of activating the environment.

### macOS / Linux

```bash
git clone https://github.com/USERNAME/crowd-stress-monitoring.git
cd crowd-stress-monitoring
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## How to use

1. Start the Flask server.
2. Open the dashboard in your browser.
3. Choose a short crowd video in a supported format.
4. Select **Analyse video** and wait for processing to finish.
5. Review the average count, peak count, congestion-risk label, timeline, and history.

Use a video that you have permission to process. Prefer public, consented, or staged footage. The app stores the filename and aggregate analysis values, not the uploaded video. A temporary copy is deleted after analysis.

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Dashboard page |
| GET | `/api/history` | Latest 20 analysis records |
| POST | `/api/analyze` | Upload a video as multipart field `video` and analyse it |

Example response from `/api/analyze`:

```json
{
  "id": 1,
  "filename": "sample.mp4",
  "frames_sampled": 12,
  "average_people_count": 4.25,
  "peak_people_count": 9,
  "risk_level": "Moderate",
  "duration_seconds": 11.4,
  "timeline": [
    {"time_seconds": 0.0, "people_count": 3, "risk_level": "Low"}
  ],
  "notice": "Congestion-risk proxy..."
}
```

## Detection method

OpenCV's pre-trained HOG + SVM people detector is applied to sampled frames. The initial prototype samples every 10th frame and limits wide frames to 960 pixels. Counts are approximate: people may be missed or duplicated due to occlusion, camera perspective, lighting, movement, and scene density.

The demonstration thresholds in `detector.py` are:
- Low: 0–5 detected people in a sampled frame
- Moderate: 6–15
- High: 16 or more

These thresholds are only for demonstrating software flow. They are not people-per-square-metre measurements, validated crowd-risk thresholds, or a substitute for human assessment. Camera calibration and a defined monitored area would be required for meaningful physical density estimates.

## Run tests

```bash
pytest -q
```

## Suggested team division

- **Member 1 — Frontend:** `templates/`, `static/`; dashboard, upload experience, chart, responsive styling.
- **Member 2 — Detection and backend:** `detector.py`, analysis endpoint in `app.py`; detector logic, input validation, API behavior and model/detection evaluation.
- **Member 3 — Database, integration and QA:** `database.py`, `tests/`, `docs/`; persistence, integration testing, architecture, setup guide and GitHub workflow coordination.

All members should contribute code, commits, pull requests, reviews, and viva preparation.

## GitHub workflow assignment checklist

- Create a GitHub repository and clone it with `git clone`.
- Use `git status`, `git add`, `git commit`, and `git push`.
- Modify a file and inspect it with `git diff`, then commit and push.
- Edit a README line directly on GitHub, then run `git pull`.
- Inspect history with `git log --oneline --graph --all`.
- Create feature branches with `git switch -c`, commit and push them.
- Open pull requests and merge feature branches into `main`.
- Create an Issue, implement its improvement on a branch, and close it through a pull request using `Closes #<issue-number>`.
- Have two contributors change the same README line on branches created from the same starting commit. Merge one, then merge the other to generate a genuine conflict. Resolve manually, commit and push.

Capture screenshots of the repository, commits, branches, Issue, pull request/merge, conflict markers, resolution, and final Git graph.

## Future improvements

- Evaluate a modern person detector against a labelled dataset.
- Add camera calibration and region-of-interest configuration.
- Add optional live-camera input with explicit authorization and privacy safeguards.
- Add user authentication and role-based access if required.
- Add exportable reports and configurable monitoring thresholds.
- Validate any risk interpretation with domain experts before real-world use.

## Dashboard

The project provides a dashboard for monitoring crowd conditions.

## Team Members

This project is developed as a Software Engineering collaborative project.
