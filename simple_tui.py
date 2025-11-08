"""A general purpose TUI helper based on the btopper framework structure.

This module provides a :class:`SimpleTUI` class that mirrors the high level
structure used by the btopper TUI implementation.  It manages initialization,
input handling, drawing and update loops while remaining lightweight enough to
be used as a starting point for new projects.

Example
-------

>>> class Demo(SimpleTUI):
...     def draw(self):
...         self.clear()
...         self.addstr(0, 0, "Hello from TUI_Monster!")
...         self.refresh()
...
... Demo().run()

The example above will start a curses driven UI that repeatedly draws the
string while keeping the event loop alive.
"""

from __future__ import annotations

import curses
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional


KeyHandler = Callable[[int], None]


@dataclass
class SimpleTUI:
    """A minimal TUI manager inspired by the btopper architecture.

    Parameters
    ----------
    refresh_rate:
        Number of seconds to wait between frames.  A smaller value will update
        the interface more frequently at the cost of higher CPU usage.
    key_handlers:
        Mapping of key codes to callback functions that should be executed when
        the key is pressed.
    """

    refresh_rate: float = 1 / 30
    key_handlers: Dict[int, KeyHandler] = field(default_factory=dict)

    _stdscr: Optional[curses.window] = field(init=False, default=None)
    _running: bool = field(init=False, default=False)

    def run(self) -> None:
        """Start the TUI event loop."""

        curses.wrapper(self._main)

    # ------------------------------------------------------------------
    # Lifecycle hooks
    # ------------------------------------------------------------------
    def on_start(self) -> None:
        """Hook executed once before the main loop begins.

        Subclasses can override this to perform initialization that requires a
        fully configured curses window.
        """

    def update(self) -> None:
        """Update application state.

        Override this method to keep track of dynamic information such as
        refreshing metrics or reading from background tasks.
        """

    def draw(self) -> None:
        """Render the current frame to the screen.

        Subclasses must override this to present output to the user.  The
        default implementation clears the screen to avoid leaving stale
        contents visible.
        """

        self.clear()
        self.refresh()

    def on_stop(self) -> None:
        """Hook executed just before the application exits."""

    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def register_handlers(self, handlers: Dict[int, KeyHandler]) -> None:
        """Register additional key handlers.

        Parameters
        ----------
        handlers:
            Mapping between curses key codes and callables.  The callables are
            invoked with the pressed key and can raise :class:`StopIteration`
            to signal that the main loop should exit.
        """

        self.key_handlers.update(handlers)

    def handle_input(self) -> None:
        """Read user input and trigger registered handlers."""

        if self._stdscr is None:
            return

        try:
            key = self._stdscr.getch()
        except curses.error:
            # Non blocking read with no input available.
            return

        if key == -1:
            return

        handler = self.key_handlers.get(key)
        if handler is not None:
            handler(key)
        elif key in (ord("q"), curses.KEY_EXIT):
            self.stop()

    # ------------------------------------------------------------------
    # Utility helpers mirroring btopper convenience APIs
    # ------------------------------------------------------------------
    def clear(self) -> None:
        if self._stdscr is not None:
            self._stdscr.erase()

    def refresh(self) -> None:
        if self._stdscr is not None:
            self._stdscr.noutrefresh()
            curses.doupdate()

    def addstr(self, y: int, x: int, text: str, attr: int | None = None) -> None:
        if self._stdscr is None:
            return

        if attr is None:
            self._stdscr.addnstr(y, x, text, len(text))
        else:
            self._stdscr.addnstr(y, x, text, len(text), attr)

    # ------------------------------------------------------------------
    # Internal logic
    # ------------------------------------------------------------------
    def _main(self, stdscr: curses.window) -> None:
        self._stdscr = stdscr
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)
        stdscr.timeout(0)

        self._running = True
        self.on_start()

        try:
            while self._running:
                self.handle_input()
                self.update()
                self.draw()
                time.sleep(max(self.refresh_rate, 0))
        finally:
            self.on_stop()
            self._stdscr = None
            self._running = False

    def stop(self) -> None:
        """Request that the main loop stops running."""

        self._running = False


__all__ = ["SimpleTUI", "KeyHandler"]
