"""Core event loop implementation for pyTuiMonster."""

from __future__ import annotations

import curses
import unicodedata
from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Callable, ClassVar, Dict, Mapping, Optional

from .config import TuiConfig
from .decorators import ALL_LIFECYCLE_STAGES, LifecycleStage

KeyHandler = Callable[[int], None]


def _char_width(char: str) -> int:
    """Return the approximate terminal cell width for a single character.

    The standard library does not expose wcwidth, but accounting for combining
    marks and East Asian wide/full-width characters is a practical improvement
    over ``len`` for curses layouts that include emoji, CJK, and other glyphs.
    """

    if unicodedata.combining(char):
        return 0
    return 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1


def _display_width(text: str) -> int:
    """Return the approximate terminal cell width for ``text``."""

    return sum(_char_width(char) for char in text)


class TuiMonsterApp(ABC):
    """A modernized curses application harness inspired by btop++."""

    _declared_key_bindings: ClassVar[Dict[int, str]] = {}
    _declared_hooks: ClassVar[Dict[LifecycleStage, tuple[str, ...]]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        key_bindings: Dict[int, str] = {}
        hooks: Dict[LifecycleStage, list[str]] = {stage: [] for stage in ALL_LIFECYCLE_STAGES}

        for base in reversed(cls.__mro__[1:]):
            key_bindings.update(getattr(base, "_declared_key_bindings", {}))
            for stage, names in getattr(base, "_declared_hooks", {}).items():
                hooks[stage].extend(name for name in names if name not in hooks[stage])

        local_keys: Dict[int, str] = {}
        for name, value in cls.__dict__.items():
            keys = getattr(value, "_tui_monster_keys", None)
            if keys:
                for key in keys:
                    if key in local_keys:
                        first = local_keys[key]
                        raise ValueError(
                            f"Duplicate key binding {key!r} on {cls.__name__}: "
                            f"{first!r} and {name!r}"
                        )
                    local_keys[key] = name
                    key_bindings[key] = name
            stage = getattr(value, "_tui_monster_stage", None)
            if stage:
                if stage not in ALL_LIFECYCLE_STAGES:
                    supported = ", ".join(ALL_LIFECYCLE_STAGES)
                    raise ValueError(
                        f"Unsupported lifecycle stage {stage!r}; expected one of: {supported}"
                    )
                if name not in hooks[stage]:
                    hooks[stage].append(name)

        cls._declared_key_bindings = key_bindings
        cls._declared_hooks = {
            stage: tuple(names) for stage, names in hooks.items() if names
        }

    def __init__(self, config: Optional[TuiConfig] = None) -> None:
        self.config = config or TuiConfig()
        self._stdscr: Optional[curses.window] = None
        self._running = False
        self._key_handlers: Dict[int, KeyHandler] = {
            key: getattr(self, name) for key, name in self._declared_key_bindings.items()
        }

    @property
    def screen(self) -> curses.window:
        if self._stdscr is None:
            raise RuntimeError("Screen is not initialized outside of run().")
        return self._stdscr

    @property
    def running(self) -> bool:
        return self._running

    @property
    def keymap(self) -> MappingProxyType[int, KeyHandler]:
        return MappingProxyType(self._key_handlers)

    def run(self) -> None:
        curses.wrapper(self._main)

    def stop(self) -> None:
        self._running = False

    def register_key_handler(self, key: int, handler: KeyHandler) -> None:
        """Register ``handler`` for ``key`` at runtime.

        Keys listed in :attr:`TuiConfig.stop_keys` are checked before
        registered handlers, so registering a handler for a configured stop
        key has no effect while that key remains a stop key. A handler may
        raise :class:`StopIteration` to stop the application.
        """

        if not isinstance(key, int):
            raise TypeError("key handler keys must be integers")
        self._key_handlers[key] = handler

    def register_key_handlers(self, handlers: Mapping[int, KeyHandler]) -> None:
        for key, handler in handlers.items():
            self.register_key_handler(key, handler)

    @abstractmethod
    def draw(self) -> None:
        """Render the interface."""

    def update(self) -> None:
        """Refresh internal state before drawing."""

    def on_start(self) -> None:
        """Hook executed once before entering the main loop."""

    def on_stop(self) -> None:
        """Hook executed once before leaving curses context."""

    def clear(self) -> None:
        if self._stdscr is not None:
            self._stdscr.erase()

    def refresh(self) -> None:
        if self._stdscr is not None:
            self._stdscr.noutrefresh()
            curses.doupdate()

    def addstr(self, y: int, x: int, text: str, attr: Optional[int] = None) -> bool:
        """Safely add text to the screen.

        Returns ``True`` when text was written and ``False`` when the screen is
        unavailable, the coordinates are outside the current terminal bounds, or
        curses rejects the write. Silent failure mirrors the previous no-op
        behavior while preventing narrow-terminal crashes.
        """

        if self._stdscr is None:
            return False
        max_y, max_x = self._stdscr.getmaxyx()
        if y < 0 or y >= max_y or x < 0 or x >= max_x:
            return False
        available_width = max_x - x
        if available_width <= 0:
            return False
        truncated = self._truncate_to_width(text, available_width)
        if not truncated:
            return False
        try:
            if attr is None:
                self._stdscr.addnstr(y, x, truncated, len(truncated))
            else:
                self._stdscr.addnstr(y, x, truncated, len(truncated), attr)
        except curses.error:
            return False
        return True

    @property
    def _frame_timeout_ms(self) -> int:
        return max(int(self.config.refresh_rate * 1000), 0)

    def _main(self, stdscr: curses.window) -> None:
        self._stdscr = stdscr
        try:
            curses.curs_set(0)
        except curses.error:
            pass
        stdscr.keypad(True)
        stdscr.timeout(self._frame_timeout_ms)

        self._running = True
        self._run_stage("before_start")
        self.on_start()
        self._run_stage("after_start")

        try:
            while self._running:
                self._process_input()

                self._run_stage("before_update")
                self.update()
                self._run_stage("after_update")

                self._run_stage("before_draw")
                self.draw()
                self._run_stage("after_draw")
        finally:
            self._run_stage("before_stop")
            self.on_stop()
            self._run_stage("after_stop")
            self._stdscr = None
            self._running = False

    def _run_stage(self, stage: LifecycleStage) -> None:
        for name in self._declared_hooks.get(stage, ()):  # type: ignore[arg-type]
            getattr(self, name)()

    def _process_input(self) -> None:
        """Handle pending input, waiting up to one frame interval.

        The first ``getch`` call blocks for at most ``config.refresh_rate``
        seconds and paces the main loop, so a keypress wakes the loop
        immediately instead of waiting out a sleep. Any further buffered keys
        are drained without waiting. With a ``refresh_rate`` of ``0`` the
        read never blocks and the loop runs as fast as possible.
        """

        if self._stdscr is None:
            return
        draining = False
        try:
            while self._running:
                try:
                    key = self._stdscr.getch()
                except curses.error:
                    return
                if not draining:
                    self._stdscr.timeout(0)
                    draining = True
                if key == -1:
                    return
                if key in self.config.stop_keys:
                    self.stop()
                    return
                handler = self._key_handlers.get(key)
                if handler is not None:
                    try:
                        handler(key)
                    except StopIteration:
                        self.stop()
                        return
        finally:
            if draining and self._stdscr is not None:
                self._stdscr.timeout(self._frame_timeout_ms)

    def _truncate_to_width(self, text: str, max_width: int) -> str:
        if max_width <= 0:
            return ""
        width = 0
        chars: list[str] = []
        for char in text:
            char_width = _char_width(char)
            if width + char_width > max_width:
                break
            chars.append(char)
            width += char_width
        return "".join(chars)

    def center_text(self, y: int, text: str, attr: Optional[int] = None) -> bool:
        """Center text on the current screen using approximate display width."""

        if self._stdscr is None:
            return False
        max_y, max_x = self._stdscr.getmaxyx()
        if y < 0 or y >= max_y:
            return False
        x = max((max_x - _display_width(text)) // 2, 0)
        return self.addstr(y, x, text, attr)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config!r})"


__all__ = ["TuiMonsterApp", "KeyHandler"]
