import sys
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from stone import StoneEnum
from move_referee import MoveReferee

class GoPlayer:

   ## Constructor
   def __init__(self):
      self.name = None
      self.stone_type = None
      self.move_referee = MoveReferee()
   
   ## Public Methods
   def register(self, name="no name"):
      self.name = name
      return name

   def receive_stone(self, stone_type):
      self.stone_type = stone_type

   def choose_move(self, boards):
      pass

class GoPlayerContract(GoPlayer):

   def __init__(self, player):
      self.player = player
      self.is_registered = False 
      self.has_stones = False

   @property
   def stone_type(self):
      return self.player.stone_type

   @property
   def name(self):
      return self.player.name
   
   def register(self, name="no name"):
      # if self.is_registered:
      #    raise Exception("register called multiple times")
      # else:
      #    self.is_registered = True
      # return self.player.register(name)


      if self.player.name != None:
         raise Exception("register called multiple times")
      return self.player.register(name)
   
   def receive_stone(self, stone_type):
      # if not self.is_registered:
      #    raise Exception("receive called before register")
      # elif self.has_stones:
      #    raise Exception("receive called twice")
      # else:
      #    self.has_stones = True
      # self.player.receive_stones(stone_type)


      if not self.player.name:
         raise Exception("receive called before register")
      elif self.player.stone_type:
         raise Exception("receive called twice")
      self.player.receive_stone(stone_type)
   
   def choose_move(self, boards):
      # if not self.has_stones:
      #    raise Exception("choose move called before receive")
      # if len(boards) > 3:
      #    raise Exception("bad boards passed in")
      # return self.player.choose_move(boards)

      if not self.player.stone_type:
         raise Exception("choose move called before receive")
      if len(boards) > 3:
         raise Exception("bad boards passed in")
      return self.player.choose_move(boards)


