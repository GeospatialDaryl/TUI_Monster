"""Core event loop implementation for pyTuiMonster."""

from __future__ import annotations

import curses
import time
from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Callable, ClassVar, Dict, Optional

from .config import TuiConfig
from .decorators import LifecycleStage

KeyHandler = Callable[[int], None]
_ALL_STAGES: tuple[LifecycleStage, ...] = (
    "before_start",
    "after_start",
    "before_update",
    "after_update",
    "before_draw",
    "after_draw",
    "before_stop",
    "after_stop",
)


class TuiMonsterApp(ABC):
    """A modernized curses application harness inspired by btopper."""

    _declared_key_bindings: ClassVar[Dict[int, str]] = {}
    _declared_hooks: ClassVar[Dict[LifecycleStage, tuple[str, ...]]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        key_bindings: Dict[int, str] = {}
        hooks: Dict[LifecycleStage, list[str]] = {stage: [] for stage in _ALL_STAGES}

        for name, value in cls.__dict__.items():
            keys = getattr(value, "_tui_monster_keys", None)
            if keys:
                for key in keys:
                    key_bindings[key] = name
            stage = getattr(value, "_tui_monster_stage", None)
            if stage:
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
        self._key_handlers[key] = handler

    def register_key_handlers(self, handlers: Dict[int, KeyHandler]) -> None:
        self._key_handlers.update(handlers)

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

    def addstr(self, y: int, x: int, text: str, attr: Optional[int] = None) -> None:
        if self._stdscr is None:
            return
        if attr is None:
            self._stdscr.addnstr(y, x, text, len(text))
        else:
            self._stdscr.addnstr(y, x, text, len(text), attr)

    def _main(self, stdscr: curses.window) -> None:
        self._stdscr = stdscr
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)
        stdscr.timeout(0)

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

                if self.config.refresh_rate > 0:
                    time.sleep(self.config.refresh_rate)
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
        if self._stdscr is None:
            return
        try:
            key = self._stdscr.getch()
        except curses.error:
            return
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config!r})"


__all__ = ["TuiMonsterApp", "KeyHandler"]
