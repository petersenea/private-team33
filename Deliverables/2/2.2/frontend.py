import sys
sys.path.append('../2.1')
sys.path.append('../Deliverables/2/2.1')
from backend_driver import json_parse_stdin
from backend import Backend
import json

# parse the stdin to json objects
objs = json_parse_stdin()

# for each series of 10, call the sort function
output = []
backend_obj = Backend()
for i in range(0, len(objs), 10):
    obj_slice = objs[i:i+10]
    if len(obj_slice) == 10:
        ret = json.dumps(backend_obj.sort(objs[i:i+10]))
        output.append(ret)

print("[{}]".format(",".join(output)))
