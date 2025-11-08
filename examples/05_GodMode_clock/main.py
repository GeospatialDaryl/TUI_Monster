"""GodMode clock example celebrating maximalist unicode bling."""

from __future__ import annotations

from datetime import datetime
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import curses

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pyTuiMonster import (
    TuiConfig,
    TuiMonsterApp,
    key_binding,
    lifecycle_hook,
)

Palette = Tuple[str, Tuple[int, int], Tuple[int, int]]
CharacterSet = Tuple[str, Sequence[str]]

PALETTES: List[Palette] = [
    ("Obsidian Prism", (curses.COLOR_CYAN, -1), (curses.COLOR_MAGENTA, -1)),
    ("Solar Forge", (curses.COLOR_YELLOW, curses.COLOR_RED), (curses.COLOR_WHITE, curses.COLOR_RED)),
    ("Deep Space", (curses.COLOR_BLUE, -1), (curses.COLOR_WHITE, -1)),
    ("Verdant Runes", (curses.COLOR_GREEN, -1), (curses.COLOR_BLACK, curses.COLOR_GREEN)),
    ("Aether Sparks", (curses.COLOR_MAGENTA, curses.COLOR_BLACK), (curses.COLOR_CYAN, curses.COLOR_BLACK)),
]

CHARSET_LIBRARY: List[CharacterSet] = [
    ("Braille Pulses", list("⠁⠃⠇⠏⠟⠿⡿⣿")),
    ("Box Glyph Array", list("┌┐└┘├┤┬┴┼─━│┃╱╲╳")),
    ("Katakana Stream", list("ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄ")),
    ("Runic Wheel", list("ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛏᛒᛖᛗᛚᛟᛞ")),
    ("Alchemy Sigils", list("🜁🜂🜃🜄🜇🜍🜔🜕🜖🜚🜛🜜🜝")),
    ("Astrology Orbit", list("♈♉♊♋♌♍♎♏♐♑♒♓")),
    ("Mahjong Winds", list("🀀🀁🀂🀃🀄🀅🀆🀇🀈🀉🀊🀋🀌🀍🀎🀏")),
]


class GodModeClockTUI(TuiMonsterApp):
    """Showcase a rotating unicode clock with color palettes and glyph wheels."""

    def __init__(self) -> None:
        super().__init__(TuiConfig(refresh_rate=0.15))
        self.current_time: str = ""
        self.palette_index = 0
        self.charset_index = 0
        self.bling_enabled = True
        self.auto_cycle_colors = True
        self.status = "Spooling interdimensional glyphs..."
        self._glyph_offset = 0
        self._frame = 0
        self._supports_color = False
        self._palette_pairs: List[Tuple[int, int]] = []

    @lifecycle_hook("after_start")
    def _initialize_colors(self) -> None:
        self._supports_color = curses.has_colors()
        if not self._supports_color:
            self.status = "Terminal lacks color support; falling back to monochrome."
            return

        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass

        self._palette_pairs.clear()
        for idx, (_, primary, accent) in enumerate(PALETTES):
            primary_id = idx * 2 + 1
            accent_id = primary_id + 1
            try:
                curses.init_pair(primary_id, primary[0], primary[1])
                curses.init_pair(accent_id, accent[0], accent[1])
            except curses.error:
                # Fallback to default colors if initialization fails.
                curses.init_pair(primary_id, curses.COLOR_WHITE, curses.COLOR_BLACK)
                curses.init_pair(accent_id, curses.COLOR_CYAN, curses.COLOR_BLACK)
            self._palette_pairs.append((primary_id, accent_id))

        self.status = "GodMode clock online. Press 'h' for help."

    def update(self) -> None:
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        glyphs = CHARSET_LIBRARY[self.charset_index][1]
        if glyphs and self.bling_enabled:
            self._glyph_offset = (self._glyph_offset + 1) % len(glyphs)
        self._frame += 1
        if (
            self.auto_cycle_colors
            and self._supports_color
            and self._palette_pairs
            and self._frame % 12 == 0
        ):
            self.palette_index = (self.palette_index + 1) % len(self._palette_pairs)

    def draw(self) -> None:
        self.clear()
        screen = self.screen
        height, width = screen.getmaxyx()
        title = "XMR GodMode Chronomancer"
        self._write_centered(0, title, self._attr(curses.A_BOLD))

        # Compose the glyph halo.
        glyph_name, glyphs = CHARSET_LIBRARY[self.charset_index]
        halo_span = max(10, min(width - 4, len(glyphs) * 2)) if glyphs else 0
        if halo_span and self.bling_enabled:
            halo = "".join(
                glyphs[(self._glyph_offset + idx) % len(glyphs)]
                for idx in range(halo_span)
            )
            self._write_centered(2, halo, self._attr())
            self._write_centered(4, halo[::-1], self._attr(accent=True))
        else:
            self._write_centered(3, "(bling disabled)", self._attr(curses.A_DIM))

        # Render the clock body.
        time_line = f"⏱  {self.current_time}"
        self._write_centered(6, time_line, self._attr(curses.A_BOLD))
        palette_name = PALETTES[self.palette_index][0]
        palette_line = f"Palette: {palette_name}"
        charset_line = f"Glyph set: {glyph_name}"
        self._write_centered(8, palette_line, self._attr())
        self._write_centered(9, charset_line, self._attr(accent=True))

        # Status and controls.
        controls = "[c]olor  [g]lyphs  [b]ling  [a]uto  [h]elp  [q]uit"
        self._write_centered(height - 3, controls, self._attr(curses.A_DIM))
        status_line = self.status
        self._write_centered(height - 2, status_line, self._attr())

        self.refresh()

    def _write_centered(self, y: int, text: str, attr: Optional[int]) -> None:
        screen = self.screen
        height, width = screen.getmaxyx()
        if y < 0 or y >= height:
            return
        x = max(0, (width - len(text)) // 2)
        self.addstr(y, x, text, attr)

    def _attr(self, base: int = 0, *, accent: bool = False) -> int | None:
        attr = base
        if self._supports_color and self._palette_pairs:
            pair = self._palette_pairs[self.palette_index][1 if accent else 0]
            attr |= curses.color_pair(pair)
        return attr or None

    @key_binding(ord("c"))
    def cycle_palette(self, _: int) -> None:
        if not self._supports_color or not self._palette_pairs:
            self.status = "Color cycling unavailable in this terminal."
            return
        self.palette_index = (self.palette_index + 1) % len(self._palette_pairs)
        self.status = f"Palette set to {PALETTES[self.palette_index][0]}"

    @key_binding(ord("g"))
    def cycle_charset(self, _: int) -> None:
        self.charset_index = (self.charset_index + 1) % len(CHARSET_LIBRARY)
        self.status = f"Glyph wheel set to {CHARSET_LIBRARY[self.charset_index][0]}"

    @key_binding(ord("b"))
    def toggle_bling(self, _: int) -> None:
        self.bling_enabled = not self.bling_enabled
        state = "enabled" if self.bling_enabled else "paused"
        self.status = f"Bling {state}."

    @key_binding(ord("a"))
    def toggle_auto_cycle(self, _: int) -> None:
        self.auto_cycle_colors = not self.auto_cycle_colors
        state = "on" if self.auto_cycle_colors else "off"
        self.status = f"Auto palette cycling {state}."

    @key_binding(ord("h"))
    def show_help(self, _: int) -> None:
        self.status = (
            "Use c/g/b/a to control the chromatic dragon clock. Press q to exit."
        )


if __name__ == "__main__":
    GodModeClockTUI().run()
