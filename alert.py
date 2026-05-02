import cv2
import os
import json
from datetime import datetime
from age_gender import estimate_age_gender
from email_alert import send_alert

OUTPUT_DIR = "output/matched_frames/"
LOG_FILE = "output/detections_log.json"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def trigger_alert(frame, box, name, confidence, frame_number):
    x1, y1, x2, y2 = [int(c) for c in box]
    face_roi = frame[y1:y2, x1:x2]
    age, gender = estimate_age_gender(face_roi)  # returns None, None (safe)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    snapshot_path = os.path.join(OUTPUT_DIR, f"match_{name}_{timestamp}.jpg")

    annotated = frame.copy()
    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0,255,0), 2)
    label = f"{name} ({confidence:.1%})"
    cv2.putText(annotated, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    if age and gender:
        cv2.putText(annotated, f"Age: {age}, Gender: {gender}", (x1, y2+20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
    cv2.imwrite(snapshot_path, annotated)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "person_name": name,
        "confidence": confidence,
        "frame_number": frame_number,
        "snapshot_path": snapshot_path,
        "age": age,
        "gender": gender,
        "bounding_box": [int(x) for x in box]
    }
    # Append to log
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    else:
        logs = []
    logs.append(entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

    send_alert(name, confidence, frame_number, snapshot_path, age, gender)
    return entry