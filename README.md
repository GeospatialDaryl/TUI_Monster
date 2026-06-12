# TUI_Monster

This repository packages the `pyTuiMonster` runtime alongside a curated set of
examples and training assets. The runtime exposes a decorator-friendly
:class:`TuiMonsterApp` that streamlines curses application development while
keeping the lifecycle patterns familiar to teams accustomed to btopper.

## Highlights

- **pyTuiMonster runtime** – installable Python package metadata plus the event
  loop, configuration dataclass, and registration decorators.
- **Tutorial curriculum** – progressive examples under `examples/` that start
  with a Hello World mode preview and continue through an animated GodMode
  chronometer.
- **Training insights** – the `training/` directory documents investigations
  such as the ongoing XMR_Godmode analysis.

Refer to `pyTuiMonster/README.md` for detailed runtime guidance and to
`README_Exampls.MD` for the example syllabus.

## Development

The project is packaged with `pyproject.toml` and can be installed in editable
mode when working locally. Use `python3` on systems that do not provide a
`python` executable:

```bash
python3 -m pip install -e .
```

Recommended validation before submitting changes:

```bash
python3 -m compileall -q pyTuiMonster simple_tui.py examples tests
python3 -m pytest -q
```
