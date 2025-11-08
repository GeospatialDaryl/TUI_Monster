"""Compatibility layer for legacy imports."""

from __future__ import annotations

from pyTuiMonster import (
    KeyHandler,
    TuiConfig,
    TuiMonsterApp,
    key_binding,
    lifecycle_hook,
)

SimpleTUI = TuiMonsterApp

__all__ = [
    "KeyHandler",
    "SimpleTUI",
    "TuiConfig",
    "TuiMonsterApp",
    "key_binding",
    "lifecycle_hook",
]
