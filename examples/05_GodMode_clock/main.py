"""Dragon wizard clock with rotating palettes and glyph storms."""

from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import curses

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pyTuiMonster import TuiConfig, TuiMonsterApp, key_binding, lifecycle_hook


Palette = Tuple[str, int, int]


class GodModeClockTUI(TuiMonsterApp):
    """A maximalist chronometer that celebrates every Unicode plane."""

    def __init__(self) -> None:
        super().__init__(TuiConfig(refresh_rate=0.05))
        self._color_palettes: List[Palette] = [
            ("Aurora Glyphstream", curses.COLOR_CYAN, curses.COLOR_BLACK),
            ("Solar Sigils", curses.COLOR_YELLOW, curses.COLOR_RED),
            ("Nether Runes", curses.COLOR_MAGENTA, curses.COLOR_BLUE),
            ("Forest Spirits", curses.COLOR_GREEN, curses.COLOR_BLACK),
            ("Crystal Lattice", curses.COLOR_WHITE, curses.COLOR_MAGENTA),
            ("Ember Crown", curses.COLOR_RED, curses.COLOR_BLACK),
        ]
        self._glyph_sets = [
            {
                "name": "Runic Ledger",
                "description": "Elder Futhark characters evoking ancient trade winds.",
                "chars": "ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯᚰᚱᚲᚳᚴᚵᚶᚷᚸ",
            },
            {
                "name": "Alchemical Bloom",
                "description": "Occult circles and planetary metals for wizardly flair.",
                "chars": "☉☾☿♀♁♂♃♄♅♆♇⚕⚚⚝⚕⚘⚚⚝",
            },
            {
                "name": "Mythic Dragons",
                "description": "CJK dragons, spirits, and protective beasts.",
                "chars": "龍龘靈麒麟鳳凰鸞鵬麒龑龖龗龞",
            },
            {
                "name": "Astral Braille",
                "description": "Braille constellations rotating through the cosmos.",
                "chars": "⠁⠃⠋⠛⠓⠟⠿⠾⠽⠮⠯⠷⠿",
            },
            {
                "name": "Cyber Katakana",
                "description": "Katakana syllables pulsing like a synthwave HUD.",
                "chars": "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎ",
            },
            {
                "name": "Heraldic Glyphs",
                "description": "Combines dingbats and chess pieces for regal drama.",
                "chars": "♔♕♖♗♘♙♚♛♜♝♞♟☩☧☨☦☥☬☫",
            },
        ]
        self._has_colors = False
        self._color_index = 0
        self._glyph_index = 0
        self._swirl_offset = 0
        self._rotation_speed = 1.0
        self._glyph_speed = 1.5
        self._swirl_speed = 0.2
        self._last_color_switch = time.monotonic()
        self._last_glyph_switch = time.monotonic()
        self._last_swirl = time.monotonic()
        self._rotate_colors = True
        self._rotate_glyphs = True
        self._status = "Dragon wizard clock awaiting commands."
        self._current_time = ""

    @lifecycle_hook("after_start")
    def _initialize_colors(self) -> None:
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            for idx, (_, fg, bg) in enumerate(self._color_palettes, start=1):
                curses.init_pair(idx, fg, bg)
            self._has_colors = True
            self._status = "Color reactor calibrated."
        else:
            self._status = "Terminal lacks color support; monochrome engaged."

    def update(self) -> None:
        now = time.monotonic()
        self._current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if (
            self._rotate_colors
            and self._has_colors
            and now - self._last_color_switch >= self._rotation_speed
        ):
            self._color_index = (self._color_index + 1) % len(self._color_palettes)
            self._last_color_switch = now

        if self._rotate_glyphs and now - self._last_glyph_switch >= self._glyph_speed:
            self._glyph_index = (self._glyph_index + 1) % len(self._glyph_sets)
            self._last_glyph_switch = now

        if self._swirl_speed > 0 and now - self._last_swirl >= self._swirl_speed:
            self._swirl_offset = (self._swirl_offset + 1) % len(self._glyph_sets[self._glyph_index]["chars"])
            self._last_swirl = now

    def draw(self) -> None:
        self.clear()
        max_y, max_x = self.screen.getmaxyx()
        palette_name, attr = self._active_palette()
        glyph_info = self._glyph_sets[self._glyph_index]

        title = "🐉 GodMode Chronomancer"
        subtitle = "Rotating Dragon Wizard Clock"
        self._center_text(0, title, attr | curses.A_BOLD if attr else curses.A_BOLD)
        self._center_text(1, subtitle, attr)

        time_line = f"Current time: {self._current_time}"
        self._center_text(3, time_line, attr)

        self._center_text(5, f"Palette: {palette_name}", attr)
        self._center_text(6, f"Glyph set: {glyph_info['name']}", attr)
        self._center_text(7, glyph_info["description"], attr)

        swirl = self._build_swirl_line(glyph_info["chars"], max_x)
        halo_y_start = max_y // 2 - 2
        for idx, line in enumerate(swirl):
            self._center_text(halo_y_start + idx, line, attr | curses.A_BOLD if attr else curses.A_BOLD)

        instructions = [
            "Controls: q quit | c toggle colors | g toggle glyphs | ,/. cycle colors | [/] cycle glyphs",
            "Speed: +/- faster | _ slower | r reset | s toggle swirl",
            f"Status: {self._status}",
        ]
        for idx, line in enumerate(instructions, start=max_y - 4):
            if idx < max_y:
                self._center_text(idx, line, attr)

        self.refresh()

    def _active_palette(self) -> Tuple[str, int | None]:
        name, fg, bg = self._color_palettes[self._color_index]
        if not self._has_colors:
            return name, None
        pair = curses.color_pair(self._color_index + 1)
        return name, pair

    def _build_swirl_line(self, glyphs: str, width: int) -> List[str]:
        if not glyphs:
            return ["(no glyphs configured)"]
        usable_width = max(width - 4, 1)
        base_length = len(glyphs)
        extended = glyphs * ((usable_width // base_length) + 3)
        offset = self._swirl_offset % base_length
        segment = extended[offset : offset + usable_width]
        if len(segment) < usable_width:
            segment = segment.ljust(usable_width)
        reverse = segment[::-1]
        shift = (offset // 2) % base_length
        secondary = extended[shift : shift + usable_width]
        if len(secondary) < usable_width:
            secondary = secondary.ljust(usable_width)
        return [segment, reverse, secondary]

    def _center_text(self, y: int, text: str, attr: int | None) -> None:
        self.center_text(y, text, attr)

    @key_binding(ord("c"))
    def toggle_colors(self, _: int) -> None:
        if not self._has_colors:
            self._status = "Color rotation unavailable in monochrome mode."
            return
        self._rotate_colors = not self._rotate_colors
        state = "resumed" if self._rotate_colors else "paused"
        self._status = f"Color cycling {state}."

    @key_binding(ord("g"))
    def toggle_glyphs(self, _: int) -> None:
        self._rotate_glyphs = not self._rotate_glyphs
        state = "resumed" if self._rotate_glyphs else "paused"
        self._status = f"Glyph cycling {state}."

    @key_binding(ord(","))
    def previous_palette(self, _: int) -> None:
        self._color_index = (self._color_index - 1) % len(self._color_palettes)
        self._rotate_colors = False
        self._status = "Selected previous palette manually."

    @key_binding(ord("."))
    def next_palette(self, _: int) -> None:
        self._color_index = (self._color_index + 1) % len(self._color_palettes)
        self._rotate_colors = False
        self._status = "Selected next palette manually."

    @key_binding(ord("["))
    def previous_glyph_set(self, _: int) -> None:
        self._glyph_index = (self._glyph_index - 1) % len(self._glyph_sets)
        self._rotate_glyphs = False
        self._swirl_offset %= len(self._glyph_sets[self._glyph_index]["chars"])
        self._status = "Selected previous glyph constellation."

    @key_binding(ord("]"))
    def next_glyph_set(self, _: int) -> None:
        self._glyph_index = (self._glyph_index + 1) % len(self._glyph_sets)
        self._rotate_glyphs = False
        self._swirl_offset %= len(self._glyph_sets[self._glyph_index]["chars"])
        self._status = "Selected next glyph constellation."

    @key_binding(ord("+"), ord("="))
    def accelerate(self, _: int) -> None:
        self._rotation_speed = max(0.1, self._rotation_speed - 0.1)
        self._glyph_speed = max(0.2, self._glyph_speed - 0.1)
        self._swirl_speed = max(0.05, self._swirl_speed - 0.02)
        self._status = "Increased temporal cadence."

    @key_binding(ord("-"))
    def decelerate(self, _: int) -> None:
        self._rotation_speed = min(5.0, self._rotation_speed + 0.1)
        self._glyph_speed = min(5.0, self._glyph_speed + 0.1)
        self._swirl_speed = min(1.0, self._swirl_speed + 0.02)
        self._status = "Decreased temporal cadence."

    @key_binding(ord("_"))
    def slow_roll(self, _: int) -> None:
        self._rotation_speed = min(10.0, self._rotation_speed + 0.5)
        self._glyph_speed = min(10.0, self._glyph_speed + 0.5)
        self._swirl_speed = min(1.5, self._swirl_speed + 0.05)
        self._status = "Entered slow-roll observatory mode."

    @key_binding(ord("r"))
    def reset(self, _: int) -> None:
        self._rotation_speed = 1.0
        self._glyph_speed = 1.5
        self._swirl_speed = 0.2
        self._rotate_colors = True and self._has_colors
        self._rotate_glyphs = True
        self._swirl_offset = 0
        now = time.monotonic()
        self._last_color_switch = now
        self._last_glyph_switch = now
        self._last_swirl = now
        self._status = "Reset cadence and resumed automatic cycling."

    @key_binding(ord("s"))
    def toggle_swirl(self, _: int) -> None:
        if self._swirl_speed == 0:
            self._swirl_speed = 0.2
            self._last_swirl = time.monotonic()
            self._status = "Swirl reactivated."
        else:
            self._swirl_speed = 0
            self._status = "Swirl paused for inspection."


if __name__ == "__main__":
    GodModeClockTUI().run()
