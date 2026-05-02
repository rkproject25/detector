"""
gui.py — Lost Person Detection System
Classic Tkinter GUI: Splash → Login → Dashboard → Feature Panels
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# THEME CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
C_BG        = "#0d1117"   # near-black background
C_PANEL     = "#161b22"   # card / panel background
C_BORDER    = "#30363d"   # subtle border
C_ACCENT    = "#238636"   # green accent (action)
C_ACCENT2   = "#1f6feb"   # blue accent (info)
C_DANGER    = "#da3633"   # red (alert/warning)
C_TEXT      = "#e6edf3"   # primary text
C_MUTED     = "#8b949e"   # secondary / muted text
C_HIGHLIGHT = "#f0b429"   # amber — used for logo badge

FONT_TITLE   = ("Georgia",        28, "bold")
FONT_BRAND   = ("Georgia",        16, "italic")
FONT_HEADING = ("Courier New",    13, "bold")
FONT_BODY    = ("Courier New",    11)
FONT_SMALL   = ("Courier New",     9)
FONT_BTN     = ("Courier New",    12, "bold")
FONT_LABEL   = ("Courier New",    10)

# ─────────────────────────────────────────────────────────────────────────────
# DUMMY AUTH  (replace with real DB check as needed)
# ─────────────────────────────────────────────────────────────────────────────
USERS = {
    "admin":    "admin",
    "operator": "detect99",
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER WIDGETS
# ─────────────────────────────────────────────────────────────────────────────

def styled_button(parent, text, command, color=None, width=22):
    """A flat, bordered button that follows the dark theme."""
    bg = color or C_ACCENT
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONT_BTN,
        bg=bg,
        fg=C_TEXT,
        activebackground=C_BORDER,
        activeforeground=C_TEXT,
        relief="flat",
        bd=0,
        padx=10,
        pady=8,
        width=width,
        cursor="hand2",
    )
    # hover effect
    def on_enter(e): btn.config(bg=_darken(bg))
    def on_leave(e): btn.config(bg=bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def _darken(hex_color):
    """Returns a slightly darker version of a hex color."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    factor = 0.75
    return "#{:02x}{:02x}{:02x}".format(int(r*factor), int(g*factor), int(b*factor))


def separator(parent, pady=6):
    tk.Frame(parent, bg=C_BORDER, height=1).pack(fill="x", padx=20, pady=pady)


def label(parent, text, font=None, color=None, anchor="w", pady=2):
    tk.Label(
        parent, text=text,
        font=font or FONT_BODY,
        bg=C_PANEL, fg=color or C_TEXT,
        anchor=anchor
    ).pack(fill="x", padx=20, pady=pady)


# ─────────────────────────────────────────────────────────────────────────────
# SCREEN BASE CLASS
# ─────────────────────────────────────────────────────────────────────────────

class Screen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=C_BG)
        self.app = app
        self.build()

    def build(self):
        """Override in subclasses."""
        pass

    def show(self):
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.lift()

    def hide(self):
        self.place_forget()


# ─────────────────────────────────────────────────────────────────────────────
# 1. SPLASH SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class SplashScreen(Screen):
    def build(self):
        self.configure(bg=C_BG)

        # ── centre container
        box = tk.Frame(self, bg=C_BG)
        box.place(relx=0.5, rely=0.5, anchor="center")

        # ── badge / icon substitute
        badge = tk.Label(
            box,
            text="⦿",
            font=("Georgia", 64),
            bg=C_BG,
            fg=C_HIGHLIGHT,
        )
        badge.pack(pady=(0, 6))

        # ── project name
        tk.Label(
            box,
            text="LOST PERSON",
            font=("Georgia", 34, "bold"),
            bg=C_BG,
            fg=C_TEXT,
        ).pack()

        tk.Label(
            box,
            text="DETECTION  SYSTEM",
            font=("Georgia", 34, "bold"),
            bg=C_BG,
            fg=C_HIGHLIGHT,
        ).pack()

        # ── thin rule
        tk.Frame(box, bg=C_BORDER, height=1, width=380).pack(pady=14)

        # ── tagline
        tk.Label(
            box,
            text="AI-powered face recognition for missing persons",
            font=FONT_BRAND,
            bg=C_BG,
            fg=C_MUTED,
        ).pack()

        tk.Label(
            box,
            text="MTCNN  ·  FaceNet / VGGFace2  ·  Cosine Similarity",
            font=FONT_SMALL,
            bg=C_BG,
            fg=C_BORDER,
        ).pack(pady=(4, 0))

        # ── enter button
        tk.Frame(box, height=30, bg=C_BG).pack()

        proceed = styled_button(box, "▶   ENTER SYSTEM", self._go_login,
                                color=C_ACCENT2, width=26)
        proceed.pack(pady=4)

        tk.Label(
            box,
            text="Authorised personnel only",
            font=FONT_SMALL,
            bg=C_BG,
            fg=C_DANGER,
        ).pack(pady=(8, 0))

    def _go_login(self):
        self.app.show_screen("login")


