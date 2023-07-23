from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Callable

from src.car import Car
from src.parser import Parser


@dataclass
class CarCreator:
    _right: int
    _top: int
    _input_source: Iterator[str]
    _parser: Parser
    _error_handler: Callable[[str], None] = lambda *args, **kwargs: None
    _help_text_handler: Callable[[str], None] = lambda *args, **kwargs: None

    def create(self) -> Car:
        name = self._create_name()
        x, y, direction = self._create_x_y_direction(name)
        commands = self._create_commands(name)
        return Car(name=name, x=x, y=y, direction=direction, commands=commands)

    def _create_name(self) -> str:
        self._help_text_handler('Please enter the name of the car:')
        return next(self._input_source).rstrip()

    def _create_x_y_direction(self, name: str) -> tuple[int, int, int]:
        while True:
            self._help_text_handler(f'Please enter initial position of car {name} in x y Direction format:')
            fields: list[str] = next(self._input_source).split()
            if len(fields) != 3:
                self._error_handler('the input should have three fields.')
                continue
            x, success = self._parser.parse_str_to_int(fields[0])
            if not success:
                continue
            if x >= self._right:
                self._error_handler(f'x should be smaller than {self._right}')
                continue

            y, success = self._parser.parse_str_to_int(fields[1])
            if not success:
                continue
            if y >= self._top:
                self._error_handler(f'y should be smaller than {self._top}')
                continue

            direction, success = self._parser.parse_str_to_direction(fields[2])
            if not success:
                continue

            return x, y, direction

    def _create_commands(self, name: str) -> str:
        while True:
            self._help_text_handler(f'Please enter the commands for car {name}:')
            commands = next(self._input_source).rstrip()
            if any(command not in {'L', 'R', 'F'} for command in commands):
                self._error_handler(f'{commands} contains characters other than \"L\", \"R\" and \"F\"')
                continue

            return commands
