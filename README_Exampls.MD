# TUI Monster Examples

This directory contains a progressive tour through the `SimpleTUI` helper
class. Each example lives in its own subfolder under `examples/` with runnable
code and accompanying documentation.

## Structure Overview

| Stage | Folder | Focus |
| ----- | ------ | ----- |
| 1 | `examples/01_hello_world/` | Rendering static content and refreshing the screen. |
| 2 | `examples/02_live_clock/` | Updating state over time with the `update()` hook. |
| 3 | `examples/03_counter/` | Handling keyboard input and mutating application state. |
| 4 | `examples/04_task_tracker/` | Combining navigation, stateful lists, and styling. |

To run any example, execute the corresponding `main.py` file with Python 3. Press
`q` to exit unless otherwise noted.

## Tutorial Progression

1. **Hello World** introduces the absolute minimum required to start drawing with
   `SimpleTUI`. You learn how to subclass, override `draw()`, and refresh the
   buffer.
2. **Live Clock** adds periodic updates and demonstrates how to control the
   refresh cadence while keeping the interface responsive.
3. **Interactive Counter** unlocks user input, showing how to register key
   handlers and maintain mutable state across frames.
4. **Task Tracker** pulls the previous concepts together to build a multi-line
   interface with navigation, toggling, and dynamic collections.

Follow the sequence in order for the smoothest learning experience.

## Appendix: Decision Log

The following log records the design choices made while preparing this tutorial
suite.

1. Chose four examples to balance brevity with progressive complexity.
2. Ordered the topics from passive rendering to fully interactive management to
   mirror common learning curves for TUI frameworks.
3. Standardized on per-example `README.md` files to keep instructions close to
   the code they describe.
4. Used numeric prefixes (01-04) in folder names so the filesystem mirrors the
   tutorial order.
5. Added a task tracker finale with navigation and list management to highlight
   how previous concepts integrate into a cohesive app.
6. Reserved the `q` key for exiting every example to maintain consistency across
   the suite.
7. Selected lightweight placeholder tasks and auto-generated task names to avoid
   needing separate input handling tutorials at this stage.
8. Documented keyboard shortcuts explicitly in each README to reduce confusion
   when experimenting in the terminal.
