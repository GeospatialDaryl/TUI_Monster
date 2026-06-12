# pyTuiMonster Runtime Guide

This package delivers the standalone runtime requested for TUI_Monster. It wraps
curses session management, lifecycle hooks, and keyboard routing into a single
extensible class while preserving the ergonomic flow inspired by the `btopper`
reference implementation.

## Module Layout

| Module | Responsibility |
| ------ | -------------- |
| `app.py` | Hosts the :class:`TuiMonsterApp` base class with the event loop, rendering helpers, and registration machinery. |
| `config.py` | Defines :class:`TuiConfig`, a lightweight dataclass controlling refresh cadence and exit keys. |
| `decorators.py` | Supplies `@key_binding` and `@lifecycle_hook` decorators for declaratively registering handlers. |
| `__init__.py` | Re-exports the public API for convenient imports (`from pyTuiMonster import TuiMonsterApp`). |

## Core Concepts

### TuiMonsterApp

* Implements the curses lifecycle: initialization, non-blocking input polling,
  update/draw loops, and teardown cleanup.
* Exposes utility helpers (`clear`, `addstr`, `refresh`) that mirror the
  original `SimpleTUI` primitives for compatibility.
* Provides `screen` and `running` properties for safe access to the curses
  window and execution state.
* Supports a read-only `keymap` view so applications can introspect registered
  handlers at runtime.
* Inherits decorated key bindings and lifecycle hooks from parent app classes,
  while rejecting duplicate key declarations within the same class.
* Uses defensive rendering helpers that avoid common narrow-terminal curses
  crashes and provide display-width-aware centering for Unicode-heavy screens.

### TuiConfig

* Encapsulates runtime knobs such as the `refresh_rate` interval and the exit
  key set.
* Validates configuration values at construction (e.g., non-negative refresh
  rates, at least one stop key) to catch mistakes early.
* Can be passed directly to `TuiMonsterApp.__init__` or reused across multiple
  applications for consistent behavior.

### Decorators

* `@key_binding(*keys)` registers the decorated method as the handler for the
  given key codes. Methods still receive the raw key value, enabling custom logic
  per key when needed. The decorator validates that at least one integer key code
  is supplied.
* `@lifecycle_hook(stage)` attaches auxiliary methods to lifecycle moments such
  as `before_start`, `after_draw`, or `before_stop`. This keeps setup/teardown
  logic modular without overriding the primary hook methods unless necessary.
  Stage names are validated at decoration time.

## Usage Pattern

```python
from pyTuiMonster import TuiConfig, TuiMonsterApp, key_binding, lifecycle_hook


class ExampleApp(TuiMonsterApp):
    def __init__(self) -> None:
        super().__init__(TuiConfig(refresh_rate=0.2))
        self.message = "Hello"

    @lifecycle_hook("after_start")
    def announce(self) -> None:
        self.message = "Ready!"

    @key_binding(ord("c"))
    def close(self, _: int) -> None:
        self.stop()

    def update(self) -> None:
        ...  # mutate state here

    def draw(self) -> None:
        self.clear()
        self.addstr(0, 0, self.message)
        self.refresh()


if __name__ == "__main__":
    ExampleApp().run()
```

## Migration Notes

* Legacy imports (`from simple_tui import SimpleTUI`) remain valid through a
  compatibility shim that aliases `SimpleTUI` to `TuiMonsterApp` and re-exports
  the decorators.
* Examples under `examples/` have been updated to consume the new package so the
  tutorial flow mirrors the modernized API.
* Existing projects can incrementally adopt decorators by decorating handlers
  while leaving imperative registration in place; the runtime merges both
  approaches.

## Next Steps

1. Add higher-level widgets (panels, tables) on top of `TuiMonsterApp` as
   mix-ins or companion classes.
2. Expand the fake-screen test suite with additional resize, Unicode-width, and
   lifecycle failure fixtures to keep terminal behavior stable in CI pipelines.
3. Expand the decorator catalog with abstractions for repeating timers or
   scheduled jobs as the project evolves.
