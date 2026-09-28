"""Baseline pedestrian detection and congestion-risk proxy using OpenCV HOG.

This prototype does not infer emotions or diagnose psychological stress.
Counts are approximate and depend on camera angle, occlusion, lighting,
video quality and the detector's limitations.
"""
import cv2


def classify_risk(people_count):
    """Classify a frame using simple demo thresholds (not safety standards)."""
    if people_count <= 5:
        return "Low"
    if people_count <= 15:
        return "Moderate"
    return "High"


def analyze_video(video_path, sample_every_n_frames=10):
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise ValueError("The uploaded file could not be opened as a video.")

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    fps = capture.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 25.0

    sampled_counts = []
    frame_index = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break

            if frame_index % sample_every_n_frames == 0:
                height, width = frame.shape[:2]
                # Resize large frames to reduce processing time while retaining
                # a consistent detector input size.
                max_width = 960
                if width > max_width:
                    scale = max_width / width
                    frame = cv2.resize(frame, (max_width, int(height * scale)))

                boxes, _weights = hog.detectMultiScale(
                    frame,
                    winStride=(8, 8),
                    padding=(8, 8),
                    scale=1.05
                )
                count = len(boxes)
                sampled_counts.append({
                    "time_seconds": round(frame_index / fps, 2),
                    "people_count": int(count),
                    "risk_level": classify_risk(count)
                })
            frame_index += 1
    finally:
        capture.release()

    if not sampled_counts:
        raise ValueError("No readable frames were found in the video.")

    counts = [point["people_count"] for point in sampled_counts]
    average_count = round(sum(counts) / len(counts), 2)
    peak_count = max(counts)

    return {
        "frames_sampled": len(sampled_counts),
        "average_people_count": average_count,
        "peak_people_count": peak_count,
        "risk_level": classify_risk(peak_count),
        "timeline": sampled_counts,
        "duration_seconds": round(frame_index / fps, 2),
        "notice": (
            "Congestion-risk proxy based on approximate detected people per sampled frame. "
            "Not a measurement of psychological stress and not a certified safety assessment."
        )
    }
