# Example 04: Task Tracker

The final tutorial entry combines rendering, updates, lifecycle hooks, and
keyboard controls to manage a small checklist. It demonstrates how to build a
multi-line layout and support multiple interaction patterns.

Concepts introduced:

- Representing structured state with a dataclass.
- Navigating lists with wrap-around selection.
- Toggling, adding, and removing items through decorated key handlers.
- Using `@lifecycle_hook` to announce readiness once the UI boots.
- Highlighting selections using `curses.A_REVERSE` attributes.

Run the example with:

```bash
python3 examples/04_task_tracker/main.py
```

Navigation shortcuts:

- Arrow keys or `j`/`k` move the selection.
- Space toggles completion.
- `t` creates a placeholder task.
- `x` removes the selected task.
- `q` exits the application.
