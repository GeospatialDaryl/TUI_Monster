"""Task tracker example combining navigation and state changes."""

import curses
from dataclasses import dataclass
from typing import List

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from simple_tui import SimpleTUI


@dataclass
class Task:
    title: str
    done: bool = False


class TaskTrackerTUI(SimpleTUI):
    """Manage a small checklist using keyboard navigation."""

    def __init__(self) -> None:
        super().__init__(refresh_rate=0.1)
        self.tasks: List[Task] = [
            Task("Read project brief"),
            Task("Sketch interface ideas"),
            Task("Build prototype"),
        ]
        self.selected = 0
        self.next_task_id = 4

    def on_start(self) -> None:
        self.register_handlers(
            {
                curses.KEY_UP: self.move_up,
                curses.KEY_DOWN: self.move_down,
                ord("k"): self.move_up,
                ord("j"): self.move_down,
                ord(" "): self.toggle_task,
                ord("t"): self.add_task,
                ord("x"): self.remove_task,
            }
        )

    def move_up(self, _: int) -> None:
        if self.tasks:
            self.selected = (self.selected - 1) % len(self.tasks)

    def move_down(self, _: int) -> None:
        if self.tasks:
            self.selected = (self.selected + 1) % len(self.tasks)

    def toggle_task(self, _: int) -> None:
        if self.tasks:
            task = self.tasks[self.selected]
            task.done = not task.done

    def add_task(self, _: int) -> None:
        title = f"New Task {self.next_task_id}"
        self.tasks.append(Task(title))
        self.selected = len(self.tasks) - 1
        self.next_task_id += 1

    def remove_task(self, _: int) -> None:
        if not self.tasks:
            return
        self.tasks.pop(self.selected)
        if self.tasks:
            self.selected %= len(self.tasks)
        else:
            self.selected = 0

    def draw(self) -> None:
        self.clear()
        self.addstr(0, 0, "Task Tracker")
        self.addstr(1, 0, "Use arrows or j/k to navigate. Space toggles a task.")
        self.addstr(2, 0, "Press 't' to add a task, 'x' to remove, 'q' to quit.")

        for idx, task in enumerate(self.tasks):
            prefix = "[x]" if task.done else "[ ]"
            marker = "->" if idx == self.selected else "  "
            line = f"{marker} {prefix} {task.title}"
            attr = curses.A_REVERSE if idx == self.selected else None
            self.addstr(4 + idx, 0, line, attr)

        if not self.tasks:
            self.addstr(4, 0, "No tasks yet. Press 't' to add one.")

        self.refresh()


if __name__ == "__main__":
    TaskTrackerTUI().run()
