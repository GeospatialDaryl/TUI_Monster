"""Decorator utilities for building pyTuiMonster applications."""

from __future__ import annotations

from typing import Callable, Literal, Protocol

LifecycleStage = Literal[
    "before_start",
    "after_start",
    "before_update",
    "after_update",
    "before_draw",
    "after_draw",
    "before_stop",
    "after_stop",
]


class KeyHandlerProtocol(Protocol):
    def __call__(self, key: int, /) -> None:
        ...


def key_binding(*keys: int) -> Callable[[Callable[[int], None]], Callable[[int], None]]:
    """Mark a method as the handler for one or more key codes."""

    def decorator(func: Callable[[int], None]) -> Callable[[int], None]:
        setattr(func, "_tui_monster_keys", tuple(keys))
        return func

    return decorator


def lifecycle_hook(stage: LifecycleStage) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """Register a method to execute during a lifecycle stage."""

    def decorator(func: Callable[..., None]) -> Callable[..., None]:
        setattr(func, "_tui_monster_stage", stage)
        return func

    return decorator
