#!/usr/bin/env python

import glob
import subprocess as sp

ng = 0
count = 0
good = 0
for f in glob.glob('data/*/*.docked.sdf'):
    pdbid = f[5:9]
    ligname = f[15:18]
    ref = f'data/{pdbid}/{pdbid}_{ligname}.pdb'
    fit = f'data/{pdbid}/{pdbid}_{ligname}.docked.sdf'
    output = sp.check_output(f'cbi_rmsd {ref} {fit}', shell=True, universal_newlines=True)
    lines = output.split('\n')
    rmsd = None
    if 1 <= len(lines) and lines[0].startswith('1'):
        count += 1
        rmsd = float(lines[0].split()[1])
        if rmsd <= 2.0:
            good += 1
    else:
        ng += 1
    percent = round(good/count*100, 1)
    if 0 < count:
        print(f'{pdbid} {rmsd} count={count} good={good} (percent={percent}%) ng={ng}')
