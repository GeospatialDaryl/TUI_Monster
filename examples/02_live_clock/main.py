"""Live clock example demonstrating state updates."""

from datetime import datetime

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pyTuiMonster import TuiConfig, TuiMonsterApp


class LiveClockTUI(TuiMonsterApp):
    """Render the current time and refresh every frame."""

    def __init__(self) -> None:
        super().__init__(TuiConfig(refresh_rate=0.5))
        self.current_time: str = ""

    def update(self) -> None:
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def draw(self) -> None:
        self.clear()
        self.addstr(0, 0, "Live Clock")
        self.addstr(2, 0, f"Current time: {self.current_time}")
        self.addstr(4, 0, "Press 'q' to quit.")
        self.refresh()


if __name__ == "__main__":
    LiveClockTUI().run()
