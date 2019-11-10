import unittest
import sys
sys.path.append('../')
sys.path.append('../../../3/3.1/src/')
sys.path.append('../../../4/4.1/src/')
sys.path.append('../../../5/5.1/src/')
from copy import deepcopy
from point import Point
from stone import StoneEnum, make_stone
from board import Board
from go_player import GoPlayer
from go_referee import GoReferee

class TestHelpers(unittest.TestCase):    

   def test_play_move_pass(self):
      ref = init_ref()
      ref.play_move("pass", 0)
      self.assertEqual(2, len(ref.history))
      self.assertTrue(ref.history[0].equal(ref.history[1]))
   
   def test_play_move_pass_deep(self):
      ref = init_ref()
      ref.play_move(Point(0, 0), 0)
      self.assertEqual(2, len(ref.history))
      self.assertFalse(ref.history[0].equal(ref.history[1]))
      ref.play_move("pass", 1)
      self.assertEqual(3, len(ref.history))
      self.assertTrue(ref.history[0].equal(ref.history[1]))
   
   def test_play_move_len(self):
      ref = init_ref()
      ref.play_move(Point(0, 0), 0)
      ref.play_move(Point(0, 1), 1)
      ref.play_move(Point(0, 2), 0)
      self.assertEqual(3, len(ref.history))
      ref.play_move(Point(0, 3), 1)
      self.assertEqual(3, len(ref.history))

   def test_winners_invalid_second(self):
      ref = init_ref()
      winners = ref.determine_winner(1)
      self.assertEqual("name1", winners[0])

   def test_winners_invalid_first(self):
      ref = init_ref()
      winners = ref.determine_winner(0)
      self.assertEqual("name2", winners[0])
   
   def test_winners_normal(self):
      ref = init_ref()
      ref.play_move(Point(0, 0), 0)
      winners = ref.determine_winner(None)
      self.assertEqual("name1", winners[0])
   
   def test_winners_tie(self):
      ref = init_ref()
      ref.play_move(Point(0, 0), 0)
      ref.play_move(Point(0, 1), 1)
      winners = ref.determine_winner(None)
      self.assertTrue("name1" in winners)
      self.assertTrue("name2" in winners)

   def test_next_step(self):
      ref = init_ref()
      self.assertEqual(1, ref.next_turn(0))
      self.assertEqual(0, ref.next_turn(1))

def init_ref():
   player1 = GoPlayer()
   player1.register("name1")
   player1.receive_stone(StoneEnum.BLACK)

   player2 = GoPlayer()
   player2.register("name2")
   player2.receive_stone(StoneEnum.WHITE)

   board = Board([[make_stone(None) for i in range(5)] for j in range(5)], 5)
   return GoReferee([board], [player1, player2])

if __name__ == '__main__':
   unittest.main()