# TuiMonsterApp

```python
from pyTuiMonster import TuiMonsterApp
```

Abstract base class for all TUI Monster applications. Subclass it, override
`draw()`, and call `run()`.

---

## Constructor

```python
TuiMonsterApp(config: TuiConfig | None = None)
```

Pass a [`TuiConfig`](config.md) to override defaults. If omitted, a default
config is created (30 fps, `q` stops).

---

## Abstract Methods

### `draw() -> None`

**Required.** Called every frame after `update()`. Render your interface here.

Always call `self.clear()` at the start and `self.refresh()` at the end:

```python
def draw(self):
    self.clear()
    self.addstr(0, 0, "line one")
    self.refresh()
```

!!! warning
    Do not call `curses.endwin()` or manage the screen lifecycle manually —
    `run()` owns initialization and teardown.

---

## Optional Hooks

### `update() -> None`

Called once per frame **before** `draw()`. Use it to refresh application state
without mixing state logic into rendering code.

```python
def update(self):
    self._now = datetime.datetime.now().isoformat()
```

### `on_start() -> None`

Called once immediately before the main loop starts. The curses screen is
initialized. Equivalent to `@lifecycle_hook("after_start")` on a free method,
but available as a direct override.

### `on_stop() -> None`

Called once after the main loop exits, before `curses.endwin()`.

---

## Rendering Methods

### `addstr(y, x, text, attr=None) -> bool`

Write `text` at row `y`, column `x` with optional curses attributes. Clips
text to the screen width automatically. Returns `True` on success, `False` if
the position is off-screen.

```python
self.addstr(2, 4, "Status: OK", curses.A_BOLD | curses.color_pair(2))
```

### `center_text(y, text, attr=None) -> bool`

Write `text` centered horizontally at row `y`. Same clipping and return
semantics as `addstr`.

```python
self.center_text(self.screen.getmaxyx()[0] // 2, "Centered!", curses.A_BOLD)
```

### `clear() -> None`

Erase the screen buffer. Call at the start of `draw()`.

### `refresh() -> None`

Flush the buffer to the terminal. Call at the end of `draw()`.

---

## Control

### `run() -> None`

Enter the event loop. Blocks until the app stops. Initializes curses, runs
lifecycle hooks, and tears down on exit.

### `stop() -> None`

Signal the event loop to exit after the current frame. Safe to call from
key handlers or lifecycle hooks.

---

## Properties

### `config: TuiConfig`

The active configuration. Read-write; changes take effect on the next frame.

### `running: bool`

`True` while the event loop is active. Read-only.

### `screen: curses.window`

Direct access to the underlying curses window. Only valid while `run()` is
executing. Use `screen.getmaxyx()` to get terminal dimensions.

### `keymap: MappingProxyType[int, KeyHandler]`

Read-only view of all registered key handlers (key code → callable).

---

## Runtime Key Registration

### `register_key_handler(key: int, handler: KeyHandler) -> None`

Attach `handler` to `key` at runtime (outside of class definition):

```python
app = MyApp()
app.register_key_handler(ord('r'), lambda k: app.reset())
app.run()
```

### `register_key_handlers(handlers: Mapping[int, KeyHandler]) -> None`

Attach multiple handlers at once:

```python
app.register_key_handlers({
    ord('r'): lambda k: app.reset(),
    ord('h'): lambda k: app.show_help(),
})
```
