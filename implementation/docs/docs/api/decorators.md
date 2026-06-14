# Decorators

```python
from pyTuiMonster import key_binding, lifecycle_hook
```

Two decorators cover all input and lifecycle needs.

---

## `@key_binding(*keys: int)`

Mark a method as the handler for one or more key codes. The method receives
the pressed key code as its only argument.

```python
import curses
from pyTuiMonster import key_binding

class MyApp(TuiMonsterApp):
    @key_binding(ord('+'), ord('='), curses.KEY_UP)
    def increment(self, key: int) -> None:
        self._count += 1
```

**Rules:**

- At least one key must be supplied; `@key_binding()` raises `ValueError`.
- All keys must be `int`; passing a string raises `TypeError`.
- Multiple decorators on the same method are supported — each adds its keys.
- If two methods claim the same key, the last registration wins.

**Common key codes:**

| Key | Code |
|-----|------|
| Letter `x` | `ord('x')` |
| Enter | `curses.KEY_ENTER` or `ord('\n')` |
| Escape | `27` |
| Arrow up | `curses.KEY_UP` |
| Arrow down | `curses.KEY_DOWN` |
| Arrow left | `curses.KEY_LEFT` |
| Arrow right | `curses.KEY_RIGHT` |
| Page up | `curses.KEY_PPAGE` |
| Page down | `curses.KEY_NPAGE` |
| Space | `ord(' ')` |
| Backspace | `curses.KEY_BACKSPACE` or `127` |

---

## `@lifecycle_hook(stage: LifecycleStage)`

Run a method at a specific point in the application lifecycle.

```python
from pyTuiMonster import lifecycle_hook

class MyApp(TuiMonsterApp):
    @lifecycle_hook("after_start")
    def init_colors(self) -> None:
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
```

**Stages (in execution order):**

| Stage | When |
|-------|------|
| `"before_start"` | Before the event loop starts; curses not yet initialized |
| `"after_start"` | After curses is initialized; safe to call all curses APIs |
| `"before_update"` | Before each call to `update()` |
| `"after_update"` | After each call to `update()`, before `draw()` |
| `"before_draw"` | Immediately before each `draw()` call |
| `"after_draw"` | Immediately after each `draw()` call |
| `"before_stop"` | After stop is signalled, before loop exits |
| `"after_stop"` | After loop exits, before `curses.endwin()` |

**Rules:**

- Method signature must be `def hook(self) -> None` — no extra arguments.
- Multiple hooks for the same stage are supported; they run in definition order.
- Hooks do not replace `on_start()` / `on_stop()` — both run.

---

## Combining Decorators

Key bindings and lifecycle hooks work independently and can both appear on
the same class:

```python
class MyApp(TuiMonsterApp):
    @lifecycle_hook("after_start")
    def setup(self):
        curses.curs_set(0)
        self._items = ["alpha", "beta", "gamma"]
        self._sel = 0

    @key_binding(curses.KEY_DOWN, ord('j'))
    def next_item(self, key):
        self._sel = (self._sel + 1) % len(self._items)

    @key_binding(curses.KEY_UP, ord('k'))
    def prev_item(self, key):
        self._sel = (self._sel - 1) % len(self._items)

    def draw(self):
        self.clear()
        for i, item in enumerate(self._items):
            attr = curses.A_REVERSE if i == self._sel else curses.A_NORMAL
            self.addstr(i + 1, 2, item, attr)
        self.refresh()
```
