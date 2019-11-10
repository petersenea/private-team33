import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from stone import StoneEnum
from move_referee import MoveReferee
from point import Point
from go_player import GoPlayer

class GoPlayerBasic(GoPlayer):

   def choose_move(self, boards):
      if not self.move_referee.valid_history(self.stone_type, boards):
         return "This history makes no sense!"
      for x, y in sorted(list(boards[0].get_points(None))):
         if self.move_referee.valid_move(self.stone_type, Point(x, y), boards, boards[0]):
            return (x, y)
      return "pass"