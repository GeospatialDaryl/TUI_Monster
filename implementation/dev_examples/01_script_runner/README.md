# Dev Example 01 — Script Runner

Wrap any shell command in a live streaming TUI using `ScriptWrapperApp`.

## Run

```bash
python implementation/dev_examples/01_script_runner/main.py
```

## What It Shows

- The `run_wrapped()` convenience function launching a multi-step shell script
- Auto-scroll tracking new output in real time
- Color-coded status badge (RUNNING → DONE / FAILED)
- Elapsed time counter in the header

## Key Controls

| Key | Action |
|-----|--------|
| `↑` / `k` | Scroll up |
| `↓` / `j` | Scroll down |
| `PgUp` / `PgDn` | Page scroll |
| `a` | Re-enable auto-scroll |
| `q` | Quit |

## Next Steps

- Replace the `script` string in `main.py` with your own command
- Subclass `ScriptWrapperApp` (see the `wrapper` scaffold template) to add
  custom key bindings like restart or kill
