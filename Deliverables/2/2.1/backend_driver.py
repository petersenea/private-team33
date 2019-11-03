import sys
import json
from backend import Backend

def json_parse_stdin():
    #this is the backend driver test. Reads all lines from input
    from_stdin = []
    for line in sys.stdin:
        if line != "":
            from_stdin.append(line)

    #parses into 10 proper JSON objects
    str_input = "".join(from_stdin)
    decoder = json.JSONDecoder()
    objs = []
    i = 0
    while i < len(str_input):
        try:
            obj, index = decoder.raw_decode(str_input[i:])
            i += index
            objs.append(obj)
        except:
            i += 1

    return objs

if __name__ == "__main__":
    objs = json_parse_stdin()
    backend = Backend()
    print (json.dumps(backend.sort(objs)))