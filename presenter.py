import subprocess
import sys
import os


class Presenter:
    """Connects Model and View and drives timer ticks via root.after."""

    def __init__(self, model, view, root):
        self.model = model
        self.view = view
        self.root = root
        self._after_id = None

        # Bind view events
        self.view.bind_start(self.on_start)
        self.view.bind_pause(self.on_pause)
        self.view.bind_reset(self.on_reset)
        self.view.bind_duration_change(self.on_duration_change)

        # Initial UI sync
        self._sync_view()

    def on_start(self):
        self.model.start()
        self._sync_view()
        self._schedule_tick()

    def on_pause(self):
        self.model.pause()
        self._cancel_tick()
        self._sync_view()

    def on_reset(self):
        self.model.reset()
        self._cancel_tick()
        self._sync_view()

    def on_duration_change(self, work_min: int, break_min: int):
        self.model.set_durations(work_min, break_min)
        self._sync_view()

    def _schedule_tick(self):
        if self._after_id is None:
            self._after_id = self.root.after(1000, self._on_tick)

    def _cancel_tick(self):
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _on_tick(self):
        self._after_id = None
        ended = self.model.tick()
        self._sync_view()
        if self.model.running:
            self._schedule_tick()
        if ended:
            # Timer reached zero.
            self._play_chime()
            try:
                self.view.show_notification("Session ended. Press Start to begin next session.")
            except Exception:
                pass

    def _sync_view(self):
        self.view.set_timer_display(self.model.get_time_mmss())
        self.view.set_mode(self.model.mode)
        # Controls: start enabled when not running and time remains, pause enabled when running
        self.view.set_controls(start_enabled=not self.model.running and self.model.seconds_remaining > 0,
                               pause_enabled=self.model.running,
                               reset_enabled=True)
        # Always set arc start to -90 (top)
        try:
            self.view.set_arc_start(90)
        except Exception:
            pass
        # Update circular progress
        try:
            frac = self.model.progress_fraction()
        except Exception:
            frac = 0.0
        try:
            self.view.set_progress(frac)
        except Exception:
            pass

    def _play_chime(self):
        # Try to play a bundled chime in resources/chime.wav, fallback to system beep
        try:
            base = os.path.dirname(sys.argv[0]) or os.getcwd()
            path = os.path.join(base, "resources", "chime.wav")
            if os.path.exists(path):
                if sys.platform == "darwin":
                    subprocess.run(["afplay", path], check=False)
                    return
                if sys.platform == "win32":
                    try:
                        import winsound

                        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        return
                    except Exception:
                        pass
                else:
                    try:
                        import playsound

                        playsound.playsound(path, block=False)
                        return
                    except Exception:
                        pass
            try:
                self.root.bell()
            except Exception:
                pass
        except Exception:
            try:
                self.root.bell()
            except Exception:
                pass