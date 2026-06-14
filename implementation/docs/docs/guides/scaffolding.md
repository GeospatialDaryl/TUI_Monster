# Scaffolding

`implementation/tools/scaffold.py` generates ready-to-run TUI project
skeletons from three built-in templates.

---

## Commands

```bash
# Basic app — single-screen TUI with update loop and key bindings
python -m implementation.tools.scaffold new my_app --type basic

# Menu app — Armbian-style hierarchical menu pre-wired with MonsterMenuApp
python -m implementation.tools.scaffold new my_menu --type menu

# Wrapper app — ScriptWrapperApp subclass ready to wrap a command
python -m implementation.tools.scaffold new my_wrapper --type wrapper

# List available templates
python -m implementation.tools.scaffold list
```

---

## Output Structure

Running `scaffold new my_app --type basic` produces:

```
my_app/
├── main.py          # Entry point — subclass of TuiMonsterApp
├── app.py           # App class (split from entry point for larger projects)
└── README.md        # Usage notes and key bindings
```

Running `scaffold new my_menu --type menu` produces:

```
my_menu/
├── main.py          # Entry point calling MonsterMenuApp
├── menu.py          # MenuItem tree definition
└── README.md
```

---

## Template Variables

All templates support these substitutions:

| Variable | Value |
|----------|-------|
| `{{APP_NAME}}` | Directory name passed to `new` |
| `{{CLASS_NAME}}` | CamelCase version of app name |
| `{{DATE}}` | ISO date of generation |
| `{{AUTHOR}}` | Git user name (falls back to system user) |

---

## Custom Templates

Point scaffold at your own template directory with `--template-dir`:

```bash
python -m implementation.tools.scaffold new my_app \
    --type basic \
    --template-dir ~/my_tui_templates
```

Template files must end in `.tmpl`. The filename without `.tmpl` becomes the
output filename. Variables are `{{UPPER_SNAKE}}` placeholders replaced via
simple string substitution.

---

## Programmatic Use

```python
from implementation.tools.scaffold import Scaffolder

s = Scaffolder(output_dir="./projects")
s.create(
    name="dashboard",
    template_type="basic",
    extra_vars={"DESCRIPTION": "System monitoring dashboard"},
)
```