# ─────────────────────────────────────────────────────────────────────────────
# 2. LOGIN SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class LoginScreen(Screen):
    def build(self):
        self.configure(bg=C_BG)

        # ── card
        card = tk.Frame(self, bg=C_PANEL, bd=0, relief="flat",
                        highlightbackground=C_BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=480)

        # ── header strip
        header = tk.Frame(card, bg=C_ACCENT2, height=6)
        header.pack(fill="x")

        tk.Label(card, text="⦿", font=("Georgia", 26),
                 bg=C_PANEL, fg=C_HIGHLIGHT).pack(pady=(22, 0))

        tk.Label(card, text="SYSTEM LOGIN",
                 font=("Georgia", 18, "bold"),
                 bg=C_PANEL, fg=C_TEXT).pack()

        tk.Label(card, text="Lost Person Detection System",
                 font=FONT_BRAND, bg=C_PANEL, fg=C_MUTED).pack(pady=(2, 20))

        separator(card, pady=0)

        # ── form
        form = tk.Frame(card, bg=C_PANEL)
        form.pack(padx=40, pady=20, fill="x")

        tk.Label(form, text="USERNAME", font=FONT_SMALL,
                 bg=C_PANEL, fg=C_MUTED, anchor="w").pack(fill="x")
        self.user_var = tk.StringVar()
        user_entry = tk.Entry(form, textvariable=self.user_var,
                              font=FONT_BODY,
                              bg=C_BG, fg=C_TEXT,
                              insertbackground=C_TEXT,
                              relief="flat",
                              highlightbackground=C_BORDER,
                              highlightthickness=1)
        user_entry.pack(fill="x", ipady=7, pady=(2, 14))

        tk.Label(form, text="PASSWORD", font=FONT_SMALL,
                 bg=C_PANEL, fg=C_MUTED, anchor="w").pack(fill="x")
        self.pass_var = tk.StringVar()
        pass_entry = tk.Entry(form, textvariable=self.pass_var,
                              show="●", font=FONT_BODY,
                              bg=C_BG, fg=C_TEXT,
                              insertbackground=C_TEXT,
                              relief="flat",
                              highlightbackground=C_BORDER,
                              highlightthickness=1)
        pass_entry.pack(fill="x", ipady=7, pady=(2, 6))

        # error label
        self.err_var = tk.StringVar()
        tk.Label(form, textvariable=self.err_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_DANGER).pack(fill="x")

        # login button
        tk.Frame(form, height=8, bg=C_PANEL).pack()
        btn = styled_button(form, "LOGIN  →", self._attempt_login,
                            color=C_ACCENT, width=30)
        btn.pack(fill="x")

        # back link
        back = tk.Label(card, text="← Back to home",
                        font=FONT_SMALL, bg=C_PANEL,
                        fg=C_MUTED, cursor="hand2")
        back.pack(pady=10)
        back.bind("<Button-1>", lambda e: self.app.show_screen("splash"))

        # bind Enter key
        self.bind_all("<Return>", lambda e: self._attempt_login())
        user_entry.focus_set()

    def _attempt_login(self):
        u = self.user_var.get().strip()
        p = self.pass_var.get().strip()
        if not u or not p:
            self.err_var.set("  ⚠  Both fields are required.")
            return
        if USERS.get(u) == p:
            self.err_var.set("")
            self.app.current_user = u
            self.app.show_screen("dashboard")
        else:
            self.err_var.set("  ⚠  Invalid credentials. Try again.")
            self.pass_var.set("")


