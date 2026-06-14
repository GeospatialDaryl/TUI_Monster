# TUI_Monster

This repository packages the `pyTuiMonster` runtime alongside a curated set of
examples and training notes. The runtime exposes a decorator-friendly
:class:`TuiMonsterApp` that streamlines curses application development, with
lifecycle patterns inspired by [btop++](https://github.com/aristocratos/btop).

## Highlights

- **pyTuiMonster runtime** – installable Python package with the event loop,
  configuration dataclass, and registration decorators.
- **Tutorial curriculum** – progressive examples under `examples/` that start
  with a Hello World mode preview and continue through an animated GodMode
  chronometer.
- **Implementation kit** – `implementation/` contains practical tooling:
  `tools/wrap.py` wraps any shell command in a streaming TUI,
  `tools/scaffold.py` generates new project skeletons, and
  `tools/monster_menu.py` provides an Armbian-style menu launcher.
  MkDocs documentation and advanced dev examples live there too.
- **Training notes** – the `training/` directory holds non-functional design
  notes such as the XMR_Godmode investigation (see `training/README.md`).

Refer to `pyTuiMonster/README.md` for detailed runtime guidance,
`README_Examples.md` for the example syllabus, and
`implementation/README.md` for the tooling kit.

## Development

The project is packaged with `pyproject.toml`. Set up a virtual environment
and install in editable mode with the dev dependencies (use `python3` on
systems that do not provide a `python` executable):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Recommended validation before submitting changes (CI runs the same steps on
Python 3.10–3.12):

```bash
python -m compileall -q pyTuiMonster simple_tui.py examples tests
python -m ruff check .
python -m pytest -q
```

## License

MIT — see [LICENSE](LICENSE).
