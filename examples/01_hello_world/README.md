# Example 01: Hello World Mode Preview

This introductory example is the project’s guided “hello world.” Instead of only
printing one static string, it previews every tutorial mode in the TUI Monster
curriculum from one small app:

1. **Hello World** – basic drawing and refresh.
2. **Live Clock** – timed `update()` state changes.
3. **Counter** – decorator-driven key handling.
4. **Task Tracker** – navigation, lifecycle hooks, styling, and collections.
5. **GodMode Clock** – animated, Unicode-heavy rendering.

Run the preview with:

```bash
python3 examples/01_hello_world/main.py
```

Controls:

| Key | Action |
| --- | --- |
| `n`, `Tab`, `Right` | Move to the next mode preview. |
| `p`, `Left` | Move to the previous mode preview. |
| `1`-`5` | Jump directly to a preview mode. |
| `q` | Exit the interface. |

Use this first when evaluating the project: it gives a quick tour of the modes
before you open the full examples in `02_live_clock` through `05_GodMode_clock`.
