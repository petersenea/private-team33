import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from copy import deepcopy
from stone import StoneEnum
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
      output = ["B", "W"]
      pass_count = 0
      turn = 0
      while pass_count < 2:
         output.append(deepcopy(self.history))
         move = self.players[turn].choose_move(self.history)
         if move == "pass":
            pass_count += 1
         else:
            pass_count = 0
            move_valid = self.move_ref.valid_move(self.players[turn].stone_type, move, self.history, self.history[0])
            if not move_valid:
               break
            self.play_move(move, turn)
         turn = (turn + 1) % 2
      output += sorted(self.determine_winner())
      return output

   def play_move(self, point, turn):
      new_board = deepcopy(self.history[0])
      new_board.place_and_update(self.players[turn].stone_type, point)
      self.history.insert(0, new_board)
      if len(self.history) == 4:
         self.history.pop()

   def determine_winner(self):
      score_dict = self.score_ref.get_score(self.history[0])
      player1_score = score_dict[self.players[0].stone_type]
      player2_score = score_dict[self.players[1].stone_type]
      if player1_score == player2_score:
         return [self.players[0].name, self.players[1].name]
      elif player1_score > player2_score:
         return [self.players[0].name]
      else:
         return [self.players[1].name]