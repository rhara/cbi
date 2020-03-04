import glob
import subprocess as sp

flist = glob.glob('data/*/*.docked.sdf')

for f in flist:
    pdbid = f[5:9]
    ligname = f[15:18]
    ref = f'data/{pdbid}/{pdbid}_{ligname}.pdb'
    fit = f'data/{pdbid}/{pdbid}_{ligname}.docked.sdf'
    sp.call(f'cbi_rmsd {ref} {fit}', shell=True)
