from constants import PASS
from exceptions import GoCrazyException

class Point:
   def __init__(self, x, y):
      self.x, self.y = x, y

def parse_move(s):
   if s == PASS:
      return PASS
   return str_to_point(s)

def str_to_point(s):
   try:
      x_str, y_str = s.split("-")
      x, y = int(x_str) - 1, int(y_str) - 1
      return Point(x, y)
   except:
      raise GoCrazyException("invalid string input for point")

def str_to_tupl(s):
   pt = str_to_point(s)
   return ((pt.x, pt.y))

def get_raw(tupl):
   # if isinstance(tupl, Point):
   #    tupl = (tupl.x, tupl.y)
   # x, y = tupl
   # return "{}-{}".format(x + 1, y + 1)

   if isinstance(tupl, Point):
      tupl = (tupl.x, tupl.y)
      x, y = tupl
      return "{}-{}".format(x + 1, y + 1)
   elif isinstance(tupl, tuple):
      x, y = tupl
      return "{}-{}".format(x + 1, y + 1)
   else:
      return "not valid"

def is_point(thing):
   try:
      str_to_pont(thing)
      return True
   except:
      return False