import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from copy import deepcopy
from stone import StoneEnum
from constants import PASS
from move_referee import MoveReferee
from score_referee import ScoreReferee

class GoReferee:

   ## Class Variables
   move_ref = MoveReferee()
   score_ref = ScoreReferee()

   ## Constructors
   def __init__(self, history, players):
      self.history = history
      self.players = players

   ## Public Methods
   def play_game(self):
      output, invalid_mover = [StoneEnum.BLACK, StoneEnum.WHITE], None
      pass_count, turn = 0, 0
      while pass_count < 2:
         output.append(deepcopy(self.history))
         curr = self.players[turn]
         move = curr.choose_move(self.history)
         if not move:
            return output[0:-1]
         elif move == PASS:
            pass_count += 1
         else:
            pass_count = 0
            move_valid = self.move_ref.valid_move(curr.stone_type, move, self.history, self.history[0])
            if not move_valid:
               invalid_mover = turn
               break
         self.play_move(move, turn)
         turn = self.next_turn(turn)
      output.append(sorted(self.determine_winner(invalid_mover)))
      return output

   def play_move(self, move, turn):
      new_board = deepcopy(self.history[0])
      if move != PASS:
         new_board.place_and_update(self.players[turn].stone_type, move)
      self.history.insert(0, new_board)
      if len(self.history) == 4:
         self.history.pop()

   def determine_winner(self, invalid_mover):
      if invalid_mover is not None:
         winner = self.next_turn(invalid_mover)
         return [self.players[winner].name]
      score_dict = self.score_ref.get_score(self.history[0])
      player1_score = score_dict[self.players[0].stone_type]
      player2_score = score_dict[self.players[1].stone_type]
      if player1_score == player2_score:
         return [self.players[0].name, self.players[1].name]
      elif player1_score > player2_score:
         return [self.players[0].name]
      else:
         return [self.players[1].name]
      
   def next_turn(self, turn):
      return (turn + 1) % 2