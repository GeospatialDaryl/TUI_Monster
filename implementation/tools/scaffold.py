"""Scaffold new TUI Monster projects from built-in templates."""

from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

_TEMPLATES_DIR = Path(__file__).parent / "templates"
_TEMPLATE_TYPES = ("basic", "menu", "wrapper")


class Scaffolder:
    """Generate TUI project skeletons from templates."""

    def __init__(
        self,
        output_dir: Optional[str] = None,
        template_dir: Optional[str] = None,
    ) -> None:
        self._output_dir = Path(output_dir) if output_dir else Path.cwd()
        self._template_dir = Path(template_dir) if template_dir else _TEMPLATES_DIR

    def create(
        self,
        name: str,
        template_type: str,
        extra_vars: Optional[Dict[str, str]] = None,
    ) -> Path:
        """Render *template_type* templates into *output_dir/name*."""
        if template_type not in _TEMPLATE_TYPES:
            raise ValueError(
                f"Unknown template type '{template_type}'. "
                f"Available: {', '.join(_TEMPLATE_TYPES)}"
            )

        dest = self._output_dir / name
        if dest.exists():
            raise FileExistsError(f"Output directory already exists: {dest}")

        vars_ = self._build_vars(name, extra_vars)
        tmpl_dir = self._template_dir / template_type

        if not tmpl_dir.is_dir():
            raise FileNotFoundError(f"Template directory not found: {tmpl_dir}")

        dest.mkdir(parents=True)

        for tmpl_file in sorted(tmpl_dir.glob("*.tmpl")):
            output_name = tmpl_file.stem   # strip .tmpl
            content = tmpl_file.read_text()
            rendered = self._render(content, vars_)
            (dest / output_name).write_text(rendered)
            print(f"  created  {dest / output_name}")

        print(f"\nScaffolded '{name}' ({template_type}) → {dest}")
        return dest

    # ------------------------------------------------------------------

    def _build_vars(self, name: str, extra: Optional[Dict[str, str]]) -> Dict[str, str]:
        author = self._git_user() or os.environ.get("USER", "unknown")
        vars_: Dict[str, str] = {
            "APP_NAME": name,
            "CLASS_NAME": self._to_class_name(name),
            "DATE": datetime.date.today().isoformat(),
            "AUTHOR": author,
            "PYTHON": sys.executable,
        }
        if extra:
            vars_.update(extra)
        return vars_

    @staticmethod
    def _render(content: str, vars_: Dict[str, str]) -> str:
        for key, value in vars_.items():
            content = content.replace(f"{{{{{key}}}}}", value)
        return content

    @staticmethod
    def _to_class_name(name: str) -> str:
        parts = re.split(r"[_\-\s]+", name)
        return "".join(p.capitalize() for p in parts if p)

    @staticmethod
    def _git_user() -> str:
        try:
            result = subprocess.run(
                ["git", "config", "user.name"],
                capture_output=True, text=True, timeout=3,
            )
            return result.stdout.strip()
        except Exception:
            return ""


# ---------------------------------------------------------------------------
# CLI

def _list_templates() -> None:
    descriptions = {
        "basic": "Single-screen TUI with update loop and key bindings",
        "menu": "Armbian-style hierarchical menu pre-wired with MonsterMenuApp",
        "wrapper": "ScriptWrapperApp subclass ready to wrap a shell command",
    }
    print("Available templates:")
    for t, desc in descriptions.items():
        print(f"  {t:<12}  {desc}")


def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="scaffold",
        description="Generate TUI Monster project skeletons.",
    )
    sub = parser.add_subparsers(dest="cmd")

    new_p = sub.add_parser("new", help="Create a new project")
    new_p.add_argument("name", help="Project directory name")
    new_p.add_argument(
        "--type", dest="template_type", default="basic",
        choices=_TEMPLATE_TYPES,
        help="Template to use (default: basic)",
    )
    new_p.add_argument("--output-dir", default=None, help="Parent directory")
    new_p.add_argument("--template-dir", default=None, help="Custom template directory")

    sub.add_parser("list", help="List available templates")

    args = parser.parse_args()

    if args.cmd == "list" or args.cmd is None:
        _list_templates()
        return

    if args.cmd == "new":
        s = Scaffolder(output_dir=args.output_dir, template_dir=args.template_dir)
        try:
            s.create(name=args.name, template_type=args.template_type)
        except (FileExistsError, ValueError, FileNotFoundError) as exc:
            sys.exit(f"Error: {exc}")


if __name__ == "__main__":
    _cli()
