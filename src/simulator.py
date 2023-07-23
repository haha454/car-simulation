import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable

from src.car import Car


@dataclass(frozen=True)
class Simulator:
    _right: int
    _top: int
    _help_text_handler: Callable[[str], None] = lambda *args, **kwargs: None

    def simulate(self, cars: list[Car]) -> list[tuple[Car, str]]:
        """
        Simulates cars movement.
        :return: A list of car with their respective collided cars, if any.
        """
        self._detect_collision(cars)
        while any(filter(Car.can_move, cars)):
            for car in filter(Car.can_move, cars):
                self._simulate_step(car)

            self._detect_collision(cars)

        return self._get_simulation_result(cars)

    @classmethod
    def _detect_collision(cls, cars: list[Car]):
        cars_per_coordinate = cls._aggregate_cars_by_coordinate(cars)

        for car in itertools.chain(*(cars for cars in cars_per_coordinate.values() if len(cars) > 1)):
            car.collided = True

    def _simulate_step(self, car: Car) -> None:
        assert car.can_move()
        car.execute_command()
        car.x = min(car.x, self._right - 1)
        car.x = max(car.x, 0)
        car.y = min(car.y, self._top - 1)
        car.y = max(car.y, 0)

    def _get_simulation_result(self, cars: list[Car]) -> list[tuple[Car, str]]:
        result = []
        for car_group in self._aggregate_cars_by_coordinate(cars).values():
            if len(car_group) == 1:
                car = car_group[0]
                assert not car.collided
                result.append((car, ''))
            else:
                assert all(car.collided for car in car_group)
                for idx, car in enumerate(car_group):
                    result.append((car, self._get_collided_car_names_from_group(car_group, idx)))

        return result

    @classmethod
    def _get_collided_car_names_from_group(cls, car_group: list[Car], idx: int) -> str:
        return ",".join(car.name for car in
                        itertools.chain(itertools.islice(car_group, idx), itertools.islice(car_group, idx + 1, None)))

    @classmethod
    def _aggregate_cars_by_coordinate(cls, cars: list[Car]) -> dict[tuple[int, int], list[Car]]:
        cars_per_coordinate: dict[tuple[int, int], list[Car]] = defaultdict(list)
        for car in cars:
            cars_per_coordinate[(car.x, car.y)].append(car)
        return cars_per_coordinate
