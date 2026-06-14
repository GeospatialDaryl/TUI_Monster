"""Armbian-style hierarchical menu TUI for TUI Monster build tooling."""

from __future__ import annotations

import curses
import sys
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from pyTuiMonster import TuiMonsterApp, TuiConfig, key_binding, lifecycle_hook


@dataclass
class MenuItem:
    """A single entry in the menu tree."""

    label: str
    description: str
    children: List["MenuItem"] = field(default_factory=list)
    action: Optional[Callable[[], None]] = None
    shortcut: str = ""


# ---------------------------------------------------------------------------
# Color pair indices
_CP_HEADER = 1      # white on deep-orange (approximated as yellow)
_CP_HEADER_DIM = 2  # dim white on dark
_CP_SELECTED = 3    # black on green
_CP_NORMAL = 4      # white on black
_CP_ARROW = 5       # yellow on black (submenu indicator)
_CP_DESCRIPTION = 6 # cyan on black
_CP_BORDER = 7      # dark cyan on black
_CP_FOOTER = 8      # black on white
_CP_SHORTCUT = 9    # yellow on black


class MonsterMenuApp(TuiMonsterApp):
    """
    Armbian-style two-panel hierarchical menu.

    Left panel: menu items with arrow-key navigation.
    Right panel: description of the selected item.
    Footer: key hints.
    """

    def __init__(
        self,
        title: str = "TUI Monster",
        menu_items: Optional[List[MenuItem]] = None,
        version: str = "",
        config: Optional[TuiConfig] = None,
    ) -> None:
        super().__init__(config or TuiConfig(refresh_rate=1 / 20))
        self._title = title
        self._version = version
        # Navigation stack: list of (items, selected_index)
        self._nav_stack: List[tuple[List[MenuItem], int]] = [
            (menu_items or [], 0)
        ]
        self._message = ""   # transient status message
        self._msg_timer = 0.0

    # ------------------------------------------------------------------
    # Properties

    @property
    def _current_items(self) -> List[MenuItem]:
        return self._nav_stack[-1][0]

    @property
    def _selected_index(self) -> int:
        return self._nav_stack[-1][1]

    @_selected_index.setter
    def _selected_index(self, value: int) -> None:
        level = self._nav_stack[-1]
        self._nav_stack[-1] = (level[0], value)

    @property
    def _selected_item(self) -> Optional[MenuItem]:
        items = self._current_items
        if not items:
            return None
        return items[self._selected_index]

    # ------------------------------------------------------------------
    # Lifecycle

    @lifecycle_hook("after_start")
    def _init_colors(self) -> None:
        curses.start_color()
        curses.use_default_colors()
        # Armbian uses a bold orange/amber header — approximate with yellow
        curses.init_pair(_CP_HEADER, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(_CP_HEADER_DIM, curses.COLOR_WHITE, -1)
        curses.init_pair(_CP_SELECTED, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(_CP_NORMAL, curses.COLOR_WHITE, -1)
        curses.init_pair(_CP_ARROW, curses.COLOR_YELLOW, -1)
        curses.init_pair(_CP_DESCRIPTION, curses.COLOR_CYAN, -1)
        curses.init_pair(_CP_BORDER, curses.COLOR_CYAN, -1)
        curses.init_pair(_CP_FOOTER, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(_CP_SHORTCUT, curses.COLOR_YELLOW, -1)
        curses.curs_set(0)

    # ------------------------------------------------------------------
    # Drawing

    def draw(self) -> None:
        self.clear()
        h, w = self.screen.getmaxyx()

        self._draw_header(h, w)
        self._draw_panels(h, w)
        self._draw_footer(h, w)
        self.refresh()

    def _draw_header(self, h: int, w: int) -> None:
        # Full-width amber banner
        banner = " " * w
        self.addstr(0, 0, banner, curses.color_pair(_CP_HEADER) | curses.A_BOLD)
        title_str = f"  {self._title}"
        version_str = f"  {self._version}  " if self._version else "  "
        self.addstr(0, 0, title_str, curses.color_pair(_CP_HEADER) | curses.A_BOLD)
        if len(title_str) + len(version_str) < w:
            self.addstr(0, w - len(version_str), version_str,
                        curses.color_pair(_CP_HEADER))

        # Breadcrumb path
        path_parts = []
        for i, (items, sel) in enumerate(self._nav_stack):
            if i == 0:
                path_parts.append(self._title)
            else:
                parent_items = self._nav_stack[i - 1][0]
                parent_sel = self._nav_stack[i - 1][1]
                if 0 <= parent_sel < len(parent_items):
                    path_parts.append(parent_items[parent_sel].label)
        breadcrumb = " › ".join(path_parts)
        self.addstr(1, 2, breadcrumb[:w - 4], curses.color_pair(_CP_HEADER_DIM) | curses.A_DIM)
        # Separator
        self.addstr(2, 0, "─" * w, curses.color_pair(_CP_BORDER))

    def _draw_panels(self, h: int, w: int) -> None:
        # Layout: header=3 rows, footer=2 rows → panel height = h - 5
        panel_top = 3
        panel_h = h - 5
        left_w = max(20, w * 2 // 3)
        right_w = w - left_w - 1

        items = self._current_items
        sel = self._selected_index

        # Scroll window so selection is visible
        max_visible = panel_h
        scroll_start = max(0, sel - max_visible + 1) if sel >= max_visible else 0
        visible_items = items[scroll_start: scroll_start + max_visible]

        # Left panel — item list
        for i, item in enumerate(visible_items):
            row = panel_top + i
            abs_i = scroll_start + i
            is_sel = abs_i == sel

            attr = curses.color_pair(_CP_SELECTED) | curses.A_BOLD if is_sel \
                else curses.color_pair(_CP_NORMAL)

            # Pad the entire left panel width for selection highlight
            line = " " * left_w
            self.addstr(row, 0, line, attr)

            # Shortcut badge
            prefix = f"[{item.shortcut}] " if item.shortcut else "    "
            label = f"{prefix}{item.label}"
            label = label[:left_w - 4]
            self.addstr(row, 2, label, attr)

            # Submenu arrow
            if item.children:
                self.addstr(row, left_w - 3, " ›",
                            curses.color_pair(_CP_ARROW) | curses.A_BOLD if is_sel
                            else curses.color_pair(_CP_ARROW))

        # Vertical divider
        for row in range(panel_top, panel_top + panel_h):
            self.addstr(row, left_w, "│", curses.color_pair(_CP_BORDER))

        # Right panel — description of selected item
        if self._selected_item:
            desc = self._selected_item.description
            desc_words = desc.split()
            lines: list[str] = []
            current = ""
            for word in desc_words:
                if len(current) + len(word) + 1 <= right_w - 2:
                    current = f"{current} {word}" if current else word
                else:
                    lines.append(current)
                    current = word
            if current:
                lines.append(current)
            for i, line in enumerate(lines[:panel_h]):
                self.addstr(panel_top + i, left_w + 2, line,
                            curses.color_pair(_CP_DESCRIPTION))

        # Status message overlay (transient)
        if self._message:
            self.center_text(panel_top + panel_h // 2, f" {self._message} ",
                             curses.color_pair(_CP_SELECTED) | curses.A_BOLD)

        # Separator above footer
        self.addstr(panel_top + panel_h, 0, "─" * w, curses.color_pair(_CP_BORDER))

    def _draw_footer(self, h: int, w: int) -> None:
        depth_indicator = f"  depth: {len(self._nav_stack)}" if len(self._nav_stack) > 1 else ""
        keys = "↑↓/jk navigate   Enter select   b/Esc back   q quit"
        footer = f" {keys}{depth_indicator}"
        self.addstr(h - 1, 0, " " * w, curses.color_pair(_CP_FOOTER))
        self.addstr(h - 1, 0, footer[:w - 1], curses.color_pair(_CP_FOOTER))

    # ------------------------------------------------------------------
    # Key handlers

    @key_binding(curses.KEY_UP, ord('k'))
    def move_up(self, key: int) -> None:
        items = self._current_items
        if items:
            self._selected_index = (self._selected_index - 1) % len(items)
        self._message = ""

    @key_binding(curses.KEY_DOWN, ord('j'))
    def move_down(self, key: int) -> None:
        items = self._current_items
        if items:
            self._selected_index = (self._selected_index + 1) % len(items)
        self._message = ""

    @key_binding(curses.KEY_ENTER, ord('\n'), ord('\r'))
    def select_item(self, key: int) -> None:
        item = self._selected_item
        if item is None:
            return
        if item.children:
            self._nav_stack.append((item.children, 0))
        elif item.action:
            # Suspend curses, run the action, restore
            curses.endwin()
            try:
                item.action()
            except Exception as exc:
                print(f"\nError: {exc}")
                input("\nPress Enter to return to menu...")
            finally:
                # Re-init curses (run() will restore properly on next frame)
                self.screen.refresh()
        else:
            self._message = f"No action defined for '{item.label}'"

    @key_binding(ord('b'), 27)   # 27 = ESC
    def go_back(self, key: int) -> None:
        if len(self._nav_stack) > 1:
            self._nav_stack.pop()
            self._message = ""


# ---------------------------------------------------------------------------
# Default development menu

def _make_default_menu() -> List[MenuItem]:
    """Build menu pre-wired for TUI Monster development tasks."""
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]

    def _wrap_cmd(cmd: list[str], title: str) -> None:
        from implementation.tools.wrap import run_wrapped
        run_wrapped(command=cmd, title=title)

    def _run_example(n: int) -> None:
        examples = {
            1: "01_hello_world",
            2: "02_live_clock",
            3: "03_counter",
            4: "04_task_tracker",
            5: "05_GodMode_clock",
        }
        folder = examples.get(n, "01_hello_world")
        path = repo_root / "examples" / folder / "main.py"
        _wrap_cmd([sys.executable, str(path)], f"Example {n}: {folder}")

    examples_items = [
        MenuItem(
            label=f"{i}. {name}",
            description=desc,
            action=(lambda n=i: _run_example(n)),
            shortcut=str(i),
        )
        for i, (name, desc) in enumerate(
            [
                ("Hello World", "Interactive mode preview — overview of all examples"),
                ("Live Clock", "Periodic state update via update() hook"),
                ("Counter", "Key bindings and mutable state"),
                ("Task Tracker", "Navigation, lifecycle hooks, and dynamic lists"),
                ("GodMode Clock", "Color palettes, Unicode glyphs, and animation"),
            ],
            start=1,
        )
    ]

    return [
        MenuItem(
            label="Run Tests",
            description="Run the full pytest suite with verbose output",
            action=lambda: _wrap_cmd(
                [sys.executable, "-m", "pytest", "-v", str(repo_root / "tests")],
                "Test Suite",
            ),
            shortcut="t",
        ),
        MenuItem(
            label="Lint",
            description="Run ruff on the entire repository",
            action=lambda: _wrap_cmd(
                [sys.executable, "-m", "ruff", "check", str(repo_root)],
                "Ruff Lint",
            ),
            shortcut="l",
        ),
        MenuItem(
            label="Examples",
            description="Launch any of the five tutorial examples",
            children=examples_items,
            shortcut="e",
        ),
        MenuItem(
            label="Scaffold Project",
            description="Generate a new TUI project skeleton from a template",
            action=lambda: _wrap_cmd(
                [sys.executable, "-m", "implementation.tools.scaffold", "list"],
                "Scaffold Templates",
            ),
            shortcut="s",
        ),
        MenuItem(
            label="Serve Docs",
            description="Start MkDocs dev server on http://localhost:8000",
            action=lambda: _wrap_cmd(
                [
                    sys.executable, "-m", "mkdocs", "serve",
                    "--config-file",
                    str(repo_root / "implementation" / "docs" / "mkdocs.yml"),
                ],
                "Docs Server (Ctrl-C to stop)",
            ),
            shortcut="d",
        ),
        MenuItem(
            label="Build Check",
            description="Compile all Python files to check for syntax errors",
            action=lambda: _wrap_cmd(
                [sys.executable, "-m", "compileall", "-q", str(repo_root)],
                "Compile Check",
            ),
            shortcut="c",
        ),
    ]


if __name__ == "__main__":
    MonsterMenuApp(
        title="TUI Monster",
        version="v1.0",
        menu_items=_make_default_menu(),
    ).run()
