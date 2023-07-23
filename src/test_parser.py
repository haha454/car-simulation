import pytest

from src.parser import Parser


class TestParser:
    @pytest.mark.parametrize('st,expected_int,expected_success', [('5', 5, True), ('a', 0, False)])
    def test_parse_str_to_int(self, st: str, expected_int: int, expected_success: bool):
        parser = Parser()

        parsed_int, success = parser.parse_str_to_int(st)

        assert expected_success == success
        if success:
            assert expected_int == parsed_int

    @pytest.mark.parametrize('st,expected_direction,expected_success', [
        ('N', 0, True),
        ('E', 1, True),
        ('S', 2, True),
        ('W', 3, True),
        ('X', 0, False)])
    def test_parse_str_to_direction(self, st: str, expected_direction: int, expected_success: bool):
        parser = Parser()

        parsed_direction, success = parser.parse_str_to_direction(st)

        assert expected_success == success
        if success:
            assert expected_direction == parsed_direction
