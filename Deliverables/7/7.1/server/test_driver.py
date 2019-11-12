import sys, socket, json, time
sys.path.append('../../3/3.1/src')
sys.path.append('../../5/5.1/src')
sys.path.append('../../../5/5.1/src')
from point import Point, get_raw
from constants import GO_CRAZY
from json_parser import json_parse_stdin
from go_player_net import GoPlayerNetwork
from test_driver_base import execute_input

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

def format_obj(obj):
    if isinstance(obj, str):
        return str
    elif isinstance(obj, Point):
        return get_raw(obj)
    else:
        raise Exception("bad type passed to format")

if __name__ == "__main__":
    ## Read Stdin
    objs = json_parse_stdin()

    ## Establish Connection
    config = read_config('go.config')
    TCP_IP = config["IP"]
    TCP_PORT = config["port"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.settimeout(60)
    s.listen(1)
    conn, addr = s.accept()
    
    player = GoPlayerNetwork(conn)
    output = []
    for obj in objs:
        ret = execute_input(player, obj)
        if ret:
            output.append(ret)
        if ret == GO_CRAZY:
            break

    ## Close the connection
    conn.send(json.dumps(-1).encode('utf-8'))
    try_shutdown(conn, socket.SHUT_RDWR)
    conn.close()
    try_shutdown(s, socket.SHUT_RDWR)
    s.close()

    ## Update the Port
    config["port"] = new_port(TCP_PORT)
    write_config(config, 'go.config')

    ## Stdout
    print (json.dumps(list(output)))
