"""Script wrapper: run any command inside a live TUI output viewer."""

from __future__ import annotations

import argparse
import curses
import os
import select
import subprocess
import time
from typing import Dict, List, Optional, Sequence, Union

from pyTuiMonster import TuiMonsterApp, TuiConfig, key_binding, lifecycle_hook


class ScriptWrapperApp(TuiMonsterApp):
    """TUI wrapper that streams subprocess output with scroll and status."""

    def __init__(
        self,
        command: Union[str, Sequence[str]],
        title: str = "",
        env: Optional[Dict[str, str]] = None,
        config: Optional[TuiConfig] = None,
    ) -> None:
        super().__init__(config or TuiConfig(refresh_rate=1 / 15))
        self._command = command
        self._title = title or (command if isinstance(command, str) else " ".join(command))
        self._env = {**os.environ, **(env or {})}
        self._lines: List[str] = []
        self._proc: Optional[subprocess.Popen] = None  # type: ignore[type-arg]
        self._status = "pending"
        self._exit_code: Optional[int] = None
        self._start_time: Optional[float] = None
        self._elapsed = 0.0
        self._scroll_offset = 0
        self._auto_scroll = True

    # ------------------------------------------------------------------
    # Lifecycle

    @lifecycle_hook("after_start")
    def _init_colors(self) -> None:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)   # RUNNING badge
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)    # DONE badge
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)      # FAILED badge
        curses.init_pair(4, curses.COLOR_CYAN, -1)                     # header title
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)    # footer bar
        curses.init_pair(6, curses.COLOR_YELLOW, -1)                   # elapsed
        curses.curs_set(0)

    @lifecycle_hook("after_start")
    def _launch_process(self) -> None:
        self._lines = []
        self._scroll_offset = 0
        self._auto_scroll = True
        self._start_time = time.monotonic()
        self._status = "running"
        self._proc = subprocess.Popen(
            self._command,
            shell=isinstance(self._command, str),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=self._env,
        )

    # ------------------------------------------------------------------
    # State update — drain stdout non-blocking

    def update(self) -> None:
        if self._proc is None:
            return
        if self._start_time is not None:
            self._elapsed = time.monotonic() - self._start_time
        # Drain available output without blocking
        while self._proc.stdout:
            ready, _, _ = select.select([self._proc.stdout], [], [], 0)
            if not ready:
                break
            line = self._proc.stdout.readline()
            if not line:
                break
            self._lines.append(line.rstrip("\n"))
            if self._auto_scroll:
                self._clamp_scroll_to_bottom()

        if self._proc.poll() is not None and self._status == "running":
            # Drain remaining output after process exits
            remaining = self._proc.stdout.read() if self._proc.stdout else ""
            for line in remaining.splitlines():
                self._lines.append(line)
            self._exit_code = self._proc.returncode
            self._status = "done" if self._exit_code == 0 else "failed"
            if self._auto_scroll:
                self._clamp_scroll_to_bottom()

    # ------------------------------------------------------------------
    # Rendering

    def draw(self) -> None:
        self.clear()
        h, w = self.screen.getmaxyx()
        self._draw_header(w)
        self._draw_output(h, w)
        self._draw_footer(h, w)
        self.refresh()

    def _draw_header(self, w: int) -> None:
        badge_text, badge_attr = self._badge()
        elapsed_str = f" {self._elapsed:.1f}s"
        title_text = f" {self._title}"

        # Fill header row
        self.addstr(0, 0, " " * w, curses.color_pair(4) | curses.A_BOLD)
        self.addstr(0, 0, title_text, curses.color_pair(4) | curses.A_BOLD)

        # Badge on the right
        badge_col = w - len(badge_text) - len(elapsed_str) - 2
        if badge_col > len(title_text):
            self.addstr(0, badge_col, badge_text, badge_attr | curses.A_BOLD)
            self.addstr(0, badge_col + len(badge_text), elapsed_str, curses.color_pair(6))

    def _draw_output(self, h: int, w: int) -> None:
        log_rows = h - 3  # header + separator + footer
        visible = self._lines[self._scroll_offset: self._scroll_offset + log_rows]
        # Separator
        self.addstr(1, 0, "─" * w, curses.A_DIM)
        for i, line in enumerate(visible):
            display = line[:w - 1] if len(line) >= w else line
            self.addstr(i + 2, 0, display)

    def _draw_footer(self, h: int, w: int) -> None:
        scroll_info = (
            f" line {self._scroll_offset + 1}/{len(self._lines)}"
            if self._lines else " (no output)"
        )
        auto_tag = " [auto]" if self._auto_scroll else ""
        keys = "↑↓/jk scroll  PgUp/PgDn  a auto-scroll  q quit"
        footer = f"{keys}{auto_tag}{scroll_info}"
        self.addstr(h - 1, 0, " " * w, curses.color_pair(5))
        self.addstr(h - 1, 1, footer[:w - 2], curses.color_pair(5))

    def _badge(self) -> tuple[str, int]:
        if self._status == "running":
            return "● RUNNING", curses.color_pair(1)
        if self._status == "done":
            return "✓ DONE", curses.color_pair(2)
        failed_code = f"({self._exit_code})" if self._exit_code is not None else ""
        return f"✗ FAILED{failed_code}", curses.color_pair(3)

    # ------------------------------------------------------------------
    # Key handlers

    @key_binding(curses.KEY_UP, ord('k'))
    def scroll_up(self, key: int) -> None:
        self._scroll_offset = max(0, self._scroll_offset - 1)
        self._auto_scroll = False

    @key_binding(curses.KEY_DOWN, ord('j'))
    def scroll_down(self, key: int) -> None:
        h, _ = self.screen.getmaxyx()
        log_rows = h - 3
        max_offset = max(0, len(self._lines) - log_rows)
        self._scroll_offset = min(max_offset, self._scroll_offset + 1)
        if self._scroll_offset >= max_offset:
            self._auto_scroll = True

    @key_binding(curses.KEY_PPAGE)
    def page_up(self, key: int) -> None:
        h, _ = self.screen.getmaxyx()
        self._scroll_offset = max(0, self._scroll_offset - (h - 3))
        self._auto_scroll = False

    @key_binding(curses.KEY_NPAGE)
    def page_down(self, key: int) -> None:
        h, _ = self.screen.getmaxyx()
        log_rows = h - 3
        max_offset = max(0, len(self._lines) - log_rows)
        self._scroll_offset = min(max_offset, self._scroll_offset + log_rows)
        if self._scroll_offset >= max_offset:
            self._auto_scroll = True

    @key_binding(ord('a'))
    def enable_auto_scroll(self, key: int) -> None:
        self._auto_scroll = True
        self._clamp_scroll_to_bottom()

    # ------------------------------------------------------------------
    # Helpers

    def _clamp_scroll_to_bottom(self) -> None:
        if not self.running:
            return
        try:
            h, _ = self.screen.getmaxyx()
        except Exception:
            return
        log_rows = h - 3
        self._scroll_offset = max(0, len(self._lines) - log_rows)


# ---------------------------------------------------------------------------
# Public convenience function

def run_wrapped(
    command: Union[str, Sequence[str]],
    title: str = "",
    env: Optional[Dict[str, str]] = None,
) -> int:
    """Run *command* inside a TUI wrapper and return the exit code."""
    app = ScriptWrapperApp(command=command, title=title, env=env)
    app.run()
    return app._exit_code if app._exit_code is not None else -1


# ---------------------------------------------------------------------------
# CLI entry point

def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="wrap",
        description="Run a command inside a live TUI output viewer.",
    )
    parser.add_argument("--title", default="", help="Header title")
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run (after optional --)",
    )
    args = parser.parse_args()

    cmd = args.command
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        parser.error("No command specified. Usage: wrap [--title TEXT] -- COMMAND")

    raise SystemExit(run_wrapped(command=cmd, title=args.title))


if __name__ == "__main__":
    _cli()
