import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from board import empty_board
from copy import deepcopy
from stone import StoneEnum
from constants import PASS
from point import Point
from move_referee import MoveReferee
from score_referee import ScoreReferee
from exceptions import *

class GoReferee:

    ## Class Variables
    move_ref = MoveReferee()
    score_ref = ScoreReferee()

    ## Constructors
    def __init__(self, players):
        self.history = [empty_board()]
        self.players = players
        self.invalid_mover = None

    ## Public Methods
    def play_game(self):
        pass_count, turn = 0, 0
        while pass_count < 2:
            curr = self.players[turn]
            try:
                move = curr.choose_move(self.history)
            except CloseConnectionException:
                self.invalid_mover = turn
                break
            if move == PASS:
                pass_count += 1
            elif isinstance(move, Point):
                pass_count = 0
                move_valid = self.move_ref.valid_move(curr.stone_type, move, self.history, self.history[0])
                if not move_valid:
                    self.invalid_mover = turn
                    break
            else:
                self.invalid_mover = turn
                break
            self.play_move(move, turn)
            turn = self.next_turn(turn)
        self.try_end_game()
        return sorted(self.determine_winner()), self.invalid_mover

    def play_move(self, move, turn):
        new_board = deepcopy(self.history[0])
        if move != PASS:
            new_board.place_and_update(self.players[turn].stone_type, move)
        self.history.insert(0, new_board)
        if len(self.history) == 4:
            self.history.pop()

    def determine_winner(self):
        if self.invalid_mover is not None:
            winner = self.next_turn(self.invalid_mover)
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
    
    def try_end_game(self):
        for p in self.players:
            try:
                p.end_game()
            except CloseConnectionException:
                pass
