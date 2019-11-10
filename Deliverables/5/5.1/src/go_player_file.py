from go_player import GoPlayer

class GoPlayerFile(GoPlayer):

   def __init__(self, points):
      super().__init__()
      self.points = points
      self.move_index = 0

   def choose_move(self, boards):
      if self.move_index > len(self.points) - 1:
         return None
      curr = self.move_index
      self.move_index += 1
      return self.points[curr]