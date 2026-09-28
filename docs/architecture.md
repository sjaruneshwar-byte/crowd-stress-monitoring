# System Architecture

```text
User
 |
 v
Browser Dashboard (HTML / CSS / JavaScript)
 |  POST /api/analyze (video upload)
 |  GET  /api/history
 v
Flask Application (app.py)
 |
 +----> Video Detector (detector.py)
 |         OpenCV HOG + SVM
 |         sampled frames -> approximate counts -> demo risk labels
 |
 +----> Persistence Layer (database.py)
           SQLite
           filename, timestamp, average/peak count, risk label, timeline
 |
 v
JSON response -> Dashboard metrics, timeline chart, history table
```

## Data flow
1. User chooses a supported video.
2. Browser sends it as multipart form data to Flask.
3. Flask validates the extension and saves a temporary copy.
4. OpenCV reads sampled frames and estimates pedestrian counts.
5. The detector computes average and peak counts and applies illustrative thresholds.
6. The database stores aggregate results and timeline values.
7. Flask returns JSON to the browser and deletes the temporary video.
8. The dashboard displays the result and reloads recent history.

## Limitations
This is a software prototype. A pedestrian detector's frame-level count is not calibrated physical density, crowd stress, or an emergency prediction. It requires proper validation before any operational use.
