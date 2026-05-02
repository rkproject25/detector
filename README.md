"# detector" 
Lost Person Detection System

An AI-powered system that detects missing persons from video footage or live webcam feeds using deep learning face recognition.

---

Project Overview

This system was built to solve a real problem — finding missing persons in surveillance footage without manually scanning hours of video. You upload a photo of the missing person and a video, and the system automatically scans every frame, detects all faces, and alerts you the moment it finds a match.

It works on a standard laptop with no GPU required.

---

What it does

- Scans video footage frame by frame for a missing person's face
- Matches detected faces against a reference photo using cosine similarity
- Saves an annotated snapshot the moment a match is found
- Estimates the detected person's age and gender
- Sends an email alert with the snapshot attached
- Supports live webcam detection in real time
- Evaluates itself — precision, recall, F1, FAR, FRR

---

How it works

You upload a clear photo of the missing person. The system encodes that face into a 512-number vector using FaceNet. Then it reads the video frame by frame, detects every face using MTCNN, encodes each one the same way, and compares them using cosine similarity. If the similarity crosses your chosen threshold, it flags it as a match.

The whole pipeline runs locally on CPU. No internet needed during detection.

---

Project structure

app.py              — the web interface, three tabs
detector.py         — face detection and embedding
matcher.py          — cosine similarity comparison
alert.py            — saves snapshots and logs detections
pipeline.py         — connects everything, runs the main loop
evaluator.py        — computes accuracy metrics
age_gender.py       — estimates age and gender on matched faces
email_alert.py      — sends Gmail alert with snapshot attached

database/missing_persons/    — put reference photos here
test_videos/                 — put videos to search here
output/matched_frames/       — annotated snapshots saved here
output/detections_log.json   — full history of all detections

---

Tech used

Python 3.10
MTCNN for face detection
FaceNet (InceptionResnetV1, VGGFace2 weights) for face embeddings
Cosine similarity via scikit-learn for matching
DeepFace for age and gender estimation
OpenCV for video processing and frame annotation
Streamlit for the web interface
Plotly for confidence score charts
Gmail SMTP for email alerts
Runs entirely on CPU

---

Installation

Step 1 — create a virtual environment

    python -m venv venv
    venv\Scripts\activate

Step 2 — install dependencies

    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    pip install facenet-pytorch opencv-python pillow numpy scikit-learn streamlit plotly pandas deepface tf-keras

Step 3 — run the app

    streamlit run app.py

Open your browser at http://localhost:8501

On first run, FaceNet downloads its pretrained weights (around 107MB). This only happens once.

---

Using the app

Video detection tab

Upload a photo of the missing person — ideally a clear, front-facing shot. Upload the video you want to search. Adjust the confidence threshold (0.75 is a good starting point) and how many frames to skip. Hit Start Detection.

The system shows a confidence chart across frames, saves annotated snapshots for every match, and gives you a full detection log you can export as CSV or JSON.

Webcam tab

Upload a reference photo, click Start Webcam, and an OpenCV window opens on your desktop. Green box means a match was found. Red box means an unknown face. Age and gender are shown below the box. Matched snapshots are saved automatically.

Evaluation tab

Upload pairs of photos — same-person pairs and different-person pairs. The system runs through all of them and reports precision, recall, F1 score, false accept rate, false reject rate, and average processing time. You can export the full report as JSON.

---

Email alerts

Open email_alert.py and fill in three fields:

    SENDER_EMAIL    = "yourgmail@gmail.com"
    SENDER_PASSWORD = "your app password here"
    RECEIVER_EMAIL  = "yourgmail@gmail.com"

The password here is a Gmail App Password, not your regular login password. To get one: Google Account, then Security, then 2-Step Verification, then App Passwords. Generate one for Mail and paste it in.

Once configured, the system sends an email the moment a match is found — with the person's name, confidence score, frame number, estimated age and gender, and the annotated snapshot attached.

---

Settings you can tune

Confidence threshold — default 0.75. Lower it if you are missing detections. Raise it if you are getting too many false matches. Range is 0.50 to 0.95.

Frame skip — default every 5th frame. Set to 3 for more thorough scanning, 10 or 15 for faster processing on long videos.

Min face size — set to 40 pixels in detector.py. Lower this if faces in your video are small or far from the camera.

---

Output files

Every detection saves three things. An annotated JPEG in output/matched_frames/ showing the bounding box, name, confidence, age, gender, and timestamp. An entry in output/detections_log.json with all the same information. And an email if your credentials are configured.

---

Known limitations

Webcam mode opens a window on your local machine. It cannot work on a cloud server since there is no physical camera attached.

Processing speed on CPU is roughly 200 to 400 milliseconds per frame depending on your machine. Videos are processed faster by skipping frames.

Accuracy drops in poor lighting, with partial occlusion, or at extreme face angles.

The system detects one face at a time per bounding box. If two people are very close together in the frame, detections may overlap.

---

Possible extensions

GPU support for real-time processing on longer videos
Simultaneous processing of multiple camera feeds
Re-identification across different cameras
Face age progression for long-missing persons
Mobile interface
Integration with external alert systems

---

References

FaceNet paper — arxiv.org/abs/1503.03832
MTCNN paper — arxiv.org/abs/1604.02878
DeepFace library — github.com/serengil/deepface
facenet-pytorch — github.com/timesler/facenet-pytorch



streamlit>=1.28.0
torch torchvision --index-url https://download.pytorch.org/whl/cpu
facenet-pytorch>=2.5.3
opencv-python>=4.8.0
numpy>=1.24.0
scikit-learn>=1.3.0
Pillow>=9.5.0
plotly>=5.14.0
pandas>=2.0.0
deepface>=0.0.79
tf-keras>=2.15.0
