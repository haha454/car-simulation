from dataclasses import dataclass
from typing import Callable

from src.const import DIRECTION_STR_TO_INT


@dataclass
class Parser:
    _error_handler: Callable[[str], None] = lambda *args, **kwargs: None

    def parse_str_to_int(self, st: str) -> tuple[int, bool]:
        if st.isdigit():
            return int(st), True

        self._error_handler(f'{st} is not a valid number')
        return 0, False

    def parse_str_to_direction(self, st: str) -> tuple[int, bool]:
        """
        Converts a string to its direction representation, indicated by const.DIRECTION_STR_TO_INT.
        """
        if st in DIRECTION_STR_TO_INT:
            return DIRECTION_STR_TO_INT[st], True

        self._error_handler(f'{st} is not a valid direction')
        return 0, False
