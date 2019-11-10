import sys, socket, json
sys.path.append('../../3/3.1/src')
sys.path.append('../../5/5.1/src')
sys.path.append('../../../5/5.1/src')
from json_parser import json_parse_stdin
from go_player_net import GoPlayerNetwork
from test_driver_base import execute_input

def read_config(path):
    with open(path) as json_data_file:
       return json.load(json_data_file)

if __name__ == "__main__":
    ## Read Stdin
    objs = json_parse_stdin()

    ## Establish Connection
    config = read_config('go.config')
    TCP_IP = config["IP"]
    TCP_PORT = config["port"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()

    player = GoPlayerNetwork(conn)
    output = []
    for obj in objs:
        ret = execute_input(player, obj)
        if ret:
            output.append(ret)
        if ret == "GO has gone crazy!":
            break
   
    ## Stdout
    # print (json.dumps(list(output)))
    sys.stdout.write(json.dumps(list(output)))
   
    ## Close the connection
    conn.send(json.dumps(-1).encode('utf-8'))
    conn.close()

