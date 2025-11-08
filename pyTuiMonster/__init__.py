"""pyTuiMonster: opinionated curses application scaffolding."""

from __future__ import annotations

from .app import KeyHandler, TuiMonsterApp
from .config import TuiConfig
from .decorators import LifecycleStage, key_binding, lifecycle_hook

__all__ = [
    "KeyHandler",
    "LifecycleStage",
    "TuiConfig",
    "TuiMonsterApp",
    "key_binding",
    "lifecycle_hook",
]
