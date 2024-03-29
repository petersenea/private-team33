import sys, json
sys.path.append('../../../3/3.1/src')
from constants import *
from point import str_to_point
from stone import get_raw_stone
from output_formatter import format_board
from go_player import GoPlayer
from exceptions import *

class GoPlayerNetwork(GoPlayer):

   def __init__(self, conn):
      self.conn = conn
      self.buf_size = 256
      self.name = None
      self.stone_type = None
   
   def register(self):
      send_str = json.dumps([REGISTER])
      ret = self.send_and_receive(send_str)
      if ret != GO_CRAZY:
         self.name = ret
      return ret

   def receive_stone(self, stone_type):
      send_str = json.dumps([RECEIVE, get_raw_stone(stone_type)])
      ret = self.send_and_receive(send_str)
      if ret != GO_CRAZY:
         self.stone_type = stone_type
      return ret

   def choose_move(self, boards):
      boards_f = [format_board(x.board) for x in boards]
      send_str = json.dumps([MOVE, boards_f])
      ret = self.send_and_receive(send_str)
      try:
         return str_to_point(ret)
      except:
         return ret

   def end_game(self):
      send_str = json.dumps([END_GAME])
      try:
         ret = self.send_and_receive(send_str)
         return ret
      except ConnectionAbortedError:
         pass


   def send_and_receive(self, send_str):
      self.conn.send(send_str.encode('utf-8'))
      data = self.conn.recv(self.buf_size)
      if data == b'':
         raise CloseConnectionException("Client has disconnected.")
      data = json.loads(data.decode('utf-8'))
      return data
