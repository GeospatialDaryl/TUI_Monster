"""Counter example showcasing key handling."""

import sys
from pathlib import Path

import curses

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pyTuiMonster import TuiConfig, TuiMonsterApp, key_binding


class CounterTUI(TuiMonsterApp):
    """Use keyboard input to increment or decrement a counter."""

    def __init__(self) -> None:
        super().__init__(TuiConfig(refresh_rate=0.1))
        self.count = 0

    @key_binding(ord("+"), ord("="), curses.KEY_UP)
    def increment(self, _: int) -> None:
        self.count += 1

    @key_binding(ord("-"), curses.KEY_DOWN)
    def decrement(self, _: int) -> None:
        self.count -= 1

    def draw(self) -> None:
        self.clear()
        self.addstr(0, 0, "Counter")
        self.addstr(2, 0, f"Current value: {self.count}")
        self.addstr(4, 0, "Press '+' or Up to increment.")
        self.addstr(5, 0, "Press '-' or Down to decrement.")
        self.addstr(7, 0, "Press 'q' to quit.")
        self.refresh()


if __name__ == "__main__":
    CounterTUI().run()
