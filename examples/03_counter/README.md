# Example 03: Interactive Counter

The third step introduces keyboard interaction by decorating handler methods
with `@key_binding`. Users can increment or decrement the counter using multiple
key bindings without manual registration code in `on_start()`.

Concepts introduced:

- Decorating handlers with `@key_binding` to associate keys with methods.
- Responding to alphanumeric and arrow keys.
- Maintaining mutable state (`self.count`) across frames.

Run the example with:

```bash
python examples/03_counter/main.py
```

Use `+` / `-` (or arrow keys) to change the value and `q` to exit.
