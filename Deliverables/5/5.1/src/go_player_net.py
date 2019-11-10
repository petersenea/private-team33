import sys, json
sys.path.append('../../../3/3.1/src')
from stone import get_raw_stone
from output_formatter import format_board
from go_player import GoPlayer

class GoPlayerNetwork(GoPlayer):

   def __init__(self, conn):
      self.conn = conn
      self.buf_size = 256
   
   def register(self, name="no name"):
      send_str = json.dumps(["register"])
      return self.send_and_receive(send_str)

   def receive_stone(self, stone_type):
      send_str = json.dumps(["receive-stones", get_raw_stone(stone_type)])
      return self.send_and_receive(send_str)
   
   def choose_move(self, boards):
      boards_f = [format_board(x.board) for x in boards]
      send_str = json.dumps(["make-a-move", boards_f])
      return self.send_and_receive(send_str)

   def send_and_receive(self, send_str):
      self.conn.send(send_str.encode('utf-8'))
      data = json.loads(self.conn.recv(self.buf_size).decode('utf-8'))
      return data