# Dev Example 02 — Progress Tracker

A multi-step pipeline view with live per-step status badges, built as a
custom `TuiMonsterApp` subclass (not `ScriptWrapperApp`).

## Run

```bash
python implementation/dev_examples/02_progress_tracker/main.py
```

## What It Shows

- `threading.Thread` for background work while the TUI renders at fixed rate
- Per-step status badges: PENDING → RUNNING → OK / FAIL
- Color pairs initialized in `@lifecycle_hook("after_start")`
- Final pass/fail summary with color

## Adapting It

Replace the `_fake_step(...)` calls in `main()` with real `Step` objects:

```python
def run_tests() -> bool:
    result = subprocess.run(["pytest", "-q"], capture_output=True)
    return result.returncode == 0

steps = [
    Step(label="Run tests", fn=run_tests),
]
```

The `fn` callable must return `True` on success, `False` on failure, and
may raise any exception to mark the step as failed with the exception
message shown inline.
