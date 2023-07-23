from src.car import Car
from src.car_creator import CarCreator
from src.parser import Parser


class TestCarCreator:
    def test_create(self):
        car_creator = CarCreator(_right=100, _top=100, _input_source=iter([
            'ex car\n',
            'invalid_x invalid_y  N',
            '100 100 N',
            '5 5 S',
            'LRXY',
            'LLRFF',
        ]), _parser=Parser())

        assert car_creator.create() == Car(name='ex car', x=5, y=5, direction=2, commands='LLRFF')
