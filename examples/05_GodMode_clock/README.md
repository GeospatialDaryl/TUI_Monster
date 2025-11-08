# Example 05: GodMode Clock

The GodMode clock turns the tame live clock into an interdimensional spectacle.
It layers rotating unicode glyph wheels, animated color palettes, and live time
tracking to mirror the dramatic aesthetic aspirations behind XMR_Godmode.

## Concepts introduced

- Managing multiple color palettes and gracefully degrading when the terminal
  lacks color support.
- Cycling through curated unicode character sets that reference diverse
  historical and cultural alphabets.
- Combining state toggles (`bling`, auto palette cycling) with status messaging
  to keep the user oriented while experimenting.
- Centering text and composing symmetrical decorative bands to mimic the visual
  polish of tools like `btop` and `btopper`.

## Controls

| Key | Action |
| --- | ------ |
| `c` | Cycle to the next color palette. |
| `g` | Rotate to the next unicode glyph set. |
| `b` | Toggle the animated glyph halo on and off. |
| `a` | Enable or disable automatic color palette cycling. |
| `h` | Show a quick reminder of the control scheme. |
| `q` | Quit the application. |

## Running the example

From the project root, execute:

```bash
python examples/05_GodMode_clock/main.py
```

If your terminal supports color, you will see the palette rotate every few
frames. Even without color support the glyph halo and status readouts remain,
providing a maximalist monochrome rendition.
