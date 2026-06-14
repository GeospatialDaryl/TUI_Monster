# Build Menu

`implementation/tools/monster_menu.py` provides an Armbian-style hierarchical
menu TUI. Define your menu as a tree of `MenuItem` objects, pass it to
`MonsterMenuApp`, and call `.run()`.

---

## Anatomy of the Menu

```
┌─────────────────────────────────────────────────────────────┐
│  TUI Monster Build Tools                          [q quit]  │
├──────────────────────────────────────────┬──────────────────┤
│                                          │                  │
│  > Run Script                            │  Run a shell     │
│    Scaffold Project                      │  script with     │
│    Browse Examples                       │  live TUI output │
│    Documentation                         │                  │
│                                          │                  │
├──────────────────────────────────────────┴──────────────────┤
│  ↑↓/jk navigate   Enter select   b/Esc back   q quit        │
└─────────────────────────────────────────────────────────────┘
```

Left panel: menu items with selection highlight.  
Right panel: description of the selected item.  
Footer: key hints.

---

## Defining a Menu

```python
from implementation.tools.monster_menu import MenuItem, MonsterMenuApp

menu = [
    MenuItem(
        label="Build",
        description="Compile and package the project",
        children=[
            MenuItem(
                label="Debug build",
                description="Build with debug symbols",
                action=lambda: run_wrapped(["make", "debug"], title="Debug Build"),
            ),
            MenuItem(
                label="Release build",
                description="Optimised production build",
                action=lambda: run_wrapped(["make", "release"], title="Release"),
            ),
        ],
    ),
    MenuItem(
        label="Test",
        description="Run the test suite",
        action=lambda: run_wrapped(["pytest", "-q"], title="Tests"),
    ),
    MenuItem(
        label="Docs",
        description="Serve documentation locally on port 8000",
        action=lambda: run_wrapped(
            ["mkdocs", "serve", "--config-file", "implementation/docs/mkdocs.yml"],
            title="Docs Server",
        ),
    ),
]

MonsterMenuApp(title="My Project", menu_items=menu).run()
```

---

## MenuItem Reference

```python
@dataclass
class MenuItem:
    label: str            # Menu text shown in the left panel
    description: str      # Help text shown in the right panel
    children: list        # Sub-items; if non-empty, Enter opens submenu
    action: Callable | None  # Callable invoked when Enter is pressed (leaf items)
    shortcut: str         # Optional single-char shortcut shown next to label
```

A `MenuItem` with both `children` and `action` will open the submenu — the
`action` is ignored.

---

## Running the Default Menu

Run `monster_menu.py` directly to launch a pre-built menu for TUI Monster
development tasks:

```bash
python implementation/tools/monster_menu.py
```

The default menu includes:

- **Run Script** — prompt for a command and wrap it
- **Scaffold Project** — interactive `scaffold.py` launcher
- **Run Examples** — numbered list of all tutorial examples
- **Serve Docs** — `mkdocs serve` in a wrapper

---

## Key Controls

| Key | Action |
|-----|--------|
| `↑` / `k` | Move selection up |
| `↓` / `j` | Move selection down |
| `Enter` | Select item (open submenu or run action) |
| `b` / `Esc` | Go back one level |
| `q` | Quit |
