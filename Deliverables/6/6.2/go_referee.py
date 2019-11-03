import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from stone import StoneEnum
from move_referee import MoveReferee
from score_referee import ScoreReferee

class GoReferee:

   ## Class Variables
   move_ref = MoveReferee()
   score_ref = ScoreReferee()

   ## Constructors
   def __init__(self, board, players):
      self.board = board
      self.players = players

   ## Public Methods
   def play_game():
      pass