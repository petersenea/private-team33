import socket
import json
import sys
sys.path.append('server/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')

from test_driver_base import execute_input
from go_player_adv import GoPlayerAdv
from go_player import GoPlayerContract
from test_driver import read_config



config = read_config('go.config')
TCP_IP = config["IP"]
TCP_PORT = config["port"]
config1 = read_config('go-player.config')
N = config1["depth"]
BUFFER_SIZE = 5552


def receive_and_send(s, player):
    while True:
        data = s.recv(BUFFER_SIZE)
        data = json.loads(data)
        if data == -1:
            break
        try:
            output = execute_input(player, data)
            s.send(json.dumps(output).encode('utf-8'))
        except:
            output = "GO has gone crazy!"
            s.send(json.dumps(output).encode('utf-8'))
            break
            
        
    s.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
player = GoPlayerAdv(N)

player_contract = GoPlayerContract(player)


receive_and_send(s, player_contract)
