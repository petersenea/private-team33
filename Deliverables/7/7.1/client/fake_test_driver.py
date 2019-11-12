import socket, json, sys, time
sys.path.append('server/')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')

from test_driver_base import execute_input
from go_player_adv import GoPlayerAdv
from go_player import GoPlayerContract
from test_driver import read_config, try_shutdown
from constants import GO_CRAZY

def receive_and_send(s, player):
    while True:
        data = s.recv(BUFFER_SIZE)
        data = json.loads(data.decode('utf-8'))
        if data == -1:
            break
        try:
            output = execute_input(player, data)
            s.send(json.dumps(output).encode('utf-8'))
        except:
            output = GO_CRAZY
            s.send(json.dumps(output).encode('utf-8'))
            break

config = read_config('go.config')
TCP_IP = config["IP"]
TCP_PORT = config["port"]
config1 = read_config('go-player.config')
N = config1["depth"]
BUFFER_SIZE = 55520
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for i in range(30):
    try:
        s.connect((TCP_IP, TCP_PORT))
        break
    except:
        time.sleep(1)
        continue

player = GoPlayerAdv(N)
player_contract = GoPlayerContract(player)
receive_and_send(s, player_contract)
try_shutdown(s, socket.SHUT_RDWR)
s.close()