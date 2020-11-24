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
        self.engine.remote.add_number(self.number)

class ClearRemote(Action):
    def perform(self) -> None:
        self.engine.remote.clear()

class ActivateRemote(Action):
    def perform(self) -> None:
        self.engine.remote.activate()

class DeleteRemoteNumber(Action):
    def perform(self) -> None:
        self.engine.remote.delete_number()

class CloseMenu(Action):
    def perform(self) -> None:
        self.engine.close_menu()

class OpenMenu(Action):
    def perform(self) -> None:
        self.engine.open_menu()