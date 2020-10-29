from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple
from actions import Action, EscapeAction, EnterRemoteNumber, ClearRemote, ActivateRemote,DeleteRemoteNumber
from enum import auto, Enum
from highlight import Highlight

import tcod.event

if TYPE_CHECKING:
    from engine import Engine

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.get():
            context.convert_event(event)
            self.dispatch(event)
            pass

    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    def on_render(self, root_console: tcod.Console) -> None:
        self.engine.render(root_console)

class MainGameEventHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        self.current_context = context
        for event in tcod.event.get():
            context.convert_event(event)
            actions = self.dispatch(event)

            if actions is None:
                continue

            for action in actions:
                action.perform()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[list(Action)]:
        actions = []

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            actions.append(EscapeAction(self.engine))
        elif key == tcod.event.K_0:
            actions.append(EnterRemoteNumber(self.engine, 0))
        elif key == tcod.event.K_1:
            actions.append(EnterRemoteNumber(self.engine, 1))
        elif key == tcod.event.K_2:
            actions.append(EnterRemoteNumber(self.engine, 2))
        elif key == tcod.event.K_3:
            actions.append(EnterRemoteNumber(self.engine, 3))
        elif key == tcod.event.K_4:
            actions.append(EnterRemoteNumber(self.engine, 4))
        elif key == tcod.event.K_5:
            actions.append(EnterRemoteNumber(self.engine, 5))
        elif key == tcod.event.K_6:
            actions.append(EnterRemoteNumber(self.engine, 6))
        elif key == tcod.event.K_7:
            actions.append(EnterRemoteNumber(self.engine, 7))
        elif key == tcod.event.K_8:
            actions.append(EnterRemoteNumber(self.engine, 8))
        elif key == tcod.event.K_9:
            actions.append(EnterRemoteNumber(self.engine, 9))
        elif key == tcod.event.K_BACKSPACE:
            actions.append(DeleteRemoteNumber(self.engine))
        elif key == tcod.event.K_RETURN or key == tcod.event.K_RETURN2:
            actions.append(ActivateRemote(self.engine))
        
        for section in self.engine.sections:
            if section.ui is not None:
                section.ui.keydown(event)

        # No valid key was pressed
        return actions

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        self.engine.mouse_location = self.current_context.pixel_to_tile(event.pixel.x, event.pixel.y)

        for section in self.engine.sections:
            if section.ui is not None:
                section.ui.mousemove(self.engine.mouse_location[0], self.engine.mouse_location[1])

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[list(Action)]:
        actions = []

        self.is_mouse_down = True
        self.mouse_down_location = self.engine.mouse_location

        for section in self.engine.sections:
            if section.ui is not None:
                section.ui.mousedown(self.engine.mouse_location[0], self.engine.mouse_location[1])

        return actions

