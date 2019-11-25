import sys, socket, importlib, math, random
sys.path.append('../../3/3.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../6/6.2/')
sys.path.append('../../8/8.1')
sys.path.append('../')

from single_elim import get_winner, load_network_player, load_default_player, create_server, close_server
from stone import StoneEnum
from go_referee import GoReferee
from exceptions import CloseConnectionException

class RoundRobinTournament:

    def __init__(self, n):
        self.n = n
        self.points_arr = [[None for i in range(n)] for j in range(n)]
        self.s = create_server(n)
        connections = [self.s.accept()[0] for i in range(n)]
        self.players = [load_network_player(c) for c in connections]
        self.names = [p.register() for p in self.players]
        self.cheaters = []

    def host_tournament(self):
        for i in range(len(self.points_arr)):
            for j in range(len(self.points_arr[0])):
                if self.points_arr[i][j] == None and i != j:
                    self.play_game(i,j)
        self.output_winners()
        close_server(self.s)

    def output_winners(self):
        print ("\n===============")
        print ("League Results")
        print ("===============")

        for i in range(len(self.points_arr)):
            _sum = 0
            for j in range(len(self.points_arr[0])):
                if self.points_arr[i][j] != None:
                    _sum += self.points_arr[i][j]
            print("Player: " + self.names[i] + ", Score: " + str(_sum))

        print("\n== Cheaters ==")
        if not len(self.cheaters):
            print ("there were no cheaters")
            return
        for i in range(len(self.cheaters)):
            print("Player: " + self.cheaters[i] + ", Score: 0" )

    def play_game(self, a, b):
        player1 = self.players[a]
        try:
            player1.receive_stone(StoneEnum.BLACK)
        except CloseConnectionException:
            self._update_score(b, a)
            self._update_score_cheater(a)
            self.cheaters.append(self.names[a])
            self._replace_cheater(a)
            return
        
        player2 = self.players[b]
        try:
            player2.receive_stone(StoneEnum.WHITE)
        except CloseConnectionException:
            self._update_score(a, b)
            self._update_score_cheater(b)
            self.cheaters.append(self.names[b])
            self._replace_cheater(b)
            self.players[a].end_game()
            return

        ref = GoReferee([player1, player2])
        winners, was_cheater = ref.play_game()
        winner_name = get_winner(winners)
        winner_index = self._get_player_index(winner_name)
        loser_name = self._get_loser(winner_name, [player1, player2])
        loser_index = self._get_player_index(loser_name)

        # update score first
        self._update_score(winner_index, loser_index)

        # check if cheater, edit points_arr and replace player if there was a cheater
        if was_cheater != None:
            self._update_score_cheater(loser_index)
            self.cheaters.append(loser_name)
            self._replace_cheater(loser_index)

    def _get_loser(self, winner_name, players):
        if winner_name == players[0].name:
            loser_name = players[1].name
        else:
            loser_name = players[0].name
        return loser_name

    def _get_player_index(self, name):
        return self.names.index(name)

    def _replace_cheater(self, cheater_index):
        self.players[cheater_index] = load_default_player()
        self.names[cheater_index] = self.players[cheater_index].register()

    def _update_score(self, winner_index, loser_index):
        self.points_arr[winner_index][loser_index] = 1
        self.points_arr[loser_index][winner_index] = 0

    def _update_score_cheater(self, cheater_index):
        for i in range(len(self.points_arr)):
            if self.points_arr[cheater_index][i] == 1:
                self.points_arr[cheater_index][i] = 0
        for i in range(len(self.points_arr)):
            if self.points_arr[i][cheater_index] == 0:
                self.points_arr[i][cheater_index] = 1