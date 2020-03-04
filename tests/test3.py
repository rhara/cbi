import cbi
import sys

apo_fname = sys.argv[1] #apo
ligand_fname = sys.argv[2]

tleap = cbi.TLEAP()
workdir = tleap(apo_fname)
protein_fname = f'{workdir}/protein_H_charged.mol2'
cbi.smina_dock(protein_fname, ligand_fname, ncpu=10, workdir=workdir)

refmol = cbi.OBMolSDFReader()(ligand_fname)[0]
fitmol_fname = f'{workdir}/docked.sdf'
fitmols = cbi.OBMolSDFReader()(fitmol_fname)
count = 0
print(workdir)
for fitmol in fitmols:
    count += 1
    rmsd = cbi.get_rmsd(refmol, fitmol)
    print(count, rmsd)
