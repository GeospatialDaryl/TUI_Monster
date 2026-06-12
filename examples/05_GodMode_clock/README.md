# 05 – GodMode Clock

The GodMode clock is a maximalist remix of the live clock tutorial. It keeps the
core cadence of regularly updating the current time but layers on rotating color
schemes, exotic Unicode glyph constellations, and swirl animations. Use it to
experiment with how far you can push `TuiMonsterApp` styling while keeping the
interface responsive.

## Concepts Introduced

- Decorating lifecycle hooks to configure curses color support as soon as the
  screen is available.
- Managing multiple concurrent animation timers (palette rotation, glyph set
  cycling, swirl offsets) inside `update()` using `time.monotonic()`.
- Centering dynamic text and drawing symmetrical halos of Unicode characters to
  mimic the glowing gauges of the original btop++ UI.
- Exposing rich runtime controls through key bindings so operators can dial the
  "bling" up or down in real time.

## Running the Example

From the repository root:

```bash
python3 examples/05_GodMode_clock/main.py
```

The script will adjust `sys.path` automatically so the local `pyTuiMonster`
package can be imported. Press `q` at any time to quit.

## Controls

| Key(s) | Action |
| ------ | ------ |
| `q` | Exit the application. |
| `c` | Toggle automatic color palette rotation. |
| `,` / `.` | Step through color palettes manually (pauses auto rotation). |
| `g` | Toggle glyph constellation cycling. |
| `[` / `]` | Step through glyph constellations manually (pauses auto rotation). |
| `+` / `=` | Increase animation speed (faster color, glyph, and swirl updates). |
| `-` | Slightly slow animations for easier inspection. |
| `_` | Enter slow-roll mode for very relaxed updates. |
| `r` | Reset speeds and resume all automatic cycling. |
| `s` | Toggle the swirling halo animation. |

## Suggested Experiments

1. Pause the palette rotation with `c` and fine tune the glyph selections to
   find combinations that pair well with your terminal theme.
2. Speed everything up with `+` to create a frantic dragon-wizard chronometer,
   then drop into `_` slow-roll mode to observe how the Unicode sets render in
   your environment.
3. Add your own glyph constellation in `main.py` by appending to
   `self._glyph_sets`—try musical notation, mathematical operators, or regional
   scripts that align with your project branding.

## Decision Log

- Styled the tutorial name as "GodMode" to align with the XMR_Godmode training
  narrative while focusing on price monitoring aesthetics rather than mining.
- Reused the live clock foundation to keep the learning curve gentle, adding one
  major feature per control cluster (colors, glyphs, swirl).
- Centered all copy and halos to echo the polished layout of btop++.
- Selected glyph sets from a variety of historical and cultural scripts to
  emphasize Unicode breadth and to encourage localization testing.
- Bound manual palette/glyph navigation to punctuation keys so the left hand can
  stay near `q` while exploring the available styles.
