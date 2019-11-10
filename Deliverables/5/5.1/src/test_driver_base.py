import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from json_parser import json_parse_stdin
from point import get_raw
from referee_formatter import format_pretty_json
from obj_parser import parse_boards, parse_stone
from constants import REGISTER, RECEIVE, MOVE
from go_player_basic import GoPlayerBasic

def execute_input(player, arr):
   if arr[0] == REGISTER:
      return player.register()
   elif arr[0] == RECEIVE:
      stone = parse_stone(arr[1])
      return player.receive_stone(stone.get_type())
   elif arr[0] == MOVE:
      boards = parse_boards(arr[1])
      output = player.choose_move(boards)
      if isinstance(output, str):
         return output
      return get_raw(output)
   else:
      return "GO has gone crazy!"

if __name__ == "__main__":
   player = GoPlayerBasic()
   objs = json_parse_stdin()
   output = filter (lambda x: x, [execute_input(player, obj) for obj in objs])
   print(format_pretty_json(list(output)))
