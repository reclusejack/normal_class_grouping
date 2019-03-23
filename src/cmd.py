import sys
from group import *
from load_data import *
from write_data import *

orig_data = [] 
group_data = [] 
rule = [] 
if len(sys.argv) != 5:

    print("%d\n" %len(sys.argv))
else:
    total_class = int(sys.argv[1])
    boy_class = int(sys.argv[2])
    girl_class = int(sys.argv[3])
    filename = sys.argv[4]
    load_data(filename, orig_data, rule)
    group_data = grouping(orig_data, total_class, boy_class, girl_class, rule)
    data = copy.deepcopy(group_data)
    writefile(data, filename, total_class, boy_class, girl_class)
