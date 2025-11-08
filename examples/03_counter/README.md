# Example 03: Interactive Counter

The third step introduces keyboard interaction by registering key handlers in
`on_start()`. Users can increment or decrement the counter using multiple key
bindings.

Concepts introduced:

- Registering handlers with `register_handlers()`.
- Responding to alphanumeric and arrow keys.
- Maintaining mutable state (`self.count`) across frames.

Run the example with:

```bash
python examples/03_counter/main.py
```

Use `+` / `-` (or arrow keys) to change the value and `q` to exit.
