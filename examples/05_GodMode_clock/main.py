"""Mythic GodMode clock showcasing color and glyph choreography."""

from __future__ import annotations

import curses
from datetime import datetime
import sys
from pathlib import Path
from typing import List

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pyTuiMonster import TuiConfig, TuiMonsterApp, key_binding, lifecycle_hook


class GodModeClock(TuiMonsterApp):
    """Render a rotating, colorized clock with swappable glyph palettes."""

    def __init__(self) -> None:
        super().__init__(TuiConfig(refresh_rate=0.25))
        self.current_time: str = ""
        self.tick: int = 0
        self.rotate_colors = True
        self.rotate_glyphs = True
        self.glyph_set_index = 0
        self.glyph_phase = 0
        self.color_index = 0
        self.status_message = "Summoning dragon wizard clock..."
        self._color_pairs: List[int] = []

        self.glyph_sets = [
            {
                "name": "Mythic Brass",  # box-drawing with celestial runes
                "corners": ("╔", "╗", "╚", "╝"),
                "horizontal": "═",
                "vertical": "║",
                "ring": list("◇◆◈◉◎✧✦✩"),
                "accent": ["⚚", "☿", "☽", "☾"],
            },
            {
                "name": "Runic Storm",
                "corners": ("ᚠ", "ᚦ", "ᚨ", "ᚱ"),
                "horizontal": "ᛜ",
                "vertical": "ᛞ",
                "ring": list("ᚠᚡᚢᚣᚤᚥᚦᚧ"),
                "accent": ["ᚨ", "ᛇ", "ᛟ", "ᛞ"],
            },
            {
                "name": "Silk Pavilion",  # East Asian inspired strokes
                "corners": ("╭", "╮", "╰", "╯"),
                "horizontal": "─",
                "vertical": "│",
                "ring": list("一二三四五六七八九十"),
                "accent": ["龍", "雲", "星", "火"],
            },
            {
                "name": "Astral Glyphics",  # emoji + symbols mashup
                "corners": ("✦", "✧", "✩", "✪"),
                "horizontal": "✶",
                "vertical": "✶",
                "ring": list("☄️⭐🌟✨💫🪐🔮⚡"),
                "accent": ["🐉", "🧙", "🌌", "🜂"],
            },
        ]

        self.color_palette = [
            (curses.COLOR_CYAN, -1),
            (curses.COLOR_MAGENTA, -1),
            (curses.COLOR_BLUE, -1),
            (curses.COLOR_GREEN, -1),
            (curses.COLOR_YELLOW, -1),
            (curses.COLOR_RED, -1),
        ]

    @lifecycle_hook("after_start")
    def _init_colors(self) -> None:
        if not curses.has_colors():
            self.status_message = "Terminal lacks color support; falling back to monochrome."
            return

        curses.start_color()
        curses.use_default_colors()
        self._color_pairs.clear()
        for index, (fg, bg) in enumerate(self.color_palette, start=1):
            try:
                curses.init_pair(index, fg, bg)
                self._color_pairs.append(curses.color_pair(index))
            except curses.error:
                continue

        if not self._color_pairs:
            self.status_message = "Color initialization failed; running in monochrome."
        else:
            self.status_message = "GodMode clock online."

    def update(self) -> None:
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tick += 1

        if self.rotate_colors and self._color_pairs:
            self.color_index = (self.color_index + 1) % len(self._color_pairs)

        active_ring = self.glyph_sets[self.glyph_set_index]["ring"]
        if self.rotate_glyphs and active_ring:
            self.glyph_phase = (self.glyph_phase + 1) % len(active_ring)

    def draw(self) -> None:
        self.clear()

        try:
            height, width = self.screen.getmaxyx()
        except curses.error:
            height, width = 0, 0

        if height < 10 or width < 40:
            self.addstr(0, 0, "Expand the window for the GodMode clock spectacle!")
            self.refresh()
            return

        attr = curses.A_BOLD
        if self._color_pairs:
            attr |= self._color_pairs[self.color_index]

        glyphs = self.glyph_sets[self.glyph_set_index]
        corners = glyphs["corners"]
        horizontal = glyphs["horizontal"]
        vertical = glyphs["vertical"]
        ring = glyphs["ring"]
        accent = glyphs["accent"]

        inner_width = width - 2
        top_fill = self._cycle_string(horizontal, ring, inner_width)
        bottom_fill = self._cycle_string(horizontal, list(reversed(ring)), inner_width)

        self.addstr(0, 0, corners[0] + top_fill + corners[1], attr)
        self.addstr(height - 1, 0, corners[2] + bottom_fill + corners[3], attr)

        for row in range(1, height - 1):
            interior = self._cycle_string(" ", ring, inner_width)
            line = f"{vertical}{interior}{vertical}"
            self.addstr(row, 0, line, attr)

        title = "XMR GodMode Dragon Wizard Clock"
        self._center_text(2, title, attr)
        self._center_text(4, self.current_time, attr | curses.A_BLINK if hasattr(curses, "A_BLINK") else attr)

        glyph_label = f"Glyphs: {glyphs['name']}"
        color_mode = "Auto" if self.rotate_colors else "Manual"
        glyph_mode = "Auto" if self.rotate_glyphs else "Manual"
        info_lines = [
            f"Color mode: {color_mode} | Glyph mode: {glyph_mode}",
            f"Palette index: {self.color_index + 1 if self._color_pairs else 0}/{len(self._color_pairs) or '—'}",
            f"Refresh rate: {self.config.refresh_rate:.2f}s",
            f"Status: {self.status_message}",
        ]

        for offset, text in enumerate([glyph_label, *info_lines]):
            self.addstr(6 + offset, 2, text[: inner_width])

        controls = [
            "Controls:",
            "  c – toggle color rotation",
            "  [ / ] – step palette backward/forward",
            "  g – toggle glyph rotation",
            "  { / } – cycle glyph sets backward/forward",
            "  + / - – adjust refresh rate",
            "  r – reset choreography",
            "  q – exit",
        ]
        for offset, text in enumerate(controls):
            self.addstr(6 + len(info_lines) + 2 + offset, 2, text[: inner_width])

        accent_char = accent[(self.tick // 5) % len(accent)] if accent else "*"
        signature = f"{accent_char} Embrace the bling {accent_char}"
        self._center_text(height - 3, signature, attr)

        self.refresh()

    def _center_text(self, row: int, text: str, attr: int) -> None:
        height, width = self.screen.getmaxyx()
        x = max(1, (width - len(text)) // 2)
        self.addstr(row, x, text[: width - 2], attr)

    def _cycle_string(self, fallback: str, ring: List[str], length: int) -> str:
        if length <= 0:
            return ""
        if not ring:
            return fallback * length
        return "".join(ring[(self.glyph_phase + i) % len(ring)] for i in range(length))

    @key_binding(ord("c"))
    def toggle_color_rotation(self, _: int) -> None:
        self.rotate_colors = not self.rotate_colors
        mode = "auto" if self.rotate_colors else "manual"
        self.status_message = f"Color rotation set to {mode}."

    @key_binding(ord("g"))
    def toggle_glyph_rotation(self, _: int) -> None:
        self.rotate_glyphs = not self.rotate_glyphs
        mode = "auto" if self.rotate_glyphs else "manual"
        self.status_message = f"Glyph rotation set to {mode}."

    @key_binding(ord("["))
    def previous_color(self, _: int) -> None:
        if not self._color_pairs:
            self.status_message = "No color palette available."
            return
        self.rotate_colors = False
        self.color_index = (self.color_index - 1) % len(self._color_pairs)
        self.status_message = "Stepped to previous color palette entry."

    @key_binding(ord("]"))
    def next_color(self, _: int) -> None:
        if not self._color_pairs:
            self.status_message = "No color palette available."
            return
        self.rotate_colors = False
        self.color_index = (self.color_index + 1) % len(self._color_pairs)
        self.status_message = "Stepped to next color palette entry."

    @key_binding(ord("{"))
    def previous_glyph_set(self, _: int) -> None:
        self.rotate_glyphs = False
        self.glyph_set_index = (self.glyph_set_index - 1) % len(self.glyph_sets)
        self.glyph_phase = 0
        self.status_message = "Selected previous glyph constellation."

    @key_binding(ord("}"))
    def next_glyph_set(self, _: int) -> None:
        self.rotate_glyphs = False
        self.glyph_set_index = (self.glyph_set_index + 1) % len(self.glyph_sets)
        self.glyph_phase = 0
        self.status_message = "Selected next glyph constellation."

    @key_binding(ord("+"))
    def increase_speed(self, _: int) -> None:
        self.config.refresh_rate = max(0.05, self.config.refresh_rate - 0.05)
        self.status_message = "Increased animation tempo."

    @key_binding(ord("-"))
    def decrease_speed(self, _: int) -> None:
        self.config.refresh_rate = min(1.0, self.config.refresh_rate + 0.05)
        self.status_message = "Decreased animation tempo."

    @key_binding(ord("r"))
    def reset(self, _: int) -> None:
        self.rotate_colors = True
        self.rotate_glyphs = True
        self.color_index = 0
        self.glyph_set_index = 0
        self.glyph_phase = 0
        self.config.refresh_rate = 0.25
        self.status_message = "Choreography reset to defaults."


if __name__ == "__main__":
    GodModeClock().run()
