# Training Notes (Non-Functional)

This directory holds **design notes and investigation material only**. Nothing
in it is part of the `pyTuiMonster` package, and nothing in it is runnable
from this repository.

- `XMR_Godmode.sh` is a launcher script for an external `crypto_monkey`
  Python package that is **not** included here (and is not on PyPI as a
  dependency of this project). The script will exit with an import error
  unless you supply that package yourself.
- `analysis_XMR_Godmode.MD` is an exploratory memo about that external
  tooling. It describes infrastructure (e.g. `~/DataField/XMR_Data/`) that
  does not exist in this repository.

If the XMR_Godmode work matures, it should move to its own repository. It is
kept here purely as a reference for a possible future `TuiMonsterApp`-based
dashboard example.
