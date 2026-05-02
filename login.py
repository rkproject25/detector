import streamlit as st

def show_login_page():
    st.set_page_config(
        page_title="Sentinel — AI Face Detection",
        page_icon="◉",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    font-family: 'Inter', sans-serif !important;
    background: #060E1A !important;
    color: #E2EAF4 !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    background: transparent !important;
}

[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stElementContainer"] {
    padding: 0 !important; margin: 0 !important; width: 100% !important;
}

/* ── ENTER BUTTON ── */
div[data-testid="stButton"] {
    display: flex !important;
    justify-content: center !important;
    padding: 0 !important;
    margin: 0 !important;
    background: #060E1A !important;
    width: 100% !important;
}
div[data-testid="stButton"] button {
    background: linear-gradient(180deg, #5DCAA5, #3DAF8A) !important;
    color: #072E58 !important;
    border: none !important;
    border-radius: 9px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 14px 36px !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
    box-shadow: 0 4px 24px rgba(93,202,165,0.25) !important;
    transition: all 0.18s ease !important;
    width: auto !important;
}
div[data-testid="stButton"] button:hover {
    box-shadow: 0 6px 32px rgba(93,202,165,0.4) !important;
    transform: translateY(-1px) !important;
}

@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }
@keyframes scan  { 0%{top:8%} 100%{top:90%} }
</style>
""", unsafe_allow_html=True)

    # ── NAV ──────────────────────────────────────────────────────────
    # All HTML below is deliberately flush-left (no indentation).
    # Streamlit's markdown parser treats any line indented 4+ spaces as a code
    # block, even with unsafe_allow_html=True. Keeping lines at column 0
    # prevents that.
    st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;padding:18px 60px;border-bottom:1px solid rgba(255,255,255,0.06);background:#060E1A;font-family:'Inter',sans-serif">
<div style="font-size:17px;font-weight:700;color:#fff;letter-spacing:-.03em;display:flex;align-items:center;gap:8px">
<div style="width:8px;height:8px;border-radius:50%;background:#5DCAA5"></div>
Sentinel
</div>
<div style="display:flex;gap:32px;font-size:13px;color:rgba(180,208,240,0.5);font-weight:500">
<span>Solution</span><span>Features</span><span>How it works</span><span>Use cases</span>
</div>
<div style="display:flex;gap:12px;align-items:center">
<span style="font-size:13px;font-weight:500;color:rgba(180,208,240,0.55);border:1px solid rgba(255,255,255,0.1);border-radius:7px;padding:7px 16px;cursor:pointer">Sign in</span>
<span style="font-size:13px;font-weight:600;color:#072E58;background:linear-gradient(180deg,#5DCAA5,#3DAF8A);border-radius:7px;padding:8px 18px;cursor:pointer">Request demo</span>
</div>
</div>
""", unsafe_allow_html=True)

    # ── HERO ─────────────────────────────────────────────────────────
    st.markdown("""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:72px;padding:88px 60px 80px;max-width:1200px;margin:0 auto;align-items:center;font-family:'Inter',sans-serif">
<div>
<div style="display:inline-flex;align-items:center;gap:7px;background:rgba(93,202,165,0.08);border:1px solid rgba(93,202,165,0.2);border-radius:100px;padding:5px 14px 5px 9px;margin-bottom:28px">
<div style="width:6px;height:6px;border-radius:50%;background:#5DCAA5;animation:blink 2s ease-in-out infinite"></div>
<span style="font-size:11px;font-weight:600;letter-spacing:.13em;color:rgba(93,202,165,.85);text-transform:uppercase">AI · Deep learning · Real-time</span>
</div>
<div style="font-size:46px;font-weight:700;color:#fff;line-height:1.07;letter-spacing:-.035em;margin-bottom:22px">
Find anyone.<br>In any footage.<br><span style="color:#5DCAA5">In real time.</span>
</div>
<p style="font-size:15px;color:rgba(180,208,240,0.58);line-height:1.75;max-width:420px;margin-bottom:36px">
AI-powered facial recognition for identifying missing persons in video streams and surveillance footage. Built for law enforcement and field operations.
</p>
<div style="display:flex;gap:12px;align-items:center;margin-bottom:32px">
<div style="font-size:14px;font-weight:600;color:#072E58;background:linear-gradient(180deg,#5DCAA5,#3DAF8A);border-radius:9px;padding:13px 28px;cursor:pointer;display:inline-block">Get started</div>
<div style="font-size:14px;font-weight:500;color:rgba(180,208,240,0.75);border:1px solid rgba(255,255,255,0.12);border-radius:9px;padding:12px 22px;cursor:pointer;display:inline-block">Request demo</div>
</div>
<div style="display:flex;gap:24px;padding-top:28px;border-top:1px solid rgba(255,255,255,0.07)">
<div style="font-size:11px;color:rgba(180,208,240,0.38);letter-spacing:.07em;text-transform:uppercase;display:flex;align-items:center;gap:6px">
<div style="width:4px;height:4px;border-radius:50%;background:#5DCAA5;opacity:.6"></div>FaceNet · VGGFace2
</div>
<div style="font-size:11px;color:rgba(180,208,240,0.38);letter-spacing:.07em;text-transform:uppercase;display:flex;align-items:center;gap:6px">
<div style="width:4px;height:4px;border-radius:50%;background:#5DCAA5;opacity:.6"></div>On-device processing
</div>
<div style="font-size:11px;color:rgba(180,208,240,0.38);letter-spacing:.07em;text-transform:uppercase;display:flex;align-items:center;gap:6px">
<div style="width:4px;height:4px;border-radius:50%;background:#5DCAA5;opacity:.6"></div>Evidence logging
</div>
</div>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.1);border-radius:14px;overflow:hidden">
<div style="background:#0D1E35;padding:11px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.07)">
<div style="font-size:10px;font-weight:600;letter-spacing:.12em;color:rgba(180,208,240,0.4);text-transform:uppercase;display:flex;align-items:center;gap:7px">
<div style="width:6px;height:6px;border-radius:50%;background:#E24B4A;animation:blink 1.2s ease-in-out infinite"></div>CAM-04 · TERMINAL B
</div>
<div style="font-size:10px;color:rgba(180,208,240,0.28);letter-spacing:.05em">14:27:39 UTC</div>
</div>
<div style="background:#061020;height:290px;position:relative;overflow:hidden">
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.022) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.022) 1px,transparent 1px);background-size:28px 28px"></div>
<div style="position:absolute;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent 5%,rgba(93,202,165,0.35) 50%,transparent 95%);animation:scan 3s ease-in-out infinite"></div>
<div style="position:absolute;top:12px;left:14px">
<span style="font-size:9px;font-weight:600;letter-spacing:.1em;color:rgba(180,208,240,0.28);text-transform:uppercase;display:block;line-height:1.6">Model</span>
<span style="font-size:11px;font-weight:600;color:rgba(93,202,165,0.65);display:block;margin-bottom:8px">FaceNet</span>
<span style="font-size:9px;font-weight:600;letter-spacing:.1em;color:rgba(180,208,240,0.28);text-transform:uppercase;display:block;line-height:1.6">Threshold</span>
<span style="font-size:11px;font-weight:600;color:rgba(93,202,165,0.65);display:block">0.75</span>
</div>
<div style="position:absolute;top:12px;right:14px;text-align:right">
<span style="font-size:9px;font-weight:600;letter-spacing:.1em;color:rgba(180,208,240,0.28);text-transform:uppercase;display:block;line-height:1.6">Faces</span>
<span style="font-size:11px;font-weight:600;color:rgba(93,202,165,0.65);display:block;margin-bottom:8px">1</span>
<span style="font-size:9px;font-weight:600;letter-spacing:.1em;color:rgba(180,208,240,0.28);text-transform:uppercase;display:block;line-height:1.6">Frame</span>
<span style="font-size:11px;font-weight:600;color:rgba(93,202,165,0.65);display:block">3,847</span>
</div>
<div style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%)">
<div style="width:88px;height:88px;border-radius:50%;background:rgba(55,138,221,0.1);border:1px solid rgba(55,138,221,0.18);display:flex;align-items:center;justify-content:center">
<div style="width:48px;height:48px;border-radius:50%;background:rgba(55,138,221,0.14);border:1px solid rgba(55,138,221,0.22)"></div>
</div>
</div>
<div style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);width:116px;height:116px">
<div style="position:absolute;top:-4px;left:-4px;width:14px;height:14px;border-top:2px solid #5DCAA5;border-left:2px solid #5DCAA5"></div>
<div style="position:absolute;top:-4px;right:-4px;width:14px;height:14px;border-top:2px solid #5DCAA5;border-right:2px solid #5DCAA5"></div>
<div style="position:absolute;bottom:-4px;left:-4px;width:14px;height:14px;border-bottom:2px solid #5DCAA5;border-left:2px solid #5DCAA5"></div>
<div style="position:absolute;bottom:-4px;right:-4px;width:14px;height:14px;border-bottom:2px solid #5DCAA5;border-right:2px solid #5DCAA5"></div>
</div>
<div style="position:absolute;left:50%;top:66%;transform:translateX(-50%);background:rgba(93,202,165,0.1);border:1px solid rgba(93,202,165,0.28);border-radius:7px;padding:5px 14px;text-align:center;white-space:nowrap">
<div style="font-size:9px;font-weight:600;letter-spacing:.1em;color:rgba(93,202,165,.55);text-transform:uppercase">Match confidence</div>
<div style="font-size:17px;font-weight:700;color:#5DCAA5;letter-spacing:-.01em;line-height:1.1;margin-top:1px">94.2%</div>
</div>
</div>
<div style="padding:11px 16px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,0.06)">
<div style="display:flex;align-items:center;gap:7px;font-size:10px;font-weight:700;color:#5DCAA5;letter-spacing:.1em;text-transform:uppercase">
<div style="width:5px;height:5px;border-radius:50%;background:#5DCAA5;animation:blink 1.5s ease-in-out infinite"></div>MATCH DETECTED
</div>
<div style="font-size:10px;color:rgba(180,208,240,0.28);letter-spacing:.05em">42 ms · 24 fps</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── METRICS ──────────────────────────────────────────────────────
    st.markdown("""
<div style="max-width:1200px;margin:0 auto;padding:0 60px 80px;font-family:'Inter',sans-serif">
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.07);border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.07)">
<div style="background:#0A1628;padding:30px 24px;text-align:center">
<div style="font-size:30px;font-weight:700;color:#fff;letter-spacing:-.03em"><span style="color:#5DCAA5">512</span>-d</div>
<div style="font-size:11px;color:rgba(180,208,240,0.38);text-transform:uppercase;letter-spacing:.1em;margin-top:7px">Embedding dimension</div>
</div>
<div style="background:#0A1628;padding:30px 24px;text-align:center">
<div style="font-size:30px;font-weight:700;color:#fff;letter-spacing:-.03em"><span style="color:#5DCAA5">&lt;50</span>ms</div>
<div style="font-size:11px;color:rgba(180,208,240,0.38);text-transform:uppercase;letter-spacing:.1em;margin-top:7px">Detection speed</div>
</div>
<div style="background:#0A1628;padding:30px 24px;text-align:center">
<div style="font-size:30px;font-weight:700;color:#fff;letter-spacing:-.03em"><span style="color:#5DCAA5">99.6</span>%</div>
<div style="font-size:11px;color:rgba(180,208,240,0.38);text-transform:uppercase;letter-spacing:.1em;margin-top:7px">LFW accuracy</div>
</div>
<div style="background:#0A1628;padding:30px 24px;text-align:center">
<div style="font-size:30px;font-weight:700;color:#fff;letter-spacing:-.03em"><span style="color:#5DCAA5">10k</span>+</div>
<div style="font-size:11px;color:rgba(180,208,240,0.38);text-transform:uppercase;letter-spacing:.1em;margin-top:7px">Streams processed</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── FEATURES ─────────────────────────────────────────────────────
    st.markdown("""
<div style="max-width:1200px;margin:0 auto;padding:80px 60px;font-family:'Inter',sans-serif;border-top:1px solid rgba(255,255,255,0.06)">
<div style="font-size:11px;font-weight:600;letter-spacing:.15em;color:rgba(93,202,165,0.65);text-transform:uppercase;margin-bottom:12px">Capabilities</div>
<div style="font-size:32px;font-weight:700;color:#fff;letter-spacing:-.03em;line-height:1.12;margin-bottom:14px">Everything needed to find who's in the footage.</div>
<p style="font-size:15px;color:rgba(180,208,240,0.5);line-height:1.75;max-width:500px;margin-bottom:52px">Purpose-built for field deployments where speed, precision, and evidence quality are non-negotiable.</p>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px">
<div style="width:38px;height:38px;border-radius:10px;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.14);display:flex;align-items:center;justify-content:center;margin-bottom:18px">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#5DCAA5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="6" r="3"/><path d="M2 14c0-3 2.7-5 6-5s6 2 6 5"/><rect x="1" y="1" width="14" height="14" rx="3"/></svg>
</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:9px">Real-time face detection</div>
<p style="font-size:13px;color:rgba(180,208,240,0.45);line-height:1.65">MTCNN-powered detection with &lt;50ms latency per frame, suitable for live surveillance streams.</p>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px">
<div style="width:38px;height:38px;border-radius:10px;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.14);display:flex;align-items:center;justify-content:center;margin-bottom:18px">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#5DCAA5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="5" cy="6" r="2"/><circle cx="11" cy="6" r="2"/><path d="M1 13c0-2.5 1.8-4 4-4m6 0c2.2 0 4 1.5 4 4"/></svg>
</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:9px">Multi-person tracking</div>
<p style="font-size:13px;color:rgba(180,208,240,0.45);line-height:1.65">Track multiple subjects simultaneously across frames with per-identity confidence scores.</p>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px">
<div style="width:38px;height:38px;border-radius:10px;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.14);display:flex;align-items:center;justify-content:center;margin-bottom:18px">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#5DCAA5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6"/><path d="M8 5v3l2 2"/></svg>
</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:9px">Adjustable threshold</div>
<p style="font-size:13px;color:rgba(180,208,240,0.45);line-height:1.65">Fine-tune cosine similarity thresholds per operation to balance precision against recall.</p>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px">
<div style="width:38px;height:38px;border-radius:10px;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.14);display:flex;align-items:center;justify-content:center;margin-bottom:18px">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#5DCAA5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3h10v10H3z"/><path d="M6 7h4M6 10h4M6 4h4"/></svg>
</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:9px">Evidence logging</div>
<p style="font-size:13px;color:rgba(180,208,240,0.45);line-height:1.65">Every match timestamped and exported as structured JSON or CSV for chain of custody.</p>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px">
<div style="width:38px;height:38px;border-radius:10px;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.14);display:flex;align-items:center;justify-content:center;margin-bottom:18px">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#5DCAA5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="12" height="12" rx="2"/><path d="M8 5v6M5 8h6"/></svg>
</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:9px">On-device processing</div>
<p style="font-size:13px;color:rgba(180,208,240,0.45);line-height:1.65">All inference runs locally — no footage leaves your network. Privacy-first by design.</p>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px">
<div style="width:38px;height:38px;border-radius:10px;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.14);display:flex;align-items:center;justify-content:center;margin-bottom:18px">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#5DCAA5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2,12 5,8 8,10 11,5 14,7"/></svg>
</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:9px">Analytics dashboard</div>
<p style="font-size:13px;color:rgba(180,208,240,0.45);line-height:1.65">Confidence trends, frame-by-frame breakdowns, and evaluation metrics in one interface.</p>
</div>

</div>
</div>
""", unsafe_allow_html=True)

    # ── HOW IT WORKS ─────────────────────────────────────────────────
    st.markdown("""
<div style="max-width:1200px;margin:0 auto;padding:80px 60px;font-family:'Inter',sans-serif;border-top:1px solid rgba(255,255,255,0.06)">
<div style="font-size:11px;font-weight:600;letter-spacing:.15em;color:rgba(93,202,165,0.65);text-transform:uppercase;margin-bottom:12px">How it works</div>
<div style="font-size:32px;font-weight:700;color:#fff;letter-spacing:-.03em;line-height:1.12;margin-bottom:14px">Four steps from photo to match alert.</div>
<p style="font-size:15px;color:rgba(180,208,240,0.5);line-height:1.75;max-width:500px;margin-bottom:52px">Sentinel's pipeline is optimized for operational speed without compromising accuracy.</p>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px">

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px 20px;text-align:center">
<div style="width:38px;height:38px;border-radius:50%;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.18);display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:13px;font-weight:700;color:#5DCAA5">01</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:8px">Upload reference</div>
<p style="font-size:12px;color:rgba(180,208,240,0.42);line-height:1.65">Provide one or more clear, front-facing photos of the person to locate.</p>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px 20px;text-align:center">
<div style="width:38px;height:38px;border-radius:50%;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.18);display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:13px;font-weight:700;color:#5DCAA5">02</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:8px">Extract embeddings</div>
<p style="font-size:12px;color:rgba(180,208,240,0.42);line-height:1.65">FaceNet encodes each reference into a 512-dimensional embedding vector.</p>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px 20px;text-align:center">
<div style="width:38px;height:38px;border-radius:50%;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.18);display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:13px;font-weight:700;color:#5DCAA5">03</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:8px">Scan footage</div>
<p style="font-size:12px;color:rgba(180,208,240,0.42);line-height:1.65">MTCNN detects and extracts faces from every frame of video or live feed.</p>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px 20px;text-align:center">
<div style="width:38px;height:38px;border-radius:50%;background:rgba(93,202,165,0.07);border:1px solid rgba(93,202,165,0.18);display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:13px;font-weight:700;color:#5DCAA5">04</div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:8px">Instant alerts</div>
<p style="font-size:12px;color:rgba(180,208,240,0.42);line-height:1.65">Matches above the threshold trigger alerts with snapshots and timestamps.</p>
</div>

</div>
</div>
""", unsafe_allow_html=True)

    # ── USE CASES ────────────────────────────────────────────────────
    st.markdown("""
<div style="max-width:1200px;margin:0 auto;padding:80px 60px;font-family:'Inter',sans-serif;border-top:1px solid rgba(255,255,255,0.06)">
<div style="font-size:11px;font-weight:600;letter-spacing:.15em;color:rgba(93,202,165,0.65);text-transform:uppercase;margin-bottom:12px">Use cases</div>
<div style="font-size:32px;font-weight:700;color:#fff;letter-spacing:-.03em;line-height:1.12;margin-bottom:14px">Built for the people who need it most.</div>
<p style="font-size:15px;color:rgba(180,208,240,0.5);line-height:1.75;max-width:500px;margin-bottom:52px">Sentinel is purpose-built for high-stakes environments where identification speed is critical.</p>
<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px">

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px;display:flex;align-items:flex-start;gap:16px">
<div style="width:42px;height:42px;border-radius:10px;background:rgba(55,138,221,0.07);border:1px solid rgba(55,138,221,0.14);display:flex;align-items:center;justify-content:center;flex-shrink:0">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#378ADD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2L3 5v4c0 3 2.5 5 5 5s5-2 5-5V5L8 2z"/></svg>
</div>
<div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:7px">Law enforcement</div>
<p style="font-size:13px;color:rgba(180,208,240,0.42);line-height:1.65">Scan archived CCTV footage or live feeds to rapidly locate suspects or persons of interest.</p>
</div>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px;display:flex;align-items:flex-start;gap:16px">
<div style="width:42px;height:42px;border-radius:10px;background:rgba(55,138,221,0.07);border:1px solid rgba(55,138,221,0.14);display:flex;align-items:center;justify-content:center;flex-shrink:0">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#378ADD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="6" r="3"/><path d="M2 14s1-4 6-4 6 4 6 4"/><path d="M13 2l2 2-2 2"/></svg>
</div>
<div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:7px">Missing person search</div>
<p style="font-size:13px;color:rgba(180,208,240,0.42);line-height:1.65">Cross-reference a missing person's photo against hours of public footage in minutes.</p>
</div>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px;display:flex;align-items:flex-start;gap:16px">
<div style="width:42px;height:42px;border-radius:10px;background:rgba(55,138,221,0.07);border:1px solid rgba(55,138,221,0.14);display:flex;align-items:center;justify-content:center;flex-shrink:0">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#378ADD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="12" height="9" rx="2"/><circle cx="8" cy="8.5" r="2.5"/><path d="M6 4V3a2 2 0 014 0v1"/></svg>
</div>
<div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:7px">CCTV monitoring</div>
<p style="font-size:13px;color:rgba(180,208,240,0.42);line-height:1.65">Automate watch-list monitoring across multiple camera feeds in real time.</p>
</div>
</div>

<div style="background:#0A1628;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:26px;display:flex;align-items:flex-start;gap:16px">
<div style="width:42px;height:42px;border-radius:10px;background:rgba(55,138,221,0.07);border:1px solid rgba(55,138,221,0.14);display:flex;align-items:center;justify-content:center;flex-shrink:0">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#378ADD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4h12v8a2 2 0 01-2 2H4a2 2 0 01-2-2V4z"/><path d="M2 4l6-2 6 2"/></svg>
</div>
<div>
<div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:7px">Security operations</div>
<p style="font-size:13px;color:rgba(180,208,240,0.42);line-height:1.65">Integrate with existing infrastructure for perimeter access and identity verification.</p>
</div>
</div>

</div>
</div>
""", unsafe_allow_html=True)

    # ── CTA BAND ─────────────────────────────────────────────────────
    st.markdown("""
<div style="background:#060E1A;padding:60px 0 20px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;font-family:'Inter',sans-serif">
<div style="font-size:28px;font-weight:700;color:#fff;letter-spacing:-.03em;margin-bottom:12px">Ready to start?</div>
<p style="font-size:15px;color:rgba(180,208,240,0.5);margin-bottom:32px">Launch the detection dashboard and begin your first scan.</p>
</div>
""", unsafe_allow_html=True)

    # ── ENTER BUTTON (real Streamlit button — always works) ──────────
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Launch Sentinel →", key="enter_btn", use_container_width=True):
            st.session_state.authenticated = True
            st.rerun()

    # ── FOOTER ───────────────────────────────────────────────────────
    st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,0.06);padding:30px 60px 40px;display:flex;align-items:center;justify-content:space-between;max-width:1200px;margin:20px auto 0;font-family:'Inter',sans-serif">
<div style="font-size:15px;font-weight:700;color:rgba(180,208,240,0.35);letter-spacing:-.02em">Sentinel</div>
<div style="font-size:11px;color:rgba(180,208,240,0.22);letter-spacing:.05em">AUTHORISED PERSONNEL ONLY · ALL SESSIONS LOGGED</div>
</div>
""", unsafe_allow_html=True)


def logout():
    st.session_state.authenticated = False
    st.rerun() 