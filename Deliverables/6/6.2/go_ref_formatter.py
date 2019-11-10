import sys
sys.path.append('../../3/3.1/src/')
from output_formatter import format_board
from board import Board
from stone import StoneEnum, get_raw_stone

def format_board_obj(board):
   return format_board(board.board)

def format_obj(obj):
   if isinstance(obj, list) and isinstance(obj[0], Board):
      return [format_board_obj(x) for x in obj]
   elif isinstance(obj, StoneEnum):
      return get_raw_stone(obj)
   return obj
