import sys
import openbabel

status = False

iname = sys.argv[1]
oname = sys.argv[2]

out = open(oname, 'wt')
for line in open(iname, 'rt'):
    line = line.rstrip()
    if line.startswith('@<TRIPOS>ATOM'):
        status = True
        continue
    elif line.startswith('@<TRIPOS>'):
        status = False
        continue
    if not status:
        continue
    it = line.split()
    print(it[8], file=out)


