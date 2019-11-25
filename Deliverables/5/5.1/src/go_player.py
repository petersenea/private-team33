import sys, random
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
from constants import *
from stone import StoneEnum
from move_referee import MoveReferee
from exceptions import GoCrazyException

class GoPlayer:

   ## Constructor
   def __init__(self):
      self.name = None
      self.stone_type = None
      self.move_referee = MoveReferee()
   
   ## Public Methods
   def register(self):
      return "no name"

   def receive_stone(self, stone_type):
      self.stone_type = stone_type

   def end_game(self):
      return "OK"

   def choose_move(self, boards):
      pass

class GoPlayerContract():

   def __init__(self, player):
      self.action = REGISTER
      self.player = player   
   
   def register(self):
      if self.action != REGISTER:
         raise GoCrazyException("Expected action was {}".format(self.action))
      self.action = RECEIVE
      self.name = self.player.register()
      return self.name
   
   def receive_stone(self, stone_type):
      if self.action != RECEIVE:
         raise GoCrazyException("Expected action was {}".format(self.action))
      self.action = MOVE
      self.player.receive_stone(stone_type)
      self.stone_type = stone_type

   def choose_move(self, boards):
      if self.action != MOVE:
         raise GoCrazyException("Expected action was {}".format(self.action))
      return self.player.choose_move(boards)
   
   def end_game(self):
      self.action = RECEIVE
      return self.player.end_game()
