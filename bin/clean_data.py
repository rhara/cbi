import os, glob
import subprocess as sp
import re

pat = re.compile('^(.*)\.pdb\.gz$')

for f in glob.glob('data/*/*'):
    if os.path.isdir(f):
        continue

    leave = False

    m = pat.search(f)
    if m:
        if m.group(1).endswith('.apo'):
            leave = False
        else:
            leave = True

    if not leave:
        sp.call(f'rm {f}', shell=True)
