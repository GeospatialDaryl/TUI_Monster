# Getting Started

## Prerequisites

- Python 3.10 or newer
- A terminal emulator that supports curses (any modern Linux/macOS terminal)
- The `pyTuiMonster` package installed in your environment

## Setup

```bash
git clone https://github.com/GeospatialDaryl/TUI_Monster
cd TUI_Monster
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

Verify the install:

```bash
python -c "from pyTuiMonster import TuiMonsterApp; print('OK')"
```

## Hello World

The minimal app overrides one method:

```python
from pyTuiMonster import TuiMonsterApp

class HelloApp(TuiMonsterApp):
    def draw(self):
        self.clear()
        self.center_text(0, "Hello, TUI Monster!  (press q to quit)")
        self.refresh()

HelloApp().run()
```

Save as `hello.py` and run:

```bash
python hello.py
```

Press `q` to exit (the default stop key).

## Adding a Key Binding

Use `@key_binding` to attach a method to one or more key codes:

```python
import curses
from pyTuiMonster import TuiMonsterApp, key_binding

class GreetApp(TuiMonsterApp):
    def __init__(self):
        super().__init__()
        self._name = "world"

    @key_binding(ord('1'))
    def greet_alice(self, key):
        self._name = "Alice"

    @key_binding(ord('2'))
    def greet_bob(self, key):
        self._name = "Bob"

    def draw(self):
        self.clear()
        h, w = self.screen.getmaxyx()
        self.center_text(h // 2, f"Hello, {self._name}!  (1/2 change name, q quit)")
        self.refresh()

GreetApp().run()
```

## Lifecycle Hooks

Run code once at startup or shutdown without touching `__init__`:

```python
from pyTuiMonster import TuiMonsterApp, lifecycle_hook

class InitApp(TuiMonsterApp):
    @lifecycle_hook("after_start")
    def setup(self):
        # curses is fully initialized here — safe to call initscr-dependent APIs
        curses.curs_set(0)   # hide cursor
        self._ready = True

    def draw(self):
        self.clear()
        status = "ready" if getattr(self, "_ready", False) else "starting"
        self.center_text(0, status)
        self.refresh()

InitApp().run()
```

## Controlling Refresh Rate

`TuiConfig.refresh_rate` is seconds per frame. Pass it to the constructor:

```python
from pyTuiMonster import TuiMonsterApp, TuiConfig

class SlowApp(TuiMonsterApp):
    def draw(self):
        self.clear()
        self.center_text(0, "Updates once per second")
        self.refresh()

SlowApp(TuiConfig(refresh_rate=1.0)).run()
```

Set `refresh_rate=0` for uncapped (CPU-bound rendering).

## Next Steps

- Read the [API Reference](api/app.md) for every method and property.
- Follow the [Guides](guides/wrapping-scripts.md) to wrap real scripts and build menus.
- Explore the [Examples](examples.md) to see the full tutorial progression.
