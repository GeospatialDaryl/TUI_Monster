# TUI Monster Examples

This directory contains a progressive tour through the standalone
`pyTuiMonster.TuiMonsterApp` helper class. Each example lives in its own
subfolder under `examples/` with runnable code and accompanying documentation.

## Structure Overview

| Stage | Folder | Focus |
| ----- | ------ | ----- |
| 1 | `examples/01_hello_world/` | Rendering static content and refreshing the screen. |
| 2 | `examples/02_live_clock/` | Updating state over time with the `update()` hook and `TuiConfig`. |
| 3 | `examples/03_counter/` | Handling keyboard input via the `@key_binding` decorator. |
| 4 | `examples/04_task_tracker/` | Combining navigation, lifecycle hooks, and styling. |
| 5 | `examples/05_GodMode_clock/` | Rotating palettes and Unicode halos inspired by XMR GodMode. |

To run any example, execute the corresponding `main.py` file with Python 3. Press
`q` to exit unless otherwise noted.

## Tutorial Progression

1. **Hello World** introduces the absolute minimum required to start drawing
   with `TuiMonsterApp`. You learn how to subclass, override `draw()`, and
   refresh the buffer.
2. **Live Clock** adds periodic updates and demonstrates how to control the
   refresh cadence while keeping the interface responsive.
3. **Interactive Counter** unlocks user input, showing how to attach keys to
   methods declaratively with `@key_binding` while maintaining mutable state.
4. **Task Tracker** pulls the previous concepts together to build a multi-line
   interface with navigation, toggling, lifecycle messaging, and dynamic
   collections.
5. **GodMode Clock** extends the live clock with color management, Unicode
   glyph constellations, and swirl animations to mirror the maximalist feel of
   the XMR_Godmode tooling.

Follow the sequence in order for the smoothest learning experience.

## Appendix: Decision Log

The following log records the design choices made while preparing this tutorial
suite.

1. Chose five examples to balance brevity with progressive complexity.
2. Ordered the topics from passive rendering to fully interactive management to
   mirror common learning curves for TUI frameworks.
3. Standardized on per-example `README.md` files to keep instructions close to
   the code they describe.
4. Used numeric prefixes (01-05) in folder names so the filesystem mirrors the
   tutorial order.
5. Added a task tracker finale with navigation and list management to highlight
   how previous concepts integrate into a cohesive app.
6. Reserved the `q` key for exiting every example to maintain consistency across
   the suite.
7. Selected lightweight placeholder tasks and auto-generated task names to avoid
   needing separate input handling tutorials at this stage.
8. Documented keyboard shortcuts explicitly in each README to reduce confusion
   when experimenting in the terminal.
9. Migrated the curriculum to the `pyTuiMonster` package to demonstrate the
   stand-alone class requested for the refactor.
10. Adopted decorator-driven input handling in later lessons so the examples
    mirror the modernized API surface area.
11. Added a GodMode clock finale to connect the tutorial to the training
    analysis while showcasing advanced styling and animation controls.
