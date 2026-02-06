
import tkinter as tk
from tkinter import ttk, messagebox
import json
import random


class View:
    """Tkinter UI with a circular progress ring and larger, professional layout."""

    # Palette / color constants
    BG = "#FFFFFF"
    PANEL = "#F3F4F6"
    TEXT = "#222222"
    ACCENT = "#1E3A8A"  # Navy blue

    # New dark header / panel colors and toast
    HEADER_BG = "#0F172A"
    BADGE_BG = "#FFFFFF"
    PANEL_DARK = "#EEEEEE"  # Light grey for controls area
    TEXT_LIGHT = "#FFFFFF"
    TOAST_BG = "#111827"
    TOAST_FG = "#FFFFFF"

    def __init__(self, root, width=520, height=760):
        self.root = root
        self.width = width
        self.height = height
        self.start_callback = None
        self.pause_callback = None
        self.reset_callback = None
        self.duration_callback = None
        self._arc = None
        self._arc_start = -90
        self.quotes = self._load_quotes()
        self.current_quote = random.choice(self.quotes) if self.quotes else "Focus Time"
        self._build_ui()

    def _load_quotes(self):
        try:
            with open("pomodoro_quotes.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return ["Focus Time"]

    def _build_ui(self):
        self.root.title("Pomodoro")
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)

        # Set window size and center
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = max(0, (screen_w - self.width) // 2)
        y = max(0, (screen_h - self.height) // 3)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Header dark bar with white text
        header = tk.Frame(self.root, bg=self.HEADER_BG, height=72)
        header.pack(fill="x", side="top")
        badge = tk.Label(header, text="Pomodoro", bg=self.HEADER_BG, fg="#FFFFFF",
                         font=(None, 16, "bold"), padx=14, pady=6)
        badge.place(relx=0.5, rely=0.5, anchor="center")

        # Main container below header
        self.container = tk.Frame(self.root, bg=self.BG)
        self.container.place(relx=0.5, x=0, y=96, anchor="n")

        # Quote of the day label (bold)
        self.quote_title_label = tk.Label(self.container, text="Quote of the day:", font=(None, 12, "bold"), bg=self.BG, fg=self.TEXT)
        self.quote_title_label.pack(pady=(6, 2))

        # Mode label (now shows random quote in italics)
        self.mode_label = tk.Label(self.container, text=self.current_quote, font=(None, 12, "italic"), bg=self.BG, fg=self.TEXT, wraplength=420, justify="center")
        self.mode_label.pack(pady=(0, 0))

        # Canvas for circular progress
        canvas_size = 520 - 80
        self.canvas = tk.Canvas(self.container, width=canvas_size, height=canvas_size, bg=self.BG, highlightthickness=0)
        self.canvas.pack(pady=10)

        pad = 22
        self._oval_bbox = (pad, pad, canvas_size - pad, canvas_size - pad)

        # Background ring
        self.canvas.create_oval(self._oval_bbox, outline="#E6E7EA", width=14)

        # Progress arc: start at top (-90). We'll animate start via presenter.
        self._arc = self.canvas.create_arc(self._oval_bbox, start=self._arc_start, extent=0, style="arc",
                                           outline=self.ACCENT, width=14)

        # Timer text in center
        self.timer_text = self.canvas.create_text(canvas_size // 2, canvas_size // 2, text="25:00", fill=self.TEXT,
                                                  font=(None, 56, "bold"))

        # Bottom controls: light grey panel with rounded corners
        bottom = tk.Frame(self.root, bg=self.PANEL_DARK, highlightthickness=0)
        bottom.place(relx=0.5, rely=0.88, anchor="s")

        durations = tk.Frame(bottom, bg=self.PANEL_DARK)
        durations.grid(row=0, column=0, pady=(8, 6))

        lbl_work = tk.Label(durations, text="Work:", bg=self.PANEL_DARK, fg=self.TEXT, font=(None, 9, "bold"))
        lbl_work.grid(row=0, column=0, sticky=tk.E)
        self.work_spin = tk.Spinbox(durations, from_=1, to=180, width=4, justify="center",
                                    bg="#FFFFFF", fg=self.TEXT, insertbackground=self.TEXT,
                                    relief="solid", borderwidth=1, highlightthickness=0)
        self.work_spin.delete(0, tk.END)
        self.work_spin.insert(0, "25")
        self.work_spin.grid(row=0, column=1, padx=(6, 12))

        lbl_break = tk.Label(durations, text="Break:", bg=self.PANEL_DARK, fg=self.TEXT, font=(None, 9, "bold"))
        lbl_break.grid(row=0, column=2, sticky=tk.E)
        self.break_spin = tk.Spinbox(durations, from_=1, to=60, width=4, justify="center",
                                     bg="#FFFFFF", fg=self.TEXT, insertbackground=self.TEXT,
                                     relief="solid", borderwidth=1, highlightthickness=0)
        self.break_spin.delete(0, tk.END)
        self.break_spin.insert(0, "5")
        self.break_spin.grid(row=0, column=3, padx=(6, 0))

        # Large control buttons (styled)
        controls = tk.Frame(bottom, bg=self.PANEL_DARK)
        controls.grid(row=1, column=0, pady=(6, 8))

        self.start_btn = tk.Button(controls, text="Start", bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#FFFFFF",
                                   padx=16, pady=8, relief="flat", font=(None, 10, "bold"))
        self.start_btn.grid(row=0, column=0, padx=10)

        self.pause_btn = tk.Button(controls, text="Pause", bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#FFFFFF",
                                   padx=16, pady=8, relief="solid", borderwidth=2, font=(None, 10, "bold"))
        self.pause_btn.grid(row=0, column=1, padx=10)

        self.reset_btn = tk.Button(controls, text="Reset", bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#FFFFFF",
                                   padx=16, pady=8, relief="solid", borderwidth=2, font=(None, 10, "bold"))
        self.reset_btn.grid(row=0, column=2, padx=10)

        # Bind buttons
        self.start_btn.configure(command=self._on_start)
        self.pause_btn.configure(command=self._on_pause)
        self.reset_btn.configure(command=self._on_reset)

        # Duration changes
        self.work_spin.bind("<FocusOut>", self._on_duration_change_event)
        self.break_spin.bind("<FocusOut>", self._on_duration_change_event)
        self.work_spin.bind("<Return>", self._on_duration_change_event)
        self.break_spin.bind("<Return>", self._on_duration_change_event)

    def _on_start(self):
        if self.start_callback:
            self.start_callback()

    def _on_pause(self):
        if self.pause_callback:
            self.pause_callback()

    def _on_reset(self):
        if self.reset_callback:
            self.reset_callback()

    def _on_duration_change_event(self, event=None):
        if self.duration_callback:
            try:
                w = int(self.work_spin.get())
            except Exception:
                w = 25
            try:
                b = int(self.break_spin.get())
            except Exception:
                b = 5
            self.duration_callback(w, b)

    # Binding helpers
    def bind_start(self, cb):
        self.start_callback = cb

    def bind_pause(self, cb):
        self.pause_callback = cb

    def bind_reset(self, cb):
        self.reset_callback = cb

    def bind_duration_change(self, cb):
        self.duration_callback = cb

    # UI update methods
    def set_timer_display(self, text: str):
        self.canvas.itemconfigure(self.timer_text, text=text)

    def set_mode(self, mode: str):
        # Do not change quote on mode switch; keep the quote shown until app restart
        self.mode_label.config(text=self.current_quote)

    def set_controls(self, *, start_enabled: bool, pause_enabled: bool, reset_enabled: bool):
        self.start_btn.config(state=(tk.NORMAL if start_enabled else tk.DISABLED))
        self.pause_btn.config(state=(tk.NORMAL if pause_enabled else tk.DISABLED))
        self.reset_btn.config(state=(tk.NORMAL if reset_enabled else tk.DISABLED))

    def set_arc_start(self, angle: float):
        """Set the arc start angle (degrees). Presenter will call this to animate rotation."""
        try:
            self._arc_start = angle
            self.canvas.itemconfigure(self._arc, start=self._arc_start)
        except Exception:
            pass

    def set_progress(self, fraction: float):
        """fraction: 0.0 - 1.0; updates the arc extent.
        Draws anticlockwise from top (start = -90)."""
        frac = max(0.0, min(1.0, float(fraction) if fraction is not None else 0.0))
        extent = -360 * frac  # negative extent draws anticlockwise from the start angle
        try:
            self.canvas.itemconfigure(self._arc, extent=extent)
        except Exception:
            pass

    def show_notification(self, text: str):
        """Non-blocking transient toast (Toplevel) that auto-destroys after 2.5s."""
        try:
            toast = tk.Toplevel(self.root)
            toast.overrideredirect(True)
            toast.attributes("-topmost", True)
            toast.configure(bg=self.TOAST_BG)

            label = tk.Label(toast, text=text, bg=self.TOAST_BG, fg=self.TOAST_FG, padx=12, pady=8)
            label.pack()

            # Position the toast centered near top of the app window
            self.root.update_idletasks()
            root_x = self.root.winfo_rootx()
            root_y = self.root.winfo_rooty()
            root_w = self.root.winfo_width()
            x = root_x + (root_w // 2) - (toast.winfo_reqwidth() // 2)
            y = root_y + 80
            toast.geometry(f"+{x}+{y}")

            # Auto destroy after 2500ms (2.5s)
            toast.after(2500, toast.destroy)
        except Exception:
            try:
                self.root.bell()
            except Exception:
                pass