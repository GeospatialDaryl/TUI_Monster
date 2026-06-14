"""Dev example 03 — custom Armbian-style build menu for TUI Monster itself.

Run:
    python implementation/dev_examples/03_menu_launcher/main.py

Demonstrates:
- Building a MenuItem tree for a real project
- Nesting submenus for grouped actions
- Wiring run_wrapped() as leaf actions
- Adding shortcut keys to menu items
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from implementation.tools.monster_menu import MenuItem, MonsterMenuApp
from implementation.tools.wrap import run_wrapped

REPO = Path(__file__).resolve().parents[3]
PY = sys.executable


def _cmd(label: str, cmd: list[str]) -> MenuItem:
    return MenuItem(
        label=label,
        description=f"Run: {' '.join(cmd)}",
        action=lambda c=cmd, t=label: run_wrapped(c, title=t),
    )


def build_menu() -> list[MenuItem]:
    return [
        MenuItem(
            label="Quality",
            description="Linting, type checks, and compile verification",
            shortcut="q",
            children=[
                _cmd("Lint (ruff)", [PY, "-m", "ruff", "check", str(REPO)]),
                _cmd("Compile check", [PY, "-m", "compileall", "-q", str(REPO)]),
                _cmd("Ruff fix", [PY, "-m", "ruff", "check", "--fix", str(REPO)]),
            ],
        ),
        MenuItem(
            label="Test",
            description="Run the pytest test suite",
            shortcut="t",
            children=[
                _cmd("All tests", [PY, "-m", "pytest", str(REPO / "tests"), "-v"]),
                _cmd("Quick tests (-q)", [PY, "-m", "pytest", str(REPO / "tests"), "-q"]),
                _cmd("With coverage", [
                    PY, "-m", "pytest", str(REPO / "tests"),
                    "--cov=pyTuiMonster", "--cov-report=term-missing",
                ]),
            ],
        ),
        MenuItem(
            label="Examples",
            description="Run any of the five tutorial examples",
            shortcut="e",
            children=[
                MenuItem(
                    label=f"{i}. {name}",
                    description=desc,
                    action=(lambda n=n, _name=name: run_wrapped(
                        [PY, str(REPO / "examples" / n / "main.py")],
                        title=_name,
                    )),
                )
                for i, (n, name, desc) in enumerate(
                    [
                        ("01_hello_world", "Hello World", "Mode preview launcher"),
                        ("02_live_clock", "Live Clock", "Periodic update via update()"),
                        ("03_counter", "Counter", "Key bindings and mutable state"),
                        ("04_task_tracker", "Task Tracker", "Navigation and lifecycle"),
                        ("05_GodMode_clock", "GodMode Clock", "Colors and animation"),
                    ],
                    start=1,
                )
            ],
        ),
        MenuItem(
            label="Docs",
            description="Documentation tools",
            shortcut="d",
            children=[
                _cmd(
                    "Serve docs (localhost:8000)",
                    [PY, "-m", "mkdocs", "serve",
                     "--config-file",
                     str(REPO / "implementation" / "docs" / "mkdocs.yml")],
                ),
                _cmd(
                    "Build docs",
                    [PY, "-m", "mkdocs", "build",
                     "--config-file",
                     str(REPO / "implementation" / "docs" / "mkdocs.yml")],
                ),
            ],
        ),
        MenuItem(
            label="Scaffold",
            description="Generate a new TUI project skeleton",
            shortcut="s",
            children=[
                MenuItem(
                    label=f"New {t} project",
                    description=desc,
                    action=(lambda t=t: run_wrapped(
                        [PY, "-m", "implementation.tools.scaffold", "list"],
                        title=f"Scaffold — {t}",
                    )),
                )
                for t, desc in [
                    ("basic", "Single-screen TUI with key bindings"),
                    ("menu", "Armbian-style hierarchical menu"),
                    ("wrapper", "Script wrapper subclass"),
                ]
            ],
        ),
    ]


if __name__ == "__main__":
    MonsterMenuApp(
        title="TUI Monster Dev",
        version="v1.0",
        menu_items=build_menu(),
    ).run()
