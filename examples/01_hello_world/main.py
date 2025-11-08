"""Minimal hello world example using :class:`pyTuiMonster.TuiMonsterApp`."""

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pyTuiMonster import TuiMonsterApp


class HelloWorldTUI(TuiMonsterApp):
    """Render a static greeting to introduce the framework."""

    def draw(self) -> None:
        self.clear()
        self.addstr(0, 0, "Hello, TUI world! Press 'q' to exit.")
        self.refresh()


if __name__ == "__main__":
    HelloWorldTUI().run()
