"""Compatibility layer for legacy imports (deprecated, use pyTuiMonster)."""

from __future__ import annotations

import warnings

from pyTuiMonster import (
    KeyHandler,
    TuiConfig,
    TuiMonsterApp,
    key_binding,
    lifecycle_hook,
)

warnings.warn(
    "the simple_tui module is deprecated; import from pyTuiMonster instead",
    DeprecationWarning,
    stacklevel=2,
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
