import streamlit as st
import sqlite3
import hashlib
import os
import tempfile
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

# Import your existing modules
from detector import encode_reference_image
from pipeline import process_video, process_webcam
from evaluator import evaluate_on_image_pairs

# ─────────────────────────────────────────────────────────────────────────────
# Database (SQLite)
# ─────────────────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, email="", full_name=""):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password_hash, email, full_name) VALUES (?,?,?,?)',
                  (username, hash_password(password), email, full_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == hash_password(password)

def get_user_info(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, email, full_name, created_at FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"username": row[0], "email": row[1], "full_name": row[2], "created_at": row[3]}
    return None

def update_user_profile(username, email, full_name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET email = ?, full_name = ? WHERE username = ?', (email, full_name, username))
    conn.commit()
    conn.close()

def update_password(username, new_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET password_hash = ? WHERE username = ?', (hash_password(new_password), username))
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────────────────────────────────────
# Page config & CSS
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Sentinel - Lost Person Detection", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0f1a; }
    .stButton>button {
        background-color: #2c7da0;
        color: white;
        border-radius: 8px;
        font-weight: 500;
    }
    .stButton>button:hover { background-color: #1f5e7a; }
    h1, h2, h3 { color: #eaeef2; }
    .alert-box {
        background: #1e3a2f;
        border-left: 5px solid #2ecc71;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #3b2e1e;
        border-left: 5px solid #f39c12;
        padding: 0.8rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = "home"

# ─────────────────────────────────────────────────────────────────────────────
# Public pages (Home, Login, Register, About, Contact)
# ─────────────────────────────────────────────────────────────────────────────
def show_home():
    st.title("🔍 Sentinel - Lost Person Detection System")
    st.markdown("**AI‑powered face recognition for finding missing persons**")
    st.image("https://img.icons8.com/fluency/200/search.png", width=150)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🎥 **Video Detection** – Search hours of footage")
    with col2:
        st.markdown("📷 **Live Webcam** – Real‑time matching")
    with col3:
        st.markdown("📊 **System Evaluation** – Precision, recall, FAR, FRR")
    if st.button("Get Started →", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()

def show_login():
    st.title("🔐 Login")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        st.markdown("---")
        if st.button("Create new account", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
        if st.button("← Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

def show_register():
    st.title("📝 Register")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            full_name = st.text_input("Full Name")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if not username or not password:
                    st.warning("Username and password required")
                elif password != confirm:
                    st.warning("Passwords do not match")
                else:
                    if add_user(username, password, email, full_name):
                        st.success("Account created! Please login.")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("Username already exists")
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

def show_about():
    st.title("📖 About Sentinel")
    st.markdown("""
    Built with state‑of‑the‑art deep learning:
    - **MTCNN** for face detection
    - **FaceNet (VGGFace2)** for face embeddings
    - **Cosine similarity** for matching
    - **CPU‑only** – runs locally, no cloud uploads
    """)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_contact():
    st.title("📬 Contact")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        msg = st.text_area("Message")
        if st.form_submit_button("Send"):
            st.success("Demo mode – message would be sent")
            st.balloons()
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Authenticated pages (Dashboard & features)
# ─────────────────────────────────────────────────────────────────────────────
def show_dashboard():
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/search.png", width=70)
        st.markdown(f"**Welcome, {st.session_state.username}**")
        st.divider()
        menu = st.radio("Navigation", 
            ["Video Detection", "Webcam Live", "System Evaluation", "Profile", "Logout"])
    
    if menu == "Video Detection":
        video_detection_tab()
    elif menu == "Webcam Live":
        webcam_tab()
    elif menu == "System Evaluation":
        evaluation_tab()
    elif menu == "Profile":
        profile_tab()
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.page = "home"
        st.rerun()

def video_detection_tab():
    st.subheader("🎥 Video Detection")
    st.markdown("Upload reference photo(s) and a video file.")

    col1, col2 = st.columns(2)
    with col1:
        ref_files = st.file_uploader("Missing Person Photo(s)", type=['jpg','jpeg','png'],
                                     accept_multiple_files=True, key="vid_ref")
        if ref_files:
            cols = st.columns(min(len(ref_files),3))
            for i, f in enumerate(ref_files):
                with cols[i%3]:
                    st.image(f, caption=f.name.split('.')[0], width=120)
    with col2:
        video_file = st.file_uploader("Video Footage", type=['mp4','avi','mov'], key="vid_vid")
        if video_file:
            st.video(video_file)

    threshold = st.slider("Confidence threshold", 0.50, 0.95, 0.75, 0.01)
    frame_skip = st.selectbox("Process every N frames", [3,5,10,15], index=1)

    run = st.button("🚀 Start Detection", type="primary", disabled=(not ref_files or not video_file))

    if run:
        ref_embeddings = {}
        status = st.empty()
        for ref in ref_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(ref.read())
                tmp_path = tmp.name
            person_name = ref.name.rsplit('.',1)[0]
            status.info(f"Encoding {person_name}...")
            try:
                emb = encode_reference_image(tmp_path)
                ref_embeddings[person_name] = emb
                status.success(f"Encoded {person_name}")
            except ValueError as e:
                st.warning(f"Skipped {ref.name} – {e}")
            finally:
                os.unlink(tmp_path)
        if not ref_embeddings:
            st.error("No valid reference faces found.")
            st.stop()
        status.success(f"{len(ref_embeddings)} reference(s) encoded.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
            tmp_vid.write(video_file.read())
            vid_path = tmp_vid.name

        progress_bar = st.progress(0)
        status_text = st.empty()
        def update_progress(cur, total):
            pct = (cur/total*100) if total>0 else 0
            progress_bar.progress(min(pct,100))
            status_text.text(f"Frame {cur}/{total}")

        with st.spinner("Processing video..."):
            results = process_video(vid_path, ref_embeddings, threshold=threshold,
                                    frame_skip=frame_skip, progress_callback=update_progress)
        os.unlink(vid_path)
        progress_bar.progress(100)

        if not results:
            st.markdown('<div class="warning-box">⚠️ No matches found.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-box">✅ {len(results)} match(es) found!</div>', unsafe_allow_html=True)
            confidences = [r['confidence'] for r in results]
            st.metric("Avg confidence", f"{sum(confidences)/len(confidences):.1%}")
            st.metric("Max confidence", f"{max(confidences):.1%}")

            df = pd.DataFrame(results)
            fig = px.line(df, x='frame_number', y='confidence', markers=True, color='person_name')
            fig.add_hline(y=threshold, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 🖼️ Snapshots")
            cols = st.columns(3)
            for i, r in enumerate(results):
                with cols[i%3]:
                    if os.path.exists(r['snapshot_path']):
                        st.image(r['snapshot_path'], caption=f"{r['person_name']} | {r['confidence']:.1%}")

            # Export
            disp = df[['timestamp','person_name','confidence','frame_number']].copy()
            disp['confidence'] = disp['confidence'].apply(lambda x: f"{x:.1%}")
            st.download_button("⬇️ CSV Report", disp.to_csv(index=False), "results.csv", "text/csv")
            st.download_button("⬇️ JSON Log", json.dumps(results, indent=2, default=str), "log.json", "application/json")

def webcam_tab():
    st.subheader("📷 Live Webcam Detection")
    st.markdown("OpenCV window will open on your desktop. Press **Q** to quit.")
    ref_photo = st.file_uploader("Reference Photo", type=['jpg','jpeg','png'], key="webcam_ref")
    if ref_photo:
        st.image(ref_photo, width=150)
    threshold = st.slider("Confidence threshold", 0.50, 0.95, 0.75, key="webcam_thresh")
    start = st.button("🎥 Start Webcam", type="primary", disabled=not ref_photo)
    if start and ref_photo:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(ref_photo.read())
            ref_path = tmp.name
        try:
            emb = encode_reference_image(ref_path)
            st.success("Opening webcam...")
            process_webcam({"Missing_Person": emb}, threshold=threshold)
            st.success("Webcam closed. Snapshots saved to output/matched_frames/.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            os.unlink(ref_path)

def evaluation_tab():
    st.subheader("📊 System Evaluation")
    st.markdown("Upload same‑person and different‑person image pairs (even count each).")
    col1, col2 = st.columns(2)
    with col1:
        same_files = st.file_uploader("Same‑person pairs", type=['jpg','jpeg','png'],
                                      accept_multiple_files=True, key="same_pairs")
    with col2:
        diff_files = st.file_uploader("Different‑person pairs", type=['jpg','jpeg','png'],
                                      accept_multiple_files=True, key="diff_pairs")
    thresh = st.slider("Threshold", 0.50, 0.95, 0.75, key="eval_thresh")
    run = st.button("Run Evaluation", type="primary", disabled=(not same_files or not diff_files))

    if run:
        pairs = []
        tmp_paths = []
        # Same-person (label=1)
        same_saved = []
        for f in same_files:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tmp.write(f.read())
            tmp.close()
            same_saved.append(tmp.name)
            tmp_paths.append(tmp.name)
        for i in range(0, len(same_saved)-1, 2):
            pairs.append({"ref_path": same_saved[i], "test_path": same_saved[i+1], "label": 1})
        # Different-person (label=0)
        diff_saved = []
        for f in diff_files:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tmp.write(f.read())
            tmp.close()
            diff_saved.append(tmp.name)
            tmp_paths.append(tmp.name)
        for i in range(0, len(diff_saved)-1, 2):
            pairs.append({"ref_path": diff_saved[i], "test_path": diff_saved[i+1], "label": 0})

        with st.spinner(f"Evaluating {len(pairs)} pairs..."):
            metrics = evaluate_on_image_pairs(pairs, threshold=thresh)

        for p in tmp_paths:
            try: os.unlink(p)
            except: pass

        if metrics:
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Accuracy", f"{metrics['accuracy']:.1%}")
            col_b.metric("Precision", f"{metrics['precision']:.1%}")
            col_c.metric("Recall", f"{metrics['recall']:.1%}")
            col_d.metric("F1 Score", f"{metrics['f1_score']:.1%}")
            col_e, col_f, col_g, col_h = st.columns(4)
            col_e.metric("FAR", f"{metrics['false_accept_rate_FAR']:.1%}")
            col_f.metric("FRR", f"{metrics['false_reject_rate_FRR']:.1%}")
            col_g.metric("TP", metrics['true_positives'])
            col_h.metric("TN", metrics['true_negatives'])

def profile_tab():
    st.subheader("👤 Your Profile")
    info = get_user_info(st.session_state.username)
    if info:
        st.write(f"**Username:** {info['username']}")
        with st.form("profile_form"):
            email = st.text_input("Email", value=info['email'] or "")
            full_name = st.text_input("Full Name", value=info['full_name'] or "")
            if st.form_submit_button("Update"):
                update_user_profile(st.session_state.username, email, full_name)
                st.success("Profile updated")
        with st.expander("Change Password"):
            with st.form("pw_form"):
                old = st.text_input("Current Password", type="password")
                new1 = st.text_input("New Password", type="password")
                new2 = st.text_input("Confirm New", type="password")
                if st.form_submit_button("Change"):
                    if verify_user(st.session_state.username, old):
                        if new1 == new2 and len(new1) >= 4:
                            update_password(st.session_state.username, new1)
                            st.success("Password changed")
                        else:
                            st.error("Passwords do not match or too short")
                    else:
                        st.error("Current password incorrect")
        st.caption(f"Member since: {info['created_at']}")

# ─────────────────────────────────────────────────────────────────────────────
# Main navigation router
# ─────────────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        # Public pages
        if st.session_state.page == "home":
            show_home()
        elif st.session_state.page == "login":
            show_login()
        elif st.session_state.page == "register":
            show_register()
        elif st.session_state.page == "about":
            show_about()
        elif st.session_state.page == "contact":
            show_contact()
        else:
            show_home()
        
        # Sidebar for public navigation
        with st.sidebar:
            st.markdown("### Public Menu")
            if st.button("🏠 Home"):
                st.session_state.page = "home"
                st.rerun()
            if st.button("🔐 Login"):
                st.session_state.page = "login"
                st.rerun()
            if st.button("📝 Register"):
                st.session_state.page = "register"
                st.rerun()
            if st.button("📖 About"):
                st.session_state.page = "about"
                st.rerun()
            if st.button("📬 Contact"):
                st.session_state.page = "contact"
                st.rerun()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()