import sys
sys.path.append('../../3/3.1/src')
sys.path.append('../../5/5.1/src')
from json_parser import json_parse_stdin
from constants import BOARD_DIM
from board import Board
from point import parse_move
from stone import StoneEnum, make_stone
from go_player_file import GoPlayerFile
from go_referee import GoReferee
from go_ref_formatter import format_obj

if __name__ == "__main__":
   objs = json_parse_stdin()

   ## Initialize Stones, Points
   names, points = objs[:2], [parse_move(x) for x in objs[2:]]
   board = Board([[make_stone(None) for i in range(BOARD_DIM)] for j in range(BOARD_DIM)])

   ## Initialize Players
   player1 = GoPlayerFile(points[::2])
   player1.register(names[0])
   player1.receive_stone(StoneEnum.BLACK)

   player2 = GoPlayerFile(points[1::2])
   player2.register(names[1])
   player2.receive_stone(StoneEnum.WHITE)

   ## Initialize Go Ref
   go_referee = GoReferee([board], [player1, player2])
   output = go_referee.play_game()
   raw_output = list(map(format_obj, output))
   print (raw_output)