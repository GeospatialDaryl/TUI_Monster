"""Dev example 02 — multi-step task pipeline with per-step status indicators.

Run:
    python implementation/dev_examples/02_progress_tracker/main.py

Demonstrates:
- Extending TuiMonsterApp for a custom pipeline view
- Threading a background task list while rendering live status
- Per-step OK / FAIL / RUNNING badges with color pairs
- Lifecycle hook for initialization
"""

from __future__ import annotations

import curses
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from pyTuiMonster import TuiMonsterApp, TuiConfig, lifecycle_hook

_CP_OK = 1
_CP_FAIL = 2
_CP_RUNNING = 3
_CP_PENDING = 4
_CP_HEADER = 5
_CP_FOOTER = 6


@dataclass
class Step:
    label: str
    fn: Callable[[], bool]   # return True on success
    status: str = "pending"  # pending | running | ok | fail
    message: str = ""


class ProgressTrackerApp(TuiMonsterApp):
    """Display a pipeline of named steps with live status updates."""

    def __init__(self, title: str, steps: List[Step]) -> None:
        super().__init__(TuiConfig(refresh_rate=1 / 10))
        self._title = title
        self._steps = steps
        self._thread: Optional[threading.Thread] = None
        self._done = False
        self._elapsed = 0.0
        self._start_time: Optional[float] = None

    @lifecycle_hook("after_start")
    def _init_colors(self) -> None:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(_CP_OK, curses.COLOR_GREEN, -1)
        curses.init_pair(_CP_FAIL, curses.COLOR_RED, -1)
        curses.init_pair(_CP_RUNNING, curses.COLOR_YELLOW, -1)
        curses.init_pair(_CP_PENDING, curses.COLOR_WHITE, -1)
        curses.init_pair(_CP_HEADER, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(_CP_FOOTER, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.curs_set(0)

    @lifecycle_hook("after_start")
    def _start_pipeline(self) -> None:
        self._start_time = time.monotonic()
        self._thread = threading.Thread(target=self._run_pipeline, daemon=True)
        self._thread.start()

    def _run_pipeline(self) -> None:
        for step in self._steps:
            step.status = "running"
            try:
                ok = step.fn()
                step.status = "ok" if ok else "fail"
            except Exception as exc:
                step.status = "fail"
                step.message = str(exc)
        self._done = True

    def update(self) -> None:
        if self._start_time is not None:
            self._elapsed = time.monotonic() - self._start_time
        if self._done and self._thread and not self._thread.is_alive():
            # Give user a moment to see the final state before auto-quit
            pass  # user presses q to exit

    def draw(self) -> None:
        self.clear()
        h, w = self.screen.getmaxyx()

        # Header
        self.addstr(0, 0, " " * w, curses.color_pair(_CP_HEADER) | curses.A_BOLD)
        self.addstr(0, 2, f"{self._title}   {self._elapsed:.1f}s",
                    curses.color_pair(_CP_HEADER) | curses.A_BOLD)

        # Steps
        for i, step in enumerate(self._steps):
            row = 2 + i
            if row >= h - 2:
                break
            badge, attr = self._badge(step.status)
            self.addstr(row, 2, badge, attr | curses.A_BOLD)
            label = f"  {step.label}"
            if step.message:
                label += f"  — {step.message}"
            self.addstr(row, 2 + len(badge), label[:w - len(badge) - 4])

        # Summary row
        if self._done:
            fails = sum(1 for s in self._steps if s.status == "fail")
            summary = "All steps passed!" if fails == 0 else f"{fails} step(s) failed."
            attr = curses.color_pair(_CP_OK) if fails == 0 else curses.color_pair(_CP_FAIL)
            self.center_text(h - 3, summary, attr | curses.A_BOLD)

        # Footer
        self.addstr(h - 1, 0, " " * w, curses.color_pair(_CP_FOOTER))
        self.addstr(h - 1, 2, "q quit", curses.color_pair(_CP_FOOTER))
        self.refresh()

    @staticmethod
    def _badge(status: str) -> tuple[str, int]:
        mapping = {
            "pending": ("○ PENDING", curses.color_pair(_CP_PENDING)),
            "running": ("● RUNNING", curses.color_pair(_CP_RUNNING)),
            "ok":      ("✓ OK     ", curses.color_pair(_CP_OK)),
            "fail":    ("✗ FAIL   ", curses.color_pair(_CP_FAIL)),
        }
        return mapping.get(status, ("? UNKNOWN", curses.A_NORMAL))


# ---------------------------------------------------------------------------

def _fake_step(label: str, duration: float, succeed: bool = True) -> Step:
    def fn() -> bool:
        time.sleep(duration)
        return succeed
    return Step(label=label, fn=fn)


def main() -> None:
    steps = [
        _fake_step("Check environment", 0.4),
        _fake_step("Install dependencies", 0.8),
        _fake_step("Compile sources", 1.2),
        _fake_step("Run unit tests", 0.6),
        _fake_step("Bundle artifacts", 0.5),
        _fake_step("Verify checksums", 0.3),
        _fake_step("Deploy to staging", 1.0),
    ]
    ProgressTrackerApp(title="Pipeline: example build", steps=steps).run()


if __name__ == "__main__":
    main()
