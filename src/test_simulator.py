import itertools

from src.car import Car
from src.simulator import Simulator


class TestSimulator:
    def test_simulate_no_collision(self):
        simulation_result = Simulator(5, 5).simulate([
            Car('A', 0, 0, 0, 'F'),
            Car('B', 1, 1, 2, 'F'),
        ])
        assert [
                   (Car('A', 0, 1, 0, 'F', collided=False, finished_commands=1), ''),
                   (Car('B', 1, 0, 2, 'F', collided=False, finished_commands=1), ''),
               ] == simulation_result

    def test_simulate_no_collision_cross_boundary(self):
        simulation_result = Simulator(2, 2).simulate([
            Car('A', 0, 0, 2, 'F'),
            Car('B', 1, 1, 0, 'F'),
        ])

        assert [
                   (Car('A', 0, 0, 2, 'F', collided=False, finished_commands=1), ''),
                   (Car('B', 1, 1, 0, 'F', collided=False, finished_commands=1), ''),
               ] == simulation_result

    def test_simulate_collide_at_beginning(self):
        simulation_result = Simulator(2, 2).simulate([
            Car('A', 0, 0, 2, 'F'),
            Car('B', 0, 0, 0, 'F'),
        ])

        assert [
                   (Car('A', 0, 0, 2, 'F', collided=True, finished_commands=0), 'B'),
                   (Car('B', 0, 0, 0, 'F', collided=True, finished_commands=0), 'A'),
               ] == simulation_result

    def test_simulate_collide_at_the_same_time(self):
        simulation_result = Simulator(2, 2).simulate([
            Car('A', 0, 0, 0, 'F'),
            Car('B', 1, 1, 3, 'F'),
        ])

        assert [
                   (Car('A', 0, 1, 0, 'F', collided=True, finished_commands=1), 'B'),
                   (Car('B', 0, 1, 3, 'F', collided=True, finished_commands=1), 'A'),
               ] == simulation_result

    def test_simulate_collide_at_the_different_times(self):
        simulation_result = Simulator(5, 5).simulate([
            Car('A', 0, 0, 0, 'F'),
            Car('B', 1, 1, 3, 'F'),
            Car('C', 5, 1, 3, 'FFFFF'),
        ])
        assert [
                   (Car('A', 0, 1, 0, 'F', collided=True, finished_commands=1), 'B,C'),
                   (Car('B', 0, 1, 3, 'F', collided=True, finished_commands=1), 'A,C'),
                   (Car('C', 0, 1, 3, 'FFFFF', collided=True, finished_commands=5), 'A,B'),
               ] == simulation_result
