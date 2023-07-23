import pytest

from src.car import Car


class TestCar:
    @pytest.mark.parametrize('car,expected_can_move', [
        (Car('car with empty commands', 0, 0, 0), False),
        (Car('collided car', 0, 0, 0, commands='LLL', collided=True, finished_commands=3), False),
        (Car('normal car', 0, 0, 0, commands='LLL'), True),
    ])
    def test_can_move(self, car: Car, expected_can_move: bool):
        assert expected_can_move == car.can_move()

    @pytest.mark.parametrize('car,expected_resulted_car', [
        (Car('car to turn left', x=5, y=5, direction=0, commands='L'),
         Car('car to turn left', x=5, y=5, direction=3, commands='L', finished_commands=1)),
        (Car('car to turn right', x=5, y=5, direction=0, commands='LR', finished_commands=1),
         Car('car to turn right', x=5, y=5, direction=1, commands='LR', finished_commands=2)),
        (Car('car to forward', x=5, y=5, direction=0, commands='LRF', finished_commands=2),
         Car('car to forward', x=5, y=6, direction=0, commands='LRF', finished_commands=3)),
    ])
    def test_execute_command(self, car: Car, expected_resulted_car: Car):
        car.execute_command()

        assert expected_resulted_car == car
