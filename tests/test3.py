import os, sys
import pandas as pd
import bindlib as bl
import prody

apo_fname = sys.argv[1] #apo
ligand_fname = sys.argv[2]

tleap = bl.TLEAP()
workdir = tleap(apo_fname)
protein_fname = f'{workdir}/protein_H_charged.mol2'
bl.smina_dock(protein_fname, ligand_fname, ncpu=10, workdir=workdir)
print(workdir)
