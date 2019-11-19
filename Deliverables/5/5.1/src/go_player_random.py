import sys, random
sys.path.append('../../3/3.1/src')
sys.path.append('../../4/4.1/src')
from constants import PASS
from point import Point
from stone import StoneEnum
from move_referee import MoveReferee
from go_player import GoPlayer

from board import Board 
from constants import BOARD_DIM
from stone import make_stone
from exceptions import CloseConnectionException

class GoPlayerRandom(GoPlayer):

    def __init__(self):
        super().__init__()
        self.move_ref = MoveReferee()

    def choose_move(self, boards):
        empty_spaces = list(boards[0].get_points(None))
        random.shuffle(empty_spaces)
        for x, y in empty_spaces:
            if self.move_ref.valid_move(self.stone_type, Point(x,y), boards, boards[0]):
                return Point(x, y)
        return PASS

class GoPlayerCrazy(GoPlayerRandom):

    def __init__(self):
        super().__init__()
        self.move_ref = MoveReferee()
        self.randomness = 0.5
    
    def register(self, name = "no name"):
        self._throw_exception()
        return super().register(name)

    def receive_stone(self, stone_type):
        self._throw_exception()
        return super().receive_stone(stone_type)

    def choose_move(self, boards):
        ret = self._return_invalid()
        if ret != None:
            return ret
        self._throw_exception()
        if random.random() < self.randomness:
            return self.choose_illegal_move(boards)
        return super().choose_move(boards)

    def choose_illegal_move(self, boards):
        filled_spaces = list(boards[0].get_points(StoneEnum.BLACK))
        filled_spaces += list(boards[0].get_points(StoneEnum.WHITE))
        if len(filled_spaces) != 0:
            x, y = filled_spaces[random.randint(0, len(filled_spaces)-1)]
            return Point(x, y)
        return Point(-1, -1)

    def _throw_exception(self):
        if random.random() < self.randomness/10:
            raise CloseConnectionException("Randomly close the connection!")

    def _return_invalid(self):
        invalid_things = [3, "14", "elevator", 12.2, [3,2,1]]
        random.shuffle(invalid_things)
        if random.random() < self.randomness/3:
            return invalid_things[0]