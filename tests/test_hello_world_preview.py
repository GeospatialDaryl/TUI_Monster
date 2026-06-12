from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

EXAMPLE_PATH = (
    Path(__file__).resolve().parents[1] / "examples" / "01_hello_world" / "main.py"
)


def load_hello_world_module():
    spec = importlib.util.spec_from_file_location("hello_world_preview", EXAMPLE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_preview_modes_cover_the_full_tutorial_sequence() -> None:
    module = load_hello_world_module()

    titles = [mode.title for mode in module.PREVIEW_MODES]

    assert titles == [
        "01 · Hello World",
        "02 · Live Clock",
        "03 · Counter",
        "04 · Task Tracker",
        "05 · GodMode Clock",
    ]


def test_preview_app_can_navigate_and_render_samples() -> None:
    module = load_hello_world_module()
    app = module.HelloWorldTUI()

    assert app.active_mode.title == "01 · Hello World"
    assert "[01]" in app.mode_tabs()

    app.next_mode(ord("n"))
    assert app.active_mode.title == "02 · Live Clock"

    app.current_time = "2026-06-12 12:34:56"
    assert "Current time: 2026-06-12 12:34:56" in app.rendered_sample_lines()

    app.jump_to_mode(ord("5"))
    assert app.active_mode.title == "05 · GodMode Clock"

    app.previous_mode(ord("p"))
    assert app.active_mode.title == "04 · Task Tracker"


def test_preview_app_requires_at_least_one_mode() -> None:
    module = load_hello_world_module()

    with pytest.raises(ValueError, match="at least one preview mode"):
        module.HelloWorldTUI(())
