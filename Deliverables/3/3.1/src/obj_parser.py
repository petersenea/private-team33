from board import Board
from stone import Stone
from constants import BOARD_DIM
from exceptions import GoCrazyException

def parse_board(matr):
   if (len(matr)!= BOARD_DIM or len(matr[0]) != BOARD_DIM):
      raise GoCrazyException
   return Board([[Stone(matr[i][j]) for i in range(BOARD_DIM)] for j in range(BOARD_DIM)])

def parse_boards(arr):
   return [parse_board(board) for board in arr]

def parse_stone(s):
   return Stone(s)