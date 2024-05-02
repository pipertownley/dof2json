import argparse
import json

from dof2json.dof2json import DigitalObstacleParser, strip_headers

parser = argparse.ArgumentParser(description='Parse DOF into json.')
parser.add_argument('infiles', type=str, nargs='+',
                    help='a list of input files e.g FILE1 FILE2 FILE3')
parser.add_argument('outfile', type=str, help="the output filename")
args = parser.parse_args()

files = args.infiles
outfile = args.outfile
json_out = []

for fn in files:
    f = open(fn, 'r')
    f = strip_headers(f)
    for ln in f:
        do = DigitalObstacleParser(ln)
        json_out.append(do.data)
try:
    fo = open(outfile, 'w')
    fo.write(json.dumps(json_out))
    fo.close()
except Exception as err:
    raise err
