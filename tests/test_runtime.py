from __future__ import annotations

import curses

import pytest

from pyTuiMonster import TuiConfig, TuiMonsterApp, key_binding, lifecycle_hook


class FakeScreen:
    def __init__(self, keys: list[int] | None = None, height: int = 24, width: int = 80) -> None:
        self.keys = list(keys or [])
        self.height = height
        self.width = width
        self.writes: list[tuple[int, int, str, int | None]] = []
        self.erased = False
        self.noutrefreshed = False
        self.nodelay_value: bool | None = None
        self.keypad_value: bool | None = None
        self.timeout_value: int | None = None

    def getch(self) -> int:
        if self.keys:
            return self.keys.pop(0)
        return -1

    def getmaxyx(self) -> tuple[int, int]:
        return self.height, self.width

    def addnstr(self, y: int, x: int, text: str, length: int, attr: int | None = None) -> None:
        self.writes.append((y, x, text[:length], attr))

    def erase(self) -> None:
        self.erased = True

    def noutrefresh(self) -> None:
        self.noutrefreshed = True

    def nodelay(self, value: bool) -> None:
        self.nodelay_value = value

    def keypad(self, value: bool) -> None:
        self.keypad_value = value

    def timeout(self, value: int) -> None:
        self.timeout_value = value


class MinimalApp(TuiMonsterApp):
    def draw(self) -> None:
        pass


def test_config_rejects_invalid_values() -> None:
    with pytest.raises(ValueError, match="refresh_rate"):
        TuiConfig(refresh_rate=-0.1)
    with pytest.raises(ValueError, match="stop_keys"):
        TuiConfig(stop_keys=())


def test_key_binding_rejects_empty_or_non_integer_keys() -> None:
    with pytest.raises(ValueError, match="at least one"):
        key_binding()
    with pytest.raises(TypeError, match="integers"):
        key_binding("x")  # type: ignore[arg-type]


def test_lifecycle_hook_rejects_unknown_stage() -> None:
    with pytest.raises(ValueError, match="Unsupported lifecycle stage"):
        lifecycle_hook("during_launch")  # type: ignore[arg-type]


def test_decorated_key_bindings_and_hooks_are_inherited() -> None:
    class BaseApp(TuiMonsterApp):
        def __init__(self) -> None:
            super().__init__(TuiConfig(refresh_rate=0, stop_keys=(ord("q"),)))
            self.events: list[str] = []

        @key_binding(ord("a"))
        def base_key(self, _: int) -> None:
            self.events.append("base_key")

        @lifecycle_hook("before_update")
        def base_hook(self) -> None:
            self.events.append("base_hook")

        def draw(self) -> None:
            pass

    class ChildApp(BaseApp):
        @key_binding(ord("b"))
        def child_key(self, _: int) -> None:
            self.events.append("child_key")

        @lifecycle_hook("before_update")
        def child_hook(self) -> None:
            self.events.append("child_hook")

    app = ChildApp()

    assert sorted(app.keymap) == [ord("a"), ord("b")]
    app._run_stage("before_update")
    assert app.events == ["base_hook", "child_hook"]


def test_duplicate_local_key_bindings_raise_error() -> None:
    with pytest.raises(ValueError, match="Duplicate key binding"):

        class DuplicateApp(TuiMonsterApp):
            @key_binding(ord("x"))
            def first(self, _: int) -> None:
                pass

            @key_binding(ord("x"))
            def second(self, _: int) -> None:
                pass

            def draw(self) -> None:
                pass


def test_process_input_drains_available_keys_and_stops() -> None:
    class InputApp(TuiMonsterApp):
        def __init__(self) -> None:
            super().__init__(TuiConfig(refresh_rate=0, stop_keys=(ord("q"),)))
            self.keys: list[int] = []

        @key_binding(ord("a"), ord("b"))
        def collect(self, key: int) -> None:
            self.keys.append(key)

        def draw(self) -> None:
            pass

    app = InputApp()
    app._stdscr = FakeScreen([ord("a"), ord("b"), ord("q")])  # type: ignore[assignment]
    app._running = True

    app._process_input()

    assert app.keys == [ord("a"), ord("b")]
    assert app.running is False


def test_addstr_bounds_and_truncation() -> None:
    app = MinimalApp()
    screen = FakeScreen(height=3, width=5)
    app._stdscr = screen  # type: ignore[assignment]

    assert app.addstr(0, 0, "abcdef") is True
    assert screen.writes == [(0, 0, "abcde", None)]
    assert app.addstr(5, 0, "outside") is False
    assert app.addstr(0, 7, "outside") is False


def test_center_text_uses_screen_width() -> None:
    app = MinimalApp()
    screen = FakeScreen(height=3, width=10)
    app._stdscr = screen  # type: ignore[assignment]

    assert app.center_text(1, "abcd") is True
    assert screen.writes[-1] == (1, 3, "abcd", None)


def test_refresh_calls_curses_doupdate(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def fake_doupdate() -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(curses, "doupdate", fake_doupdate)
    app = MinimalApp()
    screen = FakeScreen()
    app._stdscr = screen  # type: ignore[assignment]

    app.refresh()

    assert screen.noutrefreshed is True
    assert called is True
