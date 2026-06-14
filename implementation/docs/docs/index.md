# TUI Monster

**Decorator-friendly curses TUI framework for Python.**

TUI Monster wraps Python's `curses` module behind a clean class-based API so
you can build terminal UIs by overriding a single `draw()` method and
annotating handlers with decorators — no event-loop boilerplate, no manual
`getch` loops.

---

## At a Glance

```python
import curses
from pyTuiMonster import TuiMonsterApp, TuiConfig, key_binding

class ClockApp(TuiMonsterApp):
    import datetime

    def update(self):
        self._now = self.datetime.datetime.now().strftime("%H:%M:%S")

    def draw(self):
        self.clear()
        self.center_text(self.screen.getmaxyx()[0] // 2, self._now, curses.A_BOLD)
        self.refresh()

ClockApp(TuiConfig(refresh_rate=1.0)).run()
```

---

## Why TUI Monster?

| Feature | Detail |
|---------|--------|
| **Minimal API** | One abstract method (`draw`), three optional hooks |
| **Decorator input** | `@key_binding` and `@lifecycle_hook` keep handlers close to logic |
| **Safe rendering** | Unicode-aware `addstr` / `center_text` — no curses crashes on wide chars |
| **Composable config** | `TuiConfig` dataclass — swap refresh rate or stop keys without subclassing |
| **No dependencies** | Pure stdlib; curses ships with CPython |

---

## Installation

```bash
# From repo root
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
```

---

## Navigation

- **[Getting Started](getting-started.md)** — environment setup, hello world, first key binding
- **[API Reference](api/app.md)** — every public method and property
- **[Guides](guides/wrapping-scripts.md)** — practical recipes: script wrapping, build menus, scaffolding
- **[Examples](examples.md)** — annotated walkthroughs of all five tutorial examples
