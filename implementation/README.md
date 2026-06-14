# TUI Monster — Implementation Kit

Practical tooling for building, wrapping, and documenting TUI applications
with `pyTuiMonster`.

## Layout

```
implementation/
├── docs/               Web documentation (MkDocs Material)
├── tools/              Build tools for wrapping scripts and scaffolding projects
└── dev_examples/       Advanced examples beyond the tutorial curriculum
```

## Quick Start

```bash
# Install docs dependencies and serve locally
pip install -r implementation/docs/requirements-docs.txt
mkdocs serve --config-file implementation/docs/mkdocs.yml

# Wrap any shell command in a TUI
python -m implementation.tools.wrap --title "Run Tests" -- pytest -q

# Launch the Armbian-style build menu
python implementation/tools/monster_menu.py

# Scaffold a new TUI project
python -m implementation.tools.scaffold new my_app --type basic
```

## Tools

| Tool | Purpose |
|------|---------|
| `tools/wrap.py` | Wrap any command with live streaming output in a TUI |
| `tools/monster_menu.py` | Armbian-style hierarchical menu launcher |
| `tools/scaffold.py` | Generate new TUI project skeletons from templates |

## Dev Examples

| Example | Focus |
|---------|-------|
| `01_script_runner` | Run and monitor shell scripts with TUI feedback |
| `02_progress_tracker` | Multi-step task progress with per-step status |
| `03_menu_launcher` | Custom build menu wiring real project commands |
