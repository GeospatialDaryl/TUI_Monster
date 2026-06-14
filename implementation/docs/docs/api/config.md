# TuiConfig

```python
from pyTuiMonster import TuiConfig
```

Dataclass holding runtime configuration for a [`TuiMonsterApp`](app.md).

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass
class TuiConfig:
    refresh_rate: float = 1 / 30
    stop_keys: Tuple[int, ...] = (ord('q'),)
```

---

## Fields

### `refresh_rate: float`

Seconds between frames. Default: `1/30` (~33 ms, 30 fps).

| Value | Effect |
|-------|--------|
| `1/30` | 30 fps — default, smooth for most UIs |
| `0.5` | 2 fps — suitable for low-activity monitors |
| `1.0` | 1 fps — clock-style updates |
| `0` | Uncapped — runs as fast as possible (CPU-bound) |

### `stop_keys: Tuple[int, ...]`

Key codes that trigger `app.stop()`. Default: `(ord('q'),)`.

To require `Ctrl-C` only (no `q`):

```python
import signal
TuiConfig(stop_keys=())   # disable key-based stop; rely on SIGINT
```

To add `Escape` as a second quit key:

```python
TuiConfig(stop_keys=(ord('q'), 27))   # 27 = ESC
```

---

## Examples

```python
# Fast clock — 1 fps, Escape to quit
from pyTuiMonster import TuiConfig
cfg = TuiConfig(refresh_rate=1.0, stop_keys=(ord('q'), 27))

# Realtime dashboard — 60 fps
cfg = TuiConfig(refresh_rate=1/60)

# Interactive app — default config
cfg = TuiConfig()
```

---

## Changing Config at Runtime

`TuiMonsterApp.config` is read-write. Update fields during a session:

```python
@key_binding(ord('s'))
def slow_down(self, key):
    self.config.refresh_rate = 1.0
```
