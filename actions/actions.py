from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine


class Action:
    def __init__(self, engine) -> None:
        super().__init__()
        self.engine = engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class EnterRemoteNumber(Action):
    def __init__(self, engine, number: int) -> None:
        super().__init__(engine)
        self.number = number

    def perform(self) -> None:
        self.engine.page_manager.add_number(self.number)

class ClearRemote(Action):
    def perform(self) -> None:
        self.engine.page_manager.clear()

class ActivateRemote(Action):
    def perform(self) -> None:
        self.engine.page_manager.activate()

class DeleteRemoteNumber(Action):
    def perform(self) -> None:
        self.engine.page_manager.delete_number()

class CloseMenu(Action):
    def perform(self) -> None:
        self.engine.close_menu()

class OpenMenu(Action):
    def perform(self) -> None:
        self.engine.open_menu()

class AnswerCorrect(Action):
    def __init__(self, engine, question: str) -> None:
        super().__init__(engine)
        self.question = question

    def perform(self):
        self.engine.correct_answer_given(self.question)

class ShowTooltip(Action):
    def __init__(self, engine, tooltip_key: str) -> None:
        super().__init__(engine)
        self.tooltip_key = tooltip_key

    def perform(self):
        self.engine.show_tooltip(self.tooltip_key)

class HideTooltip(Action):
    def __init__(self, engine, tooltip_key: str) -> None:
        super().__init__(engine)
        self.tooltip_key = tooltip_key

    def perform(self):
        self.engine.hide_tooltip(self.tooltip_key)