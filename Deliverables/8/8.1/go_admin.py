import sys, json, socket, importlib.util
sys.path.append('../../3/3.1/src/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../6/6.2/')
from go_player_basic import GoPlayerBasic
from go_player_net import GoPlayerNetwork
from go_referee import GoReferee
from board import empty_board
from stone import StoneEnum
from exceptions import *

class GoAdmin:

    def __init__(self):
        self.default_player = self.load_default_player()
        self.conn = self.create_server()
        self.network_player = self.load_network_player()

    def administrate_game(self):
        if not self.network_player:
            return ['player1']
        board = empty_board()
        referee = GoReferee([board], [self.default_player, self.network_player])
        out = referee.play_game()
        self.close_server()
        return out
    
    def create_server(self):
        config = read_config('go.config')
        TCP_IP = config["IP"]
        TCP_PORT = config["port"]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.settimeout(60)
        s.listen(1)
        conn, addr = s.accept()
        return conn

    def close_server(self):
        try_shutdown(self.conn, socket.SHUT_RDWR)
        self.conn.close()

        ## Update the Port
        config = read_config('go.config')
        config["port"] = new_port(config["port"])
        write_config(config, 'go.config')

    def load_default_player(self):
        path = read_config('go.config')["default-player"]
        spec = importlib.util.spec_from_file_location("module.name", path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        player = foo.GoPlayerBasic()
        player.register("player1")
        player.receive_stone(StoneEnum.BLACK)
        return player

    def load_network_player(self):
        network_player = GoPlayerNetwork(self.conn)
        try:
            network_player.register("player2")  
            network_player.receive_stone(StoneEnum.WHITE)
        except CloseConnectionException:
            return None
        return network_player


## Helper Functions
def read_config(path):
    with open(path) as json_data_file:
       return json.load(json_data_file)

def write_config(data, path):
    with open(path, "w") as json_file:
        json.dump(data, json_file)

def try_shutdown(s, how):
    try:
        s.shutdown(how)
    except:
        pass

def new_port(port):
    port += 1
    if port == 65535:
        port = 8000
    return port