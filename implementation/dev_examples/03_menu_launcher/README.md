# Dev Example 03 — Menu Launcher

A complete Armbian-style build menu for TUI Monster development, wiring real
project commands (lint, test, examples, docs, scaffold) into a hierarchical
`MonsterMenuApp`.

## Run

```bash
python implementation/dev_examples/03_menu_launcher/main.py
```

## What It Shows

- Building a `MenuItem` tree with nested submenus
- Using `run_wrapped()` as leaf actions
- Shortcut keys (`q`, `t`, `e`, `d`, `s`) for quick top-level access
- The full two-panel Armbian-style layout in action

## Key Controls

| Key | Action |
|-----|--------|
| `↑` / `k` | Move up |
| `↓` / `j` | Move down |
| `Enter` | Select / open submenu |
| `b` / `Esc` | Go back |
| `q` | Quit |

## Adapting It

Copy `main.py`, replace the `build_menu()` function with your own
`MenuItem` tree, and change `REPO` to point at your project root.

The `_cmd()` helper at the top is a shorthand — each `MenuItem` just needs
a `label`, `description`, and either `children` or an `action` callable.
