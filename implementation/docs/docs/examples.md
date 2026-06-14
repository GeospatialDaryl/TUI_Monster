# Examples

Five progressive examples live under `examples/` in the repo root. Run any
with `python examples/<folder>/main.py` after activating the venv.

---

## 01 — Hello World Mode Preview

**File:** `examples/01_hello_world/main.py`

An interactive launcher that previews all five tutorial modes before you run
them individually. Use it to get a feel for the framework's range.

**Key controls:**

| Key | Action |
|-----|--------|
| `n` / `Tab` / `→` | Next mode |
| `p` / `←` | Previous mode |
| `1`–`5` | Jump to mode |
| `q` | Quit |

**Concepts demonstrated:** `@lifecycle_hook("after_start")`, centered text,
multi-mode navigation state, frame-based text formatting.

---

## 02 — Live Clock

**File:** `examples/02_live_clock/main.py`

A simple clock that updates every 0.5 seconds using the `update()` hook.
The minimal example of the state-refresh pattern.

**Key controls:** `q` to quit.

**Concepts demonstrated:** `update()` hook, `TuiConfig(refresh_rate=0.5)`,
`datetime` integration.

---

## 03 — Interactive Counter

**File:** `examples/03_counter/main.py`

An integer counter with increment and decrement bound to multiple keys each,
showing how several key codes can share a single handler.

**Key controls:**

| Key | Action |
|-----|--------|
| `+` / `=` / `↑` | Increment |
| `-` / `↓` | Decrement |
| `q` | Quit |

**Concepts demonstrated:** `@key_binding` with multiple keys, mutable state,
`curses.A_BOLD` attribute.

---

## 04 — Task Tracker

**File:** `examples/04_task_tracker/main.py`

A checklist app with Vim-style navigation, toggle, add, and delete operations.
Pulls together navigation, lifecycle hooks, and dynamic collection rendering.

**Key controls:**

| Key | Action |
|-----|--------|
| `↑` / `k` | Move selection up |
| `↓` / `j` | Move selection down |
| `Space` | Toggle done |
| `t` | Add task |
| `x` | Remove task |
| `q` | Quit |

**Concepts demonstrated:** `curses.A_REVERSE` for selection highlight, dynamic
list rendering, `@lifecycle_hook("after_start")` for status init.

---

## 05 — GodMode Clock

**File:** `examples/05_GodMode_clock/main.py`

A maximalist clock with six rotating color palettes, six Unicode glyph sets,
swirl animations, and manual speed controls — inspired by the XMR_Godmode
tooling in the training notes.

**Key controls:**

| Key | Action |
|-----|--------|
| `c` | Toggle color rotation |
| `g` | Toggle glyph rotation |
| `,` / `.` | Previous / next palette |
| `[` / `]` | Previous / next glyph set |
| `+` / `-` | Faster / slower |
| `_` | Slow-roll speed |
| `r` | Reset |
| `s` | Toggle swirl |
| `q` | Quit |

**Concepts demonstrated:** `curses.start_color()`, `curses.init_pair()`,
`curses.color_pair()`, Unicode glyph rendering, `time.monotonic()` for
animation timing.

---

## Dev Examples (implementation/)

Three additional examples in `implementation/dev_examples/` demonstrate the
build tools:

| Example | Focus |
|---------|-------|
| `01_script_runner` | Wrap a shell command with live streaming TUI output |
| `02_progress_tracker` | Multi-step task pipeline with per-step status |
| `03_menu_launcher` | Custom Armbian-style build menu for a real project |
