import sys
from typing import Iterator

from src.car import Car
from src.car_creator import CarCreator
from src.parser import Parser
from src.simulator import Simulator


def main():
    parser = Parser(_handle_error)
    input_source = iter(sys.stdin)

    while True:
        right, top = _build_field(parser, input_source)

        _create_cars_and_simulate(right, top, parser, input_source)

        if not _should_start_over(parser, input_source):
            break


def _should_start_over(parser: Parser, input_source: Iterator[str]) -> bool:
    while True:
        _handle_help_text('Please choose from the following options:\n'
                          '[1] Start over\n'
                          '[2] Exit')

        option, success = parser.parse_str_to_int(next(input_source).rstrip())
        if not success:
            continue

        if option == 1:
            return True
        elif option == 2:
            return False
        else:
            _handle_error(f'invalid option: {option}')


def _create_cars_and_simulate(right: int, top: int, parser: Parser, input_source: Iterator[str]) -> None:
    """
    Create cars on the field and execute simulator.
    """

    simulator = Simulator(right, top)
    car_creator = CarCreator(_right=right, _top=top, _input_source=input_source, _parser=parser,
                             _error_handler=_handle_error, _help_text_handler=_handle_help_text)
    cars: list[Car] = []
    while True:
        _handle_help_text('Please choose from the following options:\n'
                          '[1] Add a car to field\n'
                          '[2] Run simulation')
        option, success = parser.parse_str_to_int(next(input_source).rstrip())
        if not success:
            continue

        if option == 1:
            cars.append(car_creator.create())
            _output_list_of_cars(cars)
        elif option == 2:
            _output_list_of_cars(cars)
            _output_simulation_result(simulator.simulate(cars))
            break
        else:
            _handle_error(f'invalid option: {option}')


def _output_list_of_cars(cars) -> None:
    _handle_help_text('Your current list of cars are:')
    for car in cars:
        _handle_help_text(car.initial_state_str())
    _handle_help_text('')


def _output_simulation_result(simulation_result: list[tuple[Car, str]]) -> None:
    _handle_help_text('After simulation, the result is:')
    for car, collided_car_names in simulation_result:
        if not car.collided:
            assert not collided_car_names
            _handle_help_text(f'- {car.name}, ({car.x},{car.y}) {car.get_direction_str()}')
        else:
            assert collided_car_names
            _handle_help_text(
                f'- {car.name}, collides with {collided_car_names} at ({car.x},{car.y}) at step {car.finished_commands}')
    _handle_help_text('')


def _build_field(parser: Parser, input_source: Iterator[str]) -> tuple[int, int]:
    while True:
        _handle_help_text(
            'Welcome to Auto Driving Car Simulator!\n\n'
            'Please enter the width and height of the simulation field in x y format:')

        fields = next(input_source).split()
        if len(fields) != 2:
            _handle_error('the input should have two fields.')
            continue

        right, success = parser.parse_str_to_int(fields[0])
        if not success:
            continue
        if right <= 0:
            _handle_error('x must be a positive integer')
            continue

        top, success = parser.parse_str_to_int(fields[1])
        if not success:
            continue
        if top <= 0:
            _handle_error('top must be a positive integer')
            continue

        _handle_help_text(
            f'You have created a field of {right} x {top}.\n')

        return right, top


def _handle_help_text(help_text: str) -> None:
    print(help_text)


def _handle_error(err: str) -> None:
    print(err, file=sys.stderr)


if __name__ == '__main__':
    main()
