"""Minimal hello world example using SimpleTUI."""

from simple_tui import SimpleTUI


class HelloWorldTUI(SimpleTUI):
    """Render a static greeting to introduce the framework."""

    def draw(self) -> None:
        self.clear()
        self.addstr(0, 0, "Hello, TUI world! Press 'q' to exit.")
        self.refresh()


if __name__ == "__main__":
    HelloWorldTUI().run()
