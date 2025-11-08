# Example 02: Live Clock

Building on the Hello World example, this TUI adds an `update()` method to track
changing state. The interface prints the current timestamp and refreshes twice
per second.

Concepts introduced:

- Managing state on the instance (`self.current_time`).
- Using `update()` for periodic refreshes.
- Adjusting `refresh_rate` for smoother updates.

Run the example with:

```bash
python examples/02_live_clock/main.py
```

Press `q` to exit.
