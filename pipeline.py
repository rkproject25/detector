import cv2
import time
import os
from detector import get_frame_embeddings, encode_reference_image
from matcher import match_against_database
from alert import trigger_alert

def load_reference_database(database_dir):
    ref_embeddings = {}
    if not os.path.exists(database_dir):
        return ref_embeddings
    for fname in os.listdir(database_dir):
        if fname.lower().endswith(('.jpg','.jpeg','.png')):
            name = os.path.splitext(fname)[0]
            try:
                emb = encode_reference_image(os.path.join(database_dir, fname))
                ref_embeddings[name] = emb
            except ValueError:
                print(f"Skipped {fname}")
    return ref_embeddings

def process_video(video_path, ref_embeddings, threshold=0.75, frame_skip=5, progress_callback=None):
    results = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return results
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_number += 1
        if progress_callback:
            progress_callback(frame_number, total_frames)
        if frame_number % frame_skip != 0:
            continue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        t0 = time.time()
        detections = get_frame_embeddings(frame_rgb)
        proc_time = (time.time() - t0) * 1000
        for box, emb in detections:
            matched_name, conf = match_against_database(ref_embeddings, emb, threshold)
            if matched_name:
                entry = trigger_alert(frame, box, matched_name, conf, frame_number)
                entry['processing_time_ms'] = round(proc_time, 2)
                entry['total_frames'] = total_frames
                entry['fps'] = cap.get(cv2.CAP_PROP_FPS)
                results.append(entry)
    cap.release()
    return results

def process_webcam(ref_embeddings, threshold=0.75):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return
    frame_num = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_num += 1
        if frame_num % 3 != 0:
            cv2.imshow("Sentinel Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = get_frame_embeddings(frame_rgb)
        disp = frame.copy()
        for box, emb in detections:
            matched_name, conf = match_against_database(ref_embeddings, emb, threshold)
            x1,y1,x2,y2 = [int(c) for c in box]
            if matched_name:
                color = (0,255,0)
                label = f"{matched_name} ({conf:.1%})"
                trigger_alert(frame, box, matched_name, conf, frame_num)
            else:
                color = (0,0,255)
                label = "Unknown"
            cv2.rectangle(disp, (x1,y1), (x2,y2), color, 2)
            cv2.putText(disp, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.imshow("Sentinel Webcam", disp)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
