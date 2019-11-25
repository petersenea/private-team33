import sys, socket, importlib, math, random
sys.path.append('../../3/3.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../6/6.2/')
sys.path.append('../../8/8.1')
from board import empty_board
from stone import StoneEnum
from go_referee import GoReferee
from exceptions import CloseConnectionException
from go_player_net import GoPlayerNetwork
from go_player import GoPlayerContract
from go_admin import read_config, write_config, new_port, try_shutdown

## Shared Functions
def create_server(n):
    config = read_config('go.config')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config["IP"], config["port"]))
    s.settimeout(60)
    s.listen(n)
    return s

def close_server(s):
    config = read_config('go.config')
    config["port"] = new_port(config["port"])
    write_config(config, 'go.config')
    try_shutdown(s, socket.SHUT_RDWR)
    s.close()

def load_default_player():
    path = read_config('go.config')["default-player"]
    spec = importlib.util.spec_from_file_location("module.name", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    inner = foo.GoPlayerRandom()
    player = GoPlayerContract(inner)
    return player

def load_network_player(conn):
    inner = GoPlayerNetwork(conn)
    player = GoPlayerContract(inner)
    return player

def indices(lst, elem):
    return [i for i, x in enumerate(lst) if x == elem]

def argsort(seq):
    seq = list(map(lambda x: -x, seq))
    return sorted(range(len(seq)), key=seq.__getitem__)
    
def larger_power_of_two(n):
    return 2 if n < 2 else 2**(n - 1).bit_length()

def get_winner(arr):
    if len(arr) == 1:
        return arr[0]
    if random.random() < 0.5:
        return arr[0]
    return arr[1]

## Single Elim Tournament
class SingleElimTournament:

    def __init__(self, n):
        self.n = n
        self.total_n = larger_power_of_two(n)
        self.ranks = [0] * self.total_n
        self.round = 0
        self.s = create_server(n)
        connections = [self.s.accept()[0] for i in range(n)]
        network_players = [load_network_player(c) for c in connections]
        default_players = [load_default_player() for i in range(self.total_n - n)]
        self.players = network_players + default_players
        self.names = [self.try_register(i) for i in range(self.total_n)]

    def host_tournament(self):
        rounds = int(math.log(self.total_n, 2))
        for i in range(rounds):
            print ("\nRound: {}".format(self.round))
            self.play_round()
            self.round += 1
        self.output_winners()
        close_server(self.s)

    def output_winners(self):
        print ("\n===========")
        print ("Cup Results")
        print ("===========")
        sorted_players = argsort(self.ranks)
        rank = 1
        for ind in sorted_players:
            print("Rank {}: {}".format(rank, self.names[ind]))
            rank += 1

    def play_round(self):
        games = int(self.total_n / (2 ** (self.round + 1)))
        for i in range(games):
            a, b = indices(self.ranks, self.round)[:2]
            self.play_game(a, b)

    def play_game(self, a, b):
        player1 = self.players[a]
        try:
            player1.receive_stone(StoneEnum.BLACK)
        except CloseConnectionException:
            self.update_score(b, a)
            return

        player2 = self.players[b]
        try:
            player2.receive_stone(StoneEnum.WHITE)
        except CloseConnectionException:
            self.update_score(a, b)
            return

        ref = GoReferee([player1, player2])
        winners, _ = ref.play_game()
        winner = get_winner(winners)
        print ("-- {} advances".format(winner))
        if winner == self.names[a]:
            self.update_score(a, b)
        else:
            self.update_score(b, a)
    
    def update_score(self, winner, loser):
        self.ranks[winner] += 1
        self.ranks[loser] -= 1
    
    def try_register(self, ind):
        try:
            return self.players[ind].register()
        except CloseConnectionException:
            self.players[ind] = load_default_player()
            return self.players[ind].register()
