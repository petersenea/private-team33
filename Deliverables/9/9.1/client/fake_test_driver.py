import socket, json, sys, time
sys.path.append('./')
sys.path.append('../../5/5.1/src/')
sys.path.append('../../5/5.2/src/')
sys.path.append('../../3/3.1/src/')
sys.path.append('../../4/4.1/src/')
sys.path.append('../../8/8.1/')
from test_driver_base import execute_input
from constants import *
from go_player_random import GoPlayerCrazy, GoPlayerRandom
from go_player import GoPlayerContract
from go_admin import read_config, try_shutdown
from exceptions import *

## performs the actions read from the socket on the player
def receive_and_send(s, player):
    while True:
        data = s.recv(BUFFER_SIZE)
        
        # instead of checking for a -1
        if data == b'':
            break
        data = json.loads(data.decode('utf-8'))
        
        try:
            output = execute_input(player, data)
            s.send(json.dumps(output).encode('utf-8'))
        except GoCrazyException:
            output = GO_CRAZY
            s.send(json.dumps(output).encode('utf-8'))
            break
        except CloseConnectionException:
            print("closing connection")
            break

## creates socket
config = read_config('go.config')
TCP_IP = config["IP"]
TCP_PORT = config["port"]
BUFFER_SIZE = 55520
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for i in range(30):
    try:
        s.connect((TCP_IP, TCP_PORT))
        break
    except:
        time.sleep(1)
        continue

## instantiate remote player
player = GoPlayerRandom()
player_contract = GoPlayerContract(player)
receive_and_send(s, player_contract)
try_shutdown(s, socket.SHUT_RDWR)
s.close()