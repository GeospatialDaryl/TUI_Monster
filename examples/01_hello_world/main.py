"""Interactive hello world that previews every TUI Monster tutorial mode."""

from __future__ import annotations

import curses
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pyTuiMonster import TuiConfig, TuiMonsterApp, key_binding, lifecycle_hook


@dataclass(frozen=True)
class PreviewMode:
    """Metadata and sample lines for one tutorial preview mode."""

    title: str
    lesson: str
    controls: str
    sample_lines: tuple[str, ...]


PREVIEW_MODES: tuple[PreviewMode, ...] = (
    PreviewMode(
        title="01 · Hello World",
        lesson="Render static text, then refresh the terminal buffer.",
        controls="No controls beyond q to quit.",
        sample_lines=(
            "Hello, TUI world!",
            "This is the smallest useful pyTuiMonster screen.",
        ),
    ),
    PreviewMode(
        title="02 · Live Clock",
        lesson="Update app state on a timer before each draw pass.",
        controls="The clock refreshes automatically.",
        sample_lines=(
            "Live Clock",
            "Current time: {current_time}",
        ),
    ),
    PreviewMode(
        title="03 · Counter",
        lesson="Attach keyboard shortcuts with @key_binding decorators.",
        controls="Use + / - or arrow keys in the full counter example.",
        sample_lines=(
            "Counter",
            "Current value: {counter}",
            "+ increments, - decrements",
        ),
    ),
    PreviewMode(
        title="04 · Task Tracker",
        lesson="Combine navigation, lifecycle hooks, styling, and collections.",
        controls="Use j/k, arrows, space, t, and x in the full task tracker.",
        sample_lines=(
            "Task Tracker",
            "-> [ ] Read project brief",
            "   [x] Sketch interface ideas",
            "   [ ] Build prototype",
        ),
    ),
    PreviewMode(
        title="05 · GodMode Clock",
        lesson="Preview colors, glyph storms, animation, and Unicode-safe rendering.",
        controls="Use c/g, ,/., [/], +/-, _, r, and s in the full GodMode clock.",
        sample_lines=(
            "🐉 GodMode Chronomancer",
            "Palette: Aurora Glyphstream",
            "Glyph set: Runic Ledger",
            "ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫ",
        ),
    ),
)


class HelloWorldTUI(TuiMonsterApp):
    """Render a guided hello-world launcher for every example mode."""

    def __init__(self, modes: Sequence[PreviewMode] = PREVIEW_MODES) -> None:
        if not modes:
            raise ValueError("HelloWorldTUI requires at least one preview mode")
        super().__init__(TuiConfig(refresh_rate=0.2))
        self.modes = tuple(modes)
        self.selected_mode = 0
        self.frame = 0
        self.status = "Press n/p, ←/→, Tab, or 1-5 to preview every mode."
        self.counter = 0
        self.current_time = ""

    @lifecycle_hook("after_start")
    def announce_preview(self) -> None:
        self.status = "Hello World mode preview is ready."

    def update(self) -> None:
        self.frame += 1
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.counter = (self.frame // 5) % 100

    @key_binding(ord("n"), ord("\t"), curses.KEY_RIGHT)
    def next_mode(self, _: int) -> None:
        self.selected_mode = (self.selected_mode + 1) % len(self.modes)
        self.status = f"Previewing {self.active_mode.title}."

    @key_binding(ord("p"), curses.KEY_LEFT)
    def previous_mode(self, _: int) -> None:
        self.selected_mode = (self.selected_mode - 1) % len(self.modes)
        self.status = f"Previewing {self.active_mode.title}."

    @key_binding(ord("1"), ord("2"), ord("3"), ord("4"), ord("5"))
    def jump_to_mode(self, key: int) -> None:
        requested_index = key - ord("1")
        if requested_index >= len(self.modes):
            self.status = "That preview slot is not available in this build."
            return
        self.selected_mode = requested_index
        self.status = f"Jumped to {self.active_mode.title}."

    @property
    def active_mode(self) -> PreviewMode:
        return self.modes[self.selected_mode]

    def rendered_sample_lines(self) -> tuple[str, ...]:
        """Return the active sample with live placeholders filled in."""

        return tuple(
            line.format(current_time=self.current_time or "warming up", counter=self.counter)
            for line in self.active_mode.sample_lines
        )

    def mode_tabs(self) -> str:
        """Build a compact tab row showing all available preview modes."""

        labels = []
        for index, mode in enumerate(self.modes):
            label = mode.title.split(" · ", maxsplit=1)[0]
            labels.append(f"[{label}]" if index == self.selected_mode else f" {label} ")
        return " ".join(labels)

    def draw(self) -> None:
        self.clear()
        max_y, _ = self.screen.getmaxyx()
        mode = self.active_mode

        self.center_text(0, "TUI Monster · Hello World Mode Preview", curses.A_BOLD)
        self.center_text(2, self.mode_tabs())
        self.center_text(4, mode.title, curses.A_BOLD)
        self.center_text(5, mode.lesson)
        self.center_text(6, mode.controls)

        preview_top = 9
        self.center_text(preview_top - 1, "┌─ Preview ─────────────────────────────┐")
        for offset, line in enumerate(self.rendered_sample_lines()):
            y = preview_top + offset
            if y >= max_y - 4:
                break
            self.center_text(y, line)
        self.center_text(
            preview_top + len(self.rendered_sample_lines()) + 1,
            "└───────────────────────────────────────┘",
        )

        footer = "n/Tab/→ next · p/← previous · 1-5 jump · q quit"
        if max_y >= 3:
            self.center_text(max_y - 3, self.status)
            self.center_text(max_y - 2, footer)
        self.refresh()


if __name__ == "__main__":
    HelloWorldTUI().run()
