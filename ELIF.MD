# ELIF: Executive Landscape & Integration Framework

## Project Motivation

TUI_Monster centers on the standalone `pyTuiMonster.TuiMonsterApp`, a
modernized helper that mirrors the lifecycle conventions of
[btop++](https://github.com/aristocratos/btop) while adding decorator-driven
ergonomics for key bindings and lifecycle hooks (`pyTuiMonster/app.py`,
`pyTuiMonster/decorators.py`). The goal is to lower the barrier for rapid TUI
prototyping while keeping the architecture close to familiar terminal-monitor
patterns.

## Repository Organization

| Area | Location | Purpose |
| --- | --- | --- |
| Core helper | `pyTuiMonster/` | Houses the `TuiMonsterApp` class, configuration dataclass, and decorators used to assemble modern TUIs. |
| Example curriculum | `examples/` | Five progressively complex tutorials that teach the helper through runnable scripts and localized guides (see `README_Examples.md`). |
| Test suite | `tests/` | pytest suite covering the runtime, decorators, and the tutorial preview. |
| Training notes | `training/` | Non-functional design notes and investigations, currently anchored by the `analysis_XMR_Godmode.MD` memo (see `training/README.md`). |

The original btop++ project that inspired this runtime lives upstream at
<https://github.com/aristocratos/btop>; it is no longer vendored in this
repository.

## Products Delivered

1. **TuiMonster runtime** – A dataclass-driven event loop with decorator
   registration that handles curses session setup, input routing, rendering
   helpers, and loop control in a compact API surface.
2. **Step-by-step tutorial suite** – A curated pathway from an interactive
   "Hello World" mode preview through a stateful task tracker to the GodMode
   clock finale, each packaged with instructions to run and extend the
   scenarios while highlighting the decorators.
3. **XMR_Godmode design memo** – An exploratory analysis of external
   monitoring tooling, kept in `training/` as reference material only (it
   depends on a `crypto_monkey` package that is not part of this repository).

## Structural Workflow

Developers start by subclassing `TuiMonsterApp`, overriding `update` and
`draw` as needed while optionally decorating key handlers and lifecycle
methods for interactivity. The example curriculum doubles as reference
implementations: begin with `examples/01_hello_world` to validate terminal
setup, layer in timed refreshes via `02_live_clock`, add decorator-driven
input in `03_counter`, combine the patterns in `04_task_tracker`, and explore
styling and animation in `05_GodMode_clock`. Documentation in each example
folder keeps usage instructions adjacent to the code for quick iteration.

## Next Horizons

- **Integrate real data feeds** by pairing a polling loop with a
  `TuiMonsterApp` visualization that surfaces live metrics in real time.
- **Broaden the tutorial catalog** with additional scenarios (e.g., log
  viewers, alert dashboards) that demonstrate advanced key handling, windows,
  and color themes, extending the numbered progression already established.
- **Grow the widget layer** — higher-level panels and tables on top of
  `TuiMonsterApp` as mix-ins or companion classes.
