from __future__ import annotations

from dataclasses import dataclass

from src.const import STEPS, DIRECTION_INT_TO_STR


@dataclass
class Car:
    name: str
    x: int
    y: int
    direction: int
    commands: str = ''
    collided: bool = False
    finished_commands: int = 0

    def can_move(self):
        return not self.collided and self.finished_commands < len(self.commands)

    def execute_command(self):
        assert self.can_move()
        if self.commands[self.finished_commands] == 'L':
            self._turn_left()
        elif self.commands[self.finished_commands] == 'R':
            self._turn_right()
        elif self.commands[self.finished_commands] == 'F':
            self._forward()
        else:
            raise ValueError(f'unknown command {self.commands[self.finished_commands]}')
        self.finished_commands += 1

    def initial_state_str(self):
        return f'- {self.name}, ({self.x},{self.y}) {self.get_direction_str()}, {self.commands}'

    def get_direction_str(self) -> str:
        return DIRECTION_INT_TO_STR[self.direction]

    def _turn_left(self):
        self.direction = (self.direction + 3) % 4

    def _turn_right(self):
        self.direction = (self.direction + 1) % 4

    def _forward(self):
        self.x, self.y = self.x + STEPS[self.direction][0], self.y + STEPS[self.direction][1]
