from go_player import GoPlayer, protocol_registered, protocol_stone_set

class GoPlayerFile(GoPlayer):

   def __init__(self, points):
      super().__init__()
      self.points = points
      self.move_index = 0

   @protocol_registered
   @protocol_stone_set
   def choose_move(self, boards):
      curr = self.move_index
      self.move_index += 1
      return self.points[curr]