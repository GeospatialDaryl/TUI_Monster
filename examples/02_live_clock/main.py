"""Live clock example demonstrating state updates."""

from datetime import datetime

from simple_tui import SimpleTUI


class LiveClockTUI(SimpleTUI):
    """Render the current time and refresh every frame."""

    def __init__(self) -> None:
        super().__init__(refresh_rate=0.5)
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
