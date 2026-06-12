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

ALL_LIFECYCLE_STAGES: tuple[LifecycleStage, ...] = (
    "before_start",
    "after_start",
    "before_update",
    "after_update",
    "before_draw",
    "after_draw",
    "before_stop",
    "after_stop",
)


class KeyHandlerProtocol(Protocol):
    def __call__(self, key: int, /) -> None:
        ...


def key_binding(*keys: int) -> Callable[[Callable[[int], None]], Callable[[int], None]]:
    """Mark a method as the handler for one or more key codes.

    Parameters
    ----------
    *keys:
        Integer key codes returned by ``curses.window.getch``.

    Raises
    ------
    ValueError
        If no keys are supplied.
    TypeError
        If any key is not an integer.
    """

    if not keys:
        raise ValueError("key_binding requires at least one key code")
    invalid_keys = [key for key in keys if not isinstance(key, int)]
    if invalid_keys:
        raise TypeError("key_binding keys must be integers")

    def decorator(func: Callable[[int], None]) -> Callable[[int], None]:
        setattr(func, "_tui_monster_keys", tuple(keys))
        return func

    return decorator


def lifecycle_hook(stage: LifecycleStage) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """Register a method to execute during a lifecycle stage.

    Raises
    ------
    ValueError
        If ``stage`` is not one of the supported lifecycle stage names.
    """

    if stage not in ALL_LIFECYCLE_STAGES:
        supported = ", ".join(ALL_LIFECYCLE_STAGES)
        raise ValueError(f"Unsupported lifecycle stage {stage!r}; expected one of: {supported}")

    def decorator(func: Callable[..., None]) -> Callable[..., None]:
        setattr(func, "_tui_monster_stage", stage)
        return func

    return decorator
