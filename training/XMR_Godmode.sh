#!/usr/bin/env bash
# xmr-godmode.sh — Redonkulous XMR TUI launcher around the Python3 engine
#
# Requirements:
#   - python3
#   - crypto_monkey package/module available on PYTHONPATH
#
# Defaults:
#   - Symbol: XMR
#   - Source: coindesk
#   - Interval: 15s
#   - Mode: ionizer (Z-score / analytics)
#   - Theme: runic (max Unicode glimmer)

set -euo pipefail

# ---------- Defaults ----------
SYMBOL="${SYMBOL:-XMR}"
SOURCE="${SOURCE:-coindesk}"   # coindesk | yahoo | history
INTERVAL="${INTERVAL:-15}"
MODE="${MODE:-ionizer}"        # ionizer | indicator | btop | simple | sma
THEME="${THEME:-runic}"        # line | greek | runic
WIDTH="${WIDTH:-90}"

PY_CMD="${PY_CMD:-python3}"

usage() {
  cat <<EOF
Usage: $0 [options] [SYMBOL]

Redonkulous XMR TUI powered by crypto_monkey (Python3 engine).

Options:
  -s SOURCE     Source: coindesk | yahoo | history  (default: ${SOURCE})
  -i SECONDS    Refresh interval (default: ${INTERVAL})
  -m MODE       TUI mode:
                  ionizer   — Z-score ionizer (default)
                  indicator — analytics dashboard
                  btop      — btop-style chart
                  simple    — simple table
                  sma       — SMA watch
  -t THEME      Theme: line | greek | runic (default: ${THEME})
  -w WIDTH      Panel width (default: ${WIDTH})
  -h            Show this help

Env overrides:
  SYMBOL, SOURCE, INTERVAL, MODE, THEME, WIDTH, PY_CMD

Examples:
  # Pure chaos, default everything, XMR focus
  $0

  # 5s updates, greek theme
  INTERVAL=5 THEME=greek $0

  # Use simple mode for BTC
  $0 -m simple BTC

  # History-only (no live scraping), using cached CSV data
  SOURCE=history $0

EOF
}

while getopts ":s:i:m:t:w:h" opt; do
  case "$opt" in
    s) SOURCE="$OPTARG" ;;
    i) INTERVAL="$OPTARG" ;;
    m) MODE="$OPTARG" ;;
    t) THEME="$OPTARG" ;;
    w) WIDTH="$OPTARG" ;;
    h) usage; exit 0 ;;
    \?) echo "Unknown option: -$OPTARG" >&2; usage; exit 2 ;;
    :)  echo "Option -$OPTARG requires an argument." >&2; usage; exit 2 ;;
  esac
done
shift $((OPTIND - 1))

if [[ $# -gt 0 ]]; then
  SYMBOL="$1"
fi

# ---------- Checks ----------
if ! command -v "$PY_CMD" >/dev/null 2>&1; then
  echo "Error: python3 (or PY_CMD=$PY_CMD) not found in PATH." >&2
  exit 1
fi

# Quick check that crypto_monkey is importable
if ! "$PY_CMD" -c "import crypto_monkey" >/dev/null 2>&1; then
  echo "Error: crypto_monkey Python package/module not found." >&2
  echo "Make sure it's on PYTHONPATH or installed (e.g., pip install -e .)." >&2
  exit 1
fi

# Map MODE to crypto_monkey subcommand
case "$MODE" in
  ionizer)   SUBCMD="ionizer" ;;
  indicator) SUBCMD="indicator" ;;
  btop)      SUBCMD="tui-btop" ;;
  simple)    SUBCMD="tui-simple" ;;
  sma)       SUBCMD="sma-watch" ;;
  *)
    echo "Unknown MODE='$MODE'. Use ionizer|indicator|btop|simple|sma." >&2
    exit 2
    ;;
esac

# ---------- Terminal wizardry ----------
hide_cursor() { tput civis 2>/dev/null || true; }
show_cursor() { tput cnorm 2>/dev/null || true; }
reset_colors() { tput sgr0 2>/dev/null || printf '\033[0m'; }
clear_screen() { tput clear 2>/dev/null || printf '\033[2J\033[H'; }

cleanup() {
  reset_colors
  show_cursor
  clear_screen
}
trap cleanup EXIT INT TERM

# Let's go full extra on the intro
intro_banner() {
  clear_screen
  hide_cursor

  # Bold + bright magenta-ish
  printf '\033[1;95m'

  cat <<'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║   ᚱ  ᛖ  ᛞ  ᛟ  ᚾ  ᚲ  ᚢ  ᛚ  ᛟ  ᚢ  ᛋ    ᚷ  ᛚ  ᛁ  ᛗ  ᛗ  ᛖ  ᚱ            ║
║                                                                              ║
║          ███   XMR GODMODE ORACLE   ███                                      ║
║                                                                              ║
║  ✧ Unicode-fueled Z-score divination, powered by the crypto_monkey engine ✧  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF

  reset_colors
  sleep 1
}

status_line() {
  local now
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '\033[1;96m'  # bright cyan
  printf "Mode: %-9s  Symbol: %-6s  Source: %-9s  Theme: %-6s  Interval: %ss  Time: %s\n" \
    "$MODE" "$SYMBOL" "$SOURCE" "$THEME" "$INTERVAL" "$now"
  reset_colors
  printf '\n'
}

# ---------- Main loop ----------
intro_banner
sleep 0.8

# Hand off to Python TUI in a loop — we let Python own the TUI; shell wraps glimmer.
# We don't need to loop here, the Python app already loops by itself.
clear_screen
hide_cursor

status_line

# Color the whole session background slightly (optional, harmless if unsupported)
# Example: dim background using 256-color escape
printf '\033[48;5;235m' || true

# Exec the Python TUI; when it exits, our trap will clean up the terminal.
exec "$PY_CMD" -m crypto_monkey.cli \
  "$SUBCMD" \
  -s "$SOURCE" \
  -i "$INTERVAL" \
  -t "$THEME" \
  -w "$WIDTH" \
  "$SYMBOL"