# ─────────────────────────────────────────────────────────────────────────────
# 3. DASHBOARD SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class DashboardScreen(Screen):
    def build(self):
        self.configure(bg=C_BG)

        # ── top bar
        topbar = tk.Frame(self, bg=C_PANEL, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="⦿  Lost Person Detection System",
                 font=("Georgia", 13, "bold"),
                 bg=C_PANEL, fg=C_HIGHLIGHT).pack(side="left", padx=20, pady=14)

        self.user_label = tk.Label(topbar, text="",
                                   font=FONT_SMALL, bg=C_PANEL, fg=C_MUTED)
        self.user_label.pack(side="right", padx=10)

        logout_btn = tk.Label(topbar, text="Logout  ⏻",
                              font=FONT_SMALL, bg=C_PANEL,
                              fg=C_DANGER, cursor="hand2")
        logout_btn.pack(side="right", padx=10, pady=14)
        logout_btn.bind("<Button-1>", lambda e: self.app.logout())

        # ── welcome strip
        tk.Frame(self, bg=C_BORDER, height=1).pack(fill="x")

        welcome = tk.Frame(self, bg=C_BG)
        welcome.pack(pady=(36, 10))

        tk.Label(welcome, text="SELECT AN OPERATION",
                 font=("Georgia", 20, "bold"),
                 bg=C_BG, fg=C_TEXT).pack()
        tk.Label(welcome, text="Choose a module below to begin",
                 font=FONT_BRAND, bg=C_BG, fg=C_MUTED).pack(pady=4)

        # ── cards row
        cards_row = tk.Frame(self, bg=C_BG)
        cards_row.pack(pady=20, padx=40)

        options = [
            {
                "icon":    "🎥",
                "title":   "VIDEO\nDETECTION",
                "desc":    "Scan a recorded video file\nfor a missing person's face.\nExport matches as CSV / JSON.",
                "color":   C_ACCENT2,
                "screen":  "video",
            },
            {
                "icon":    "📷",
                "title":   "WEBCAM\nLIVE MODE",
                "desc":    "Real-time detection using\nyour webcam feed.\nPress Q to stop session.",
                "color":   C_ACCENT,
                "screen":  "webcam",
            },
            {
                "icon":    "📊",
                "title":   "SYSTEM\nEVALUATION",
                "desc":    "Measure precision, recall,\nF1 score, FAR & FRR\nusing labelled test pairs.",
                "color":   C_HIGHLIGHT,
                "screen":  "evaluation",
            },
        ]

        for opt in options:
            self._make_card(cards_row, opt)

        # ── status bar
        tk.Frame(self, bg=C_BORDER, height=1).pack(fill="x", side="bottom")
        status = tk.Frame(self, bg=C_PANEL, height=30)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)
        tk.Label(status,
                 text="Models: MTCNN  ·  FaceNet/VGGFace2  ·  Cosine Similarity  ·  CPU",
                 font=FONT_SMALL, bg=C_PANEL, fg=C_MUTED).pack(side="left", padx=16, pady=7)

    def _make_card(self, parent, opt):
        """Builds one option card."""
        card = tk.Frame(parent, bg=C_PANEL, width=220, height=320,
                        highlightbackground=opt["color"],
                        highlightthickness=2, bd=0)
        card.pack(side="left", padx=18)
        card.pack_propagate(False)

        # colour top accent
        tk.Frame(card, bg=opt["color"], height=5).pack(fill="x")

        # icon
        tk.Label(card, text=opt["icon"], font=("Segoe UI Emoji", 36),
                 bg=C_PANEL).pack(pady=(20, 6))

        # title
        tk.Label(card, text=opt["title"],
                 font=("Courier New", 13, "bold"),
                 bg=C_PANEL, fg=C_TEXT,
                 justify="center").pack()

        # thin rule
        tk.Frame(card, bg=C_BORDER, height=1, width=160).pack(pady=10)

        # description
        tk.Label(card, text=opt["desc"],
                 font=FONT_SMALL, bg=C_PANEL,
                 fg=C_MUTED, justify="center").pack(padx=12)

        # spacer
        tk.Frame(card, bg=C_PANEL).pack(expand=True)

        # action button
        btn = styled_button(card, "OPEN  →",
                            lambda s=opt["screen"]: self.app.show_screen(s),
                            color=opt["color"], width=16)
        btn.pack(pady=16)

        # hover glow on whole card
        def on_enter(e, c=card, col=opt["color"]):
            c.config(highlightbackground=col, highlightthickness=3)
        def on_leave(e, c=card, col=opt["color"]):
            c.config(highlightbackground=col, highlightthickness=2)
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    def refresh_user(self):
        self.user_label.config(text=f"Logged in as:  {self.app.current_user}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. VIDEO DETECTION PANEL
# ─────────────────────────────────────────────────────────────────────────────

class VideoScreen(Screen):
    def build(self):
        self.configure(bg=C_BG)
        self._build_topbar("🎥  Video Detection")

        content = tk.Frame(self, bg=C_BG)
        content.pack(fill="both", expand=True, padx=40, pady=20)

        # ── left: inputs
        left = tk.Frame(content, bg=C_PANEL,
                        highlightbackground=C_BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="INPUTS", font=FONT_HEADING,
                 bg=C_PANEL, fg=C_ACCENT2).pack(anchor="w", padx=16, pady=(14, 4))
        separator(left, pady=2)

        # reference photo
        tk.Label(left, text="Reference Photo (missing person)",
                 font=FONT_LABEL, bg=C_PANEL, fg=C_MUTED).pack(anchor="w", padx=16, pady=(10, 2))
        self.ref_path_var = tk.StringVar(value="No file selected")
        tk.Label(left, textvariable=self.ref_path_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_MUTED,
                 wraplength=280, anchor="w").pack(anchor="w", padx=16)
        styled_button(left, "Browse Photo…", self._pick_ref,
                      color=C_ACCENT2, width=20).pack(anchor="w", padx=16, pady=6)

        # video file
        tk.Label(left, text="Video File to Search",
                 font=FONT_LABEL, bg=C_PANEL, fg=C_MUTED).pack(anchor="w", padx=16, pady=(10, 2))
        self.vid_path_var = tk.StringVar(value="No file selected")
        tk.Label(left, textvariable=self.vid_path_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_MUTED,
                 wraplength=280, anchor="w").pack(anchor="w", padx=16)
        styled_button(left, "Browse Video…", self._pick_vid,
                      color=C_ACCENT2, width=20).pack(anchor="w", padx=16, pady=6)

        separator(left)

        # threshold slider
        tk.Label(left, text="Confidence Threshold",
                 font=FONT_LABEL, bg=C_PANEL, fg=C_MUTED).pack(anchor="w", padx=16)
        self.thresh_var = tk.DoubleVar(value=0.75)
        thresh_row = tk.Frame(left, bg=C_PANEL)
        thresh_row.pack(fill="x", padx=16, pady=4)
        tk.Scale(thresh_row, variable=self.thresh_var,
                 from_=0.50, to=0.95, resolution=0.01,
                 orient="horizontal", bg=C_PANEL, fg=C_TEXT,
                 highlightthickness=0, troughcolor=C_BG,
                 activebackground=C_ACCENT2, length=200).pack(side="left")
        tk.Label(thresh_row, textvariable=self.thresh_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_HIGHLIGHT).pack(side="left", padx=8)

        # frame skip
        tk.Label(left, text="Process every N frames",
                 font=FONT_LABEL, bg=C_PANEL, fg=C_MUTED).pack(anchor="w", padx=16)
        self.skip_var = tk.IntVar(value=5)
        skip_row = tk.Frame(left, bg=C_PANEL)
        skip_row.pack(fill="x", padx=16, pady=4)
        for v in [3, 5, 10, 15]:
            tk.Radiobutton(skip_row, text=str(v), variable=self.skip_var, value=v,
                           font=FONT_LABEL, bg=C_PANEL, fg=C_TEXT,
                           selectcolor=C_BG, activebackground=C_PANEL).pack(side="left", padx=6)

        tk.Frame(left, bg=C_PANEL).pack(expand=True)
        self.run_btn = styled_button(left, "▶  START DETECTION",
                                     self._run_detection, color=C_ACCENT, width=24)
        self.run_btn.pack(pady=16)

        # ── right: output log
        right = tk.Frame(content, bg=C_PANEL,
                         highlightbackground=C_BORDER, highlightthickness=1)
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(right, text="DETECTION LOG", font=FONT_HEADING,
                 bg=C_PANEL, fg=C_ACCENT).pack(anchor="w", padx=16, pady=(14, 4))
        separator(right, pady=2)

        self.log_text = tk.Text(right, font=FONT_SMALL, bg=C_BG, fg=C_TEXT,
                                relief="flat", state="disabled",
                                insertbackground=C_TEXT, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.progress_var = tk.DoubleVar(value=0)
        ttk.Progressbar(right, variable=self.progress_var, maximum=100,
                        length=300).pack(fill="x", padx=10, pady=(0, 10))

        self._ref_path = None
        self._vid_path = None

    def _pick_ref(self):
        p = filedialog.askopenfilename(
            title="Select reference photo",
            filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if p:
            self._ref_path = p
            self.ref_path_var.set(os.path.basename(p))

    def _pick_vid(self):
        p = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[("Videos", "*.mp4 *.avi *.mov")])
        if p:
            self._vid_path = p
            self.vid_path_var.set(os.path.basename(p))

    def _log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _run_detection(self):
        if not self._ref_path:
            messagebox.showwarning("Missing Input", "Please select a reference photo.")
            return
        if not self._vid_path:
            messagebox.showwarning("Missing Input", "Please select a video file.")
            return

        self.run_btn.config(state="disabled", text="Processing…")
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        self.progress_var.set(0)

        def task():
            try:
                from detector import encode_reference_image
                from pipeline import process_video

                self._log(f"[+] Encoding reference: {os.path.basename(self._ref_path)}")
                embedding = encode_reference_image(self._ref_path)
                person_name = os.path.splitext(os.path.basename(self._ref_path))[0]
                ref_embeddings = {person_name: embedding}
                self._log(f"[+] Reference encoded successfully.")
                self._log(f"[+] Starting video scan: {os.path.basename(self._vid_path)}")
                self._log(f"    Threshold: {self.thresh_var.get():.2f}  |  Skip: every {self.skip_var.get()} frames\n")

                def progress(cur, total):
                    pct = (cur / total * 100) if total else 0
                    self.progress_var.set(pct)

                results = process_video(
                    self._vid_path,
                    ref_embeddings,
                    threshold=self.thresh_var.get(),
                    frame_skip=self.skip_var.get(),
                    progress_callback=progress,
                )

                self.progress_var.set(100)
                self._log(f"\n[✓] Scan complete — {len(results)} match(es) found.")
                for r in results:
                    self._log(f"    Frame {r['frame_number']:>5}  |  "
                              f"Confidence: {r['confidence']:.1%}  |  "
                              f"{r['timestamp']}")
                    self._log(f"    Snapshot: {r['snapshot_path']}")
            except Exception as ex:
                self._log(f"\n[ERROR] {ex}")
            finally:
                self.run_btn.config(state="normal", text="▶  START DETECTION")

        threading.Thread(target=task, daemon=True).start()

    def _build_topbar(self, title):
        _build_inner_topbar(self, title, self.app)


# ─────────────────────────────────────────────────────────────────────────────
# 5. WEBCAM SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class WebcamScreen(Screen):
    def build(self):
        self.configure(bg=C_BG)
        self._build_topbar("📷  Webcam Live Mode")

        content = tk.Frame(self, bg=C_BG)
        content.pack(fill="both", expand=True, padx=40, pady=20)

        # instructions card
        info = tk.Frame(content, bg=C_PANEL,
                        highlightbackground=C_BORDER, highlightthickness=1)
        info.pack(fill="x", pady=(0, 16))

        tk.Label(info, text="HOW TO USE", font=FONT_HEADING,
                 bg=C_PANEL, fg=C_ACCENT).pack(anchor="w", padx=16, pady=(12, 4))
        separator(info, pady=2)

        steps = [
            "1.  Select a clear, front-facing reference photo of the missing person.",
            "2.  Adjust the confidence threshold to control matching strictness.",
            "3.  Click  START WEBCAM  — an OpenCV window will open on your desktop.",
            "4.  Green bounding box = match found.   Red box = unrecognised face.",
            "5.  Press  Q  in the OpenCV window to end the session.",
            "6.  Matched frame snapshots are saved to  output/matched_frames/",
        ]
        for s in steps:
            tk.Label(info, text=s, font=FONT_BODY,
                     bg=C_PANEL, fg=C_TEXT, anchor="w").pack(fill="x", padx=24, pady=2)
        tk.Frame(info, height=10, bg=C_PANEL).pack()

        # controls card
        ctrl = tk.Frame(content, bg=C_PANEL,
                        highlightbackground=C_BORDER, highlightthickness=1)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="CONFIGURATION", font=FONT_HEADING,
                 bg=C_PANEL, fg=C_ACCENT2).pack(anchor="w", padx=16, pady=(12, 4))
        separator(ctrl, pady=2)

        row1 = tk.Frame(ctrl, bg=C_PANEL)
        row1.pack(fill="x", padx=20, pady=8)

        tk.Label(row1, text="Reference Photo:", font=FONT_LABEL,
                 bg=C_PANEL, fg=C_MUTED, width=18, anchor="w").pack(side="left")
        self.ref_path_var = tk.StringVar(value="No file selected")
        tk.Label(row1, textvariable=self.ref_path_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_TEXT).pack(side="left", padx=8)
        styled_button(row1, "Browse…", self._pick_ref,
                      color=C_ACCENT2, width=12).pack(side="left", padx=10)

        row2 = tk.Frame(ctrl, bg=C_PANEL)
        row2.pack(fill="x", padx=20, pady=8)

        tk.Label(row2, text="Confidence Threshold:", font=FONT_LABEL,
                 bg=C_PANEL, fg=C_MUTED, width=18, anchor="w").pack(side="left")
        self.thresh_var = tk.DoubleVar(value=0.75)
        tk.Scale(row2, variable=self.thresh_var,
                 from_=0.50, to=0.95, resolution=0.01,
                 orient="horizontal", bg=C_PANEL, fg=C_TEXT,
                 highlightthickness=0, troughcolor=C_BG,
                 activebackground=C_ACCENT, length=200).pack(side="left")
        tk.Label(row2, textvariable=self.thresh_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_HIGHLIGHT).pack(side="left", padx=8)

        tk.Frame(ctrl, height=6, bg=C_PANEL).pack()
        self.start_btn = styled_button(ctrl, "🎥  START WEBCAM",
                                       self._start_webcam, color=C_ACCENT, width=24)
        self.start_btn.pack(pady=14)

        self._ref_path = None

    def _pick_ref(self):
        p = filedialog.askopenfilename(
            title="Select reference photo",
            filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if p:
            self._ref_path = p
            self.ref_path_var.set(os.path.basename(p))

    def _start_webcam(self):
        if not self._ref_path:
            messagebox.showwarning("Missing Input", "Please select a reference photo.")
            return

        self.start_btn.config(state="disabled", text="Webcam running…")

        def task():
            try:
                from detector import encode_reference_image
                from pipeline import process_webcam
                embedding = encode_reference_image(self._ref_path)
                process_webcam(
                    {"Missing_Person": embedding},
                    threshold=self.thresh_var.get()
                )
            except Exception as ex:
                messagebox.showerror("Error", str(ex))
            finally:
                self.start_btn.config(state="normal", text="🎥  START WEBCAM")

        threading.Thread(target=task, daemon=True).start()

    def _build_topbar(self, title):
        _build_inner_topbar(self, title, self.app)


# ─────────────────────────────────────────────────────────────────────────────
# 6. EVALUATION SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class EvaluationScreen(Screen):
    def build(self):
        self.configure(bg=C_BG)
        self._build_topbar("📊  System Evaluation")

        content = tk.Frame(self, bg=C_BG)
        content.pack(fill="both", expand=True, padx=40, pady=20)

        # ── left: config
        left = tk.Frame(content, bg=C_PANEL,
                        highlightbackground=C_BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="EVALUATION SETUP", font=FONT_HEADING,
                 bg=C_PANEL, fg=C_HIGHLIGHT).pack(anchor="w", padx=16, pady=(14, 4))
        separator(left, pady=2)

        # same-person folder
        tk.Label(left, text="Same-Person Pairs Folder",
                 font=FONT_LABEL, bg=C_PANEL, fg=C_MUTED).pack(anchor="w", padx=16, pady=(10, 2))
        self.same_var = tk.StringVar(value="Not selected")
        tk.Label(left, textvariable=self.same_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_TEXT,
                 wraplength=260, anchor="w").pack(anchor="w", padx=16)
        styled_button(left, "Browse Folder…", self._pick_same,
                      color=C_HIGHLIGHT, width=20).pack(anchor="w", padx=16, pady=6)

        # diff-person folder
        tk.Label(left, text="Different-Person Pairs Folder",
                 font=FONT_LABEL, bg=C_PANEL, fg=C_MUTED).pack(anchor="w", padx=16, pady=(10, 2))
        self.diff_var = tk.StringVar(value="Not selected")
        tk.Label(left, textvariable=self.diff_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_TEXT,
                 wraplength=260, anchor="w").pack(anchor="w", padx=16)
        styled_button(left, "Browse Folder…", self._pick_diff,
                      color=C_HIGHLIGHT, width=20).pack(anchor="w", padx=16, pady=6)

        separator(left)

        # threshold
        tk.Label(left, text="Evaluation Threshold",
                 font=FONT_LABEL, bg=C_PANEL, fg=C_MUTED).pack(anchor="w", padx=16)
        self.thresh_var = tk.DoubleVar(value=0.75)
        trow = tk.Frame(left, bg=C_PANEL)
        trow.pack(fill="x", padx=16, pady=4)
        tk.Scale(trow, variable=self.thresh_var,
                 from_=0.50, to=0.95, resolution=0.01,
                 orient="horizontal", bg=C_PANEL, fg=C_TEXT,
                 highlightthickness=0, troughcolor=C_BG,
                 activebackground=C_HIGHLIGHT, length=200).pack(side="left")
        tk.Label(trow, textvariable=self.thresh_var,
                 font=FONT_SMALL, bg=C_PANEL, fg=C_HIGHLIGHT).pack(side="left", padx=8)

        tk.Frame(left, bg=C_PANEL).pack(expand=True)
        self.eval_btn = styled_button(left, "▶  RUN EVALUATION",
                                      self._run_eval, color=C_HIGHLIGHT, width=24)
        self.eval_btn.pack(pady=16)

        # ── right: results
        right = tk.Frame(content, bg=C_PANEL,
                         highlightbackground=C_BORDER, highlightthickness=1)
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(right, text="RESULTS", font=FONT_HEADING,
                 bg=C_PANEL, fg=C_ACCENT).pack(anchor="w", padx=16, pady=(14, 4))
        separator(right, pady=2)

        self.results_text = tk.Text(right, font=FONT_SMALL, bg=C_BG, fg=C_TEXT,
                                    relief="flat", state="disabled",
                                    insertbackground=C_TEXT, wrap="word")
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)

        self._same_folder = None
        self._diff_folder = None

    def _pick_same(self):
        p = filedialog.askdirectory(title="Select same-person pairs folder")
        if p:
            self._same_folder = p
            self.same_var.set(os.path.basename(p))

    def _pick_diff(self):
        p = filedialog.askdirectory(title="Select different-person pairs folder")
        if p:
            self._diff_folder = p
            self.diff_var.set(os.path.basename(p))

    def _log(self, msg):
        self.results_text.config(state="normal")
        self.results_text.insert("end", msg + "\n")
        self.results_text.see("end")
        self.results_text.config(state="disabled")

    def _run_eval(self):
        if not self._same_folder or not self._diff_folder:
            messagebox.showwarning("Missing Input",
                                   "Please select both same-person and different-person folders.")
            return

        self.eval_btn.config(state="disabled", text="Evaluating…")
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.config(state="disabled")

        def task():
            try:
                import glob
                from evaluator import evaluate_on_image_pairs

                def get_pairs(folder, label):
                    exts = ('*.jpg', '*.jpeg', '*.png')
                    files = []
                    for ext in exts:
                        files.extend(glob.glob(os.path.join(folder, ext)))
                    files = sorted(files)
                    pairs = []
                    for i in range(0, len(files) - 1, 2):
                        pairs.append({
                            "ref_path":  files[i],
                            "test_path": files[i + 1],
                            "label": label
                        })
                    return pairs

                test_pairs = get_pairs(self._same_folder, 1) + \
                             get_pairs(self._diff_folder, 0)
                self._log(f"[+] {len(test_pairs)} pairs loaded. Running evaluation…\n")

                metrics = evaluate_on_image_pairs(test_pairs,
                                                  threshold=self.thresh_var.get())
                if not metrics:
                    self._log("[!] No valid pairs could be processed.")
                    return

                lines = [
                    "=" * 44,
                    "         EVALUATION RESULTS",
                    "=" * 44,
                    f"  Threshold         : {metrics['threshold']}",
                    f"  Total pairs       : {metrics['total_pairs']}",
                    "-" * 44,
                    f"  Accuracy          : {metrics['accuracy']:.1%}",
                    f"  Precision         : {metrics['precision']:.1%}",
                    f"  Recall            : {metrics['recall']:.1%}",
                    f"  F1 Score          : {metrics['f1_score']:.1%}",
                    "-" * 44,
                    f"  False Accept Rate : {metrics['false_accept_rate_FAR']:.1%}",
                    f"  False Reject Rate : {metrics['false_reject_rate_FRR']:.1%}",
                    "-" * 44,
                    f"  TP={metrics['true_positives']}  TN={metrics['true_negatives']}  "
                    f"FP={metrics['false_positives']}  FN={metrics['false_negatives']}",
                    "-" * 44,
                    f"  Avg score (same)  : {metrics['avg_score_same_person']:.4f}",
                    f"  Avg score (diff)  : {metrics['avg_score_diff_person']:.4f}",
                    f"  Avg time/pair     : {metrics['avg_processing_time_ms']:.0f} ms",
                    "=" * 44,
                ]
                for line in lines:
                    self._log(line)

            except Exception as ex:
                self._log(f"\n[ERROR] {ex}")
            finally:
                self.eval_btn.config(state="normal", text="▶  RUN EVALUATION")

        threading.Thread(target=task, daemon=True).start()

    def _build_topbar(self, title):
        _build_inner_topbar(self, title, self.app)


# ─────────────────────────────────────────────────────────────────────────────
# SHARED INNER TOPBAR HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _build_inner_topbar(screen, title, app):
    topbar = tk.Frame(screen, bg=C_PANEL, height=52)
    topbar.pack(fill="x")
    topbar.pack_propagate(False)

    tk.Label(topbar, text=title,
             font=("Georgia", 13, "bold"),
             bg=C_PANEL, fg=C_HIGHLIGHT).pack(side="left", padx=20, pady=14)

    back = tk.Label(topbar, text="← Dashboard",
                    font=FONT_SMALL, bg=C_PANEL,
                    fg=C_ACCENT2, cursor="hand2")
    back.pack(side="right", padx=20, pady=14)
    back.bind("<Button-1>", lambda e: app.show_screen("dashboard"))

    tk.Frame(screen, bg=C_BORDER, height=1).pack(fill="x")


# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION CONTROLLER
# ─────────────────────────────────────────────────────────────────────────────

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lost Person Detection System")
        self.root.geometry("940x660")
        self.root.minsize(900, 620)
        self.root.configure(bg=C_BG)
        self.root.resizable(True, True)

        # Try to set window icon (skip silently if unavailable)
        try:
            self.root.iconbitmap("icon.ico")
        except Exception:
            pass

        self.current_user = None

        # Build all screens
        self.screens = {
            "splash":     SplashScreen(self.root, self),
            "login":      LoginScreen(self.root, self),
            "dashboard":  DashboardScreen(self.root, self),
            "video":      VideoScreen(self.root, self),
            "webcam":     WebcamScreen(self.root, self),
            "evaluation": EvaluationScreen(self.root, self),
        }

        self.active_screen = None
        self.show_screen("splash")

    def show_screen(self, name):
        if self.active_screen:
            self.screens[self.active_screen].hide()
        self.active_screen = name
        screen = self.screens[name]

        # Refresh dynamic content where needed
        if name == "dashboard" and hasattr(screen, "refresh_user"):
            screen.refresh_user()

        screen.show()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.current_user = None
            self.show_screen("splash")

    def run(self):
        self.root.mainloop()


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    App().run()  