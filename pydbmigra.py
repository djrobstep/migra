import sys
from migra import do_command
import version
import argparse
a=''
try:
    a=sys.argv[1]
except:
    pass
if a=='--version':
    print(version.version_dict)
else:
    do_command()