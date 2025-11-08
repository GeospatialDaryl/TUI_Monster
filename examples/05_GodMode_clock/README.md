# Example 05 – GodMode Clock

The GodMode clock is the flamboyant sibling of the live clock tutorial. It keeps
track of the current wall-clock time while orchestrating animated color palettes
and glyph constellations inspired by the `XMR_Godmode` briefing. The goal is to
show how the `pyTuiMonster` runtime can power a maximalist TUI with rotating
styling, unicode diversity, and runtime controls.

## New Concepts

* **Color choreography** – Uses a lifecycle hook to initialize multiple curses
  color pairs, then cycles them each frame or by user request.
* **Unicode glyph palettes** – Demonstrates how to rotate through historical,
  cultural, and emoji-based characters while keeping the layout responsive.
* **Runtime controls** – Adds keyboard bindings for toggling animation modes,
  switching glyph sets, and tuning the refresh cadence in real time.

## Running the Demo

```bash
python3 main.py
```

Make sure you execute the command inside `examples/05_GodMode_clock/`. Press `q`
to quit at any time.

## Keyboard Shortcuts

| Keys | Action |
| ---- | ------ |
| `c` | Toggle automatic color rotation. |
| `[` / `]` | Step backward/forward through the color palette. |
| `g` | Toggle automatic glyph rotation. |
| `{` / `}` | Cycle through the themed glyph constellations. |
| `+` / `-` | Speed up or slow down the refresh cadence. |
| `r` | Reset all animation settings to their defaults. |
| `q` | Exit the application. |

## Design Notes

* The example starts from the live clock template and layers on additional state
  for colors, glyph selection, and animation pacing.
* Glyph sets pull from box-drawing runes, futhark characters, East Asian
  numerals, and emoji to emphasize unicode breadth.
* The draw routine keeps a generous border and centered messaging so the clock
  resembles a "dragon wizard" dashboard rather than a minimal ticker.
* Status messaging doubles as feedback when users disable automation or tweak
  palettes, keeping the tutorial approachable despite the extra flair.
