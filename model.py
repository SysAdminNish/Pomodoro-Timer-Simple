class Model:
    """Encapsulates Pomodoro timer state and durations."""
    def __init__(self, work_minutes: int = 25, break_minutes: int = 5):
        self.work_minutes = int(work_minutes)
        self.break_minutes = int(break_minutes)
        self.mode = "work"  # 'work' or 'break'
        self.running = False
        self.seconds_remaining = self.work_minutes * 60

    def set_durations(self, work_minutes: int, break_minutes: int):
        self.work_minutes = int(work_minutes)
        self.break_minutes = int(break_minutes)
        # If not running, update the visible remaining seconds to the selected durations
        if not self.running:
            self.seconds_remaining = (self.work_minutes * 60) if self.mode == "work" else (self.break_minutes * 60)

    def start(self):
        if not self.running:
            self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.seconds_remaining = (self.work_minutes * 60) if self.mode == "work" else (self.break_minutes * 60)

    def tick(self) -> bool:
        """Advance timer by one second. Returns True if timer reached zero on this tick."""
        if not self.running:
            return False
        if self.seconds_remaining > 0:
            self.seconds_remaining -= 1
        if self.seconds_remaining <= 0:
            # timer finished
            self.running = False
            self.seconds_remaining = 0
            return True
        return False

    def switch_mode(self, mode: str):
        """Switch mode without starting the timer. mode should be 'work' or 'break'."""
        if mode not in ("work", "break"):
            return
        self.mode = mode
        self.seconds_remaining = (self.work_minutes * 60) if self.mode == "work" else (self.break_minutes * 60)

    def get_time_mmss(self) -> str:
        m, s = divmod(int(self.seconds_remaining), 60)
        return f"{m:02d}:{s:02d}"

    def total_seconds(self) -> int:
        """Return the total seconds for the current mode."""
        return (self.work_minutes * 60) if self.mode == "work" else (self.break_minutes * 60)

    def progress_fraction(self) -> float:
        """Return fraction completed (0.0-1.0)."""
        total = self.total_seconds()
        if total <= 0:
            return 0.0
        return max(0.0, min(1.0, (total - self.seconds_remaining) / total))