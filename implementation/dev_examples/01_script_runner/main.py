"""Dev example 01 — wrap a shell command with live streaming TUI output.

Run:
    python implementation/dev_examples/01_script_runner/main.py

Demonstrates:
- ScriptWrapperApp for live process streaming
- Auto-scroll behaviour
- Color-coded exit status badge
- Scroll controls
"""

import sys
from pathlib import Path

# Allow running from the repo root without installing
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from implementation.tools.wrap import run_wrapped


def main() -> None:
    # Simulate a multi-second build with mixed output
    script = (
        "for i in $(seq 1 20); do "
        "  echo \"Step $i/20: processing...\"; "
        "  sleep 0.15; "
        "done; "
        "echo ''; "
        "echo 'Build complete.'"
    )
    exit_code = run_wrapped(
        command=script,
        title="Example Build Script",
    )
    print(f"\nExit code: {exit_code}")


if __name__ == "__main__":
    main()
