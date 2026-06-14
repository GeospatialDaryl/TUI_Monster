"""Configuration objects for the pyTuiMonster runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import curses

_DEFAULT_STOP_KEYS = (ord("q"),)
if hasattr(curses, "KEY_EXIT"):
    _DEFAULT_STOP_KEYS = _DEFAULT_STOP_KEYS + (curses.KEY_EXIT,)


@dataclass(slots=True)
class TuiConfig:
    """Runtime configuration for :class:`~pyTuiMonster.app.TuiMonsterApp`.

    Parameters
    ----------
    refresh_rate:
        Seconds between frames. The interval is enforced by the curses input
        timeout, so a keypress wakes the loop immediately. A value of ``0``
        disables waiting entirely and the loop runs as fast as possible
        (useful for tests, but it busy-spins a CPU core in a real terminal).
    stop_keys:
        Key codes that cause :meth:`~pyTuiMonster.app.TuiMonsterApp.stop`
        to be invoked when pressed.
    """

    refresh_rate: float = 1 / 30
    stop_keys: Tuple[int, ...] = _DEFAULT_STOP_KEYS

    def __post_init__(self) -> None:
        if self.refresh_rate < 0:
            raise ValueError("refresh_rate must be non-negative")
        if not self.stop_keys:
            raise ValueError("stop_keys must contain at least one key code")
