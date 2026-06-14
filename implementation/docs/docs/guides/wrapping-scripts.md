# Wrapping Scripts

`implementation/tools/wrap.py` gives any shell command a live TUI interface —
scrollable output, elapsed timer, and a color-coded exit status badge.

---

## Quick Use

```bash
# From the repo root with venv active:
python -m implementation.tools.wrap --title "Run Tests" -- pytest -q
python -m implementation.tools.wrap --title "Build Docs" -- mkdocs build
python -m implementation.tools.wrap -- bash scripts/deploy.sh
```

The `--` separates wrap options from the command being wrapped.

---

## TUI Controls

| Key | Action |
|-----|--------|
| `↑` / `k` | Scroll output up |
| `↓` / `j` | Scroll output down |
| `PgUp` | Scroll up one page |
| `PgDn` | Scroll down one page |
| `a` | Re-enable auto-scroll (follows new output) |
| `q` | Quit (process keeps running until it finishes or you interrupt) |

Auto-scroll is enabled by default and disables automatically when you press `↑`.

---

## Programmatic Use

Import `run_wrapped` to launch the wrapper from another Python script:

```python
from implementation.tools.wrap import run_wrapped

exit_code = run_wrapped(
    command=["pytest", "tests/", "-v"],
    title="Test Suite",
)
if exit_code != 0:
    raise SystemExit(f"Tests failed with exit code {exit_code}")
```

Or subclass `ScriptWrapperApp` for full control:

```python
from implementation.tools.wrap import ScriptWrapperApp
from pyTuiMonster import TuiConfig, key_binding

class MyWrapper(ScriptWrapperApp):
    @key_binding(ord('r'))
    def restart(self, key):
        """Kill and relaunch the wrapped command."""
        if self._proc:
            self._proc.terminate()
        self._launch_process()

MyWrapper(
    command=["python", "server.py"],
    title="Dev Server",
    config=TuiConfig(refresh_rate=1/15),
).run()
```

---

## Status Badges

The header shows one of three status badges:

| Badge | Meaning |
|-------|---------|
| `● RUNNING` (yellow) | Process is active |
| `✓ DONE` (green) | Exited with code 0 |
| `✗ FAILED (N)` (red) | Exited with non-zero code N |

---

## Passing Environment Variables

`run_wrapped` accepts an `env` dict that is merged with the current
environment:

```python
run_wrapped(
    command=["make", "release"],
    title="Release Build",
    env={"BUILD_ENV": "production", "VERBOSE": "1"},
)
```
