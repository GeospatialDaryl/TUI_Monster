# Example 01: Hello World

This introductory example shows how to use the stand-alone
`pyTuiMonster.TuiMonsterApp` class to display a static message. It focuses on
the core drawing lifecycle:

1. Subclass `TuiMonsterApp` (or the compatibility alias `SimpleTUI`).
2. Override `draw()` to render content.
3. Call `refresh()` after writing to the screen.

Run the example with:

```bash
python examples/01_hello_world/main.py
```

Press `q` to exit the interface.
