"""Counter example showcasing key handling."""

import curses

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from simple_tui import SimpleTUI


class CounterTUI(SimpleTUI):
    """Use keyboard input to increment or decrement a counter."""

    def __init__(self) -> None:
        super().__init__(refresh_rate=0.1)
        self.count = 0

    def on_start(self) -> None:
        self.register_handlers(
            {
                ord("+"): self.increment,
                ord("="): self.increment,
                ord("-"): self.decrement,
                curses.KEY_UP: self.increment,
                curses.KEY_DOWN: self.decrement,
            }
        )

    def increment(self, _: int) -> None:
        self.count += 1

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
