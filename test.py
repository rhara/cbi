import bindlib.biomolecule as bio
import bindlib.smallmolecule as sm
import bindlib.math as pm

to_sdf = sm.PDBConv(to='sdf')
to_smi = sm.PDBConv(to='smi')

protein = bio.read_pdb_protein('data/5eol.pdb.gz')
ligand_test = protein.select('hetero and not water')

# print(ligand_test.getCoords())
print(ligand_test.getCoords().shape)
dmat = pm.get_distance_matrix(ligand_test, ligand_test)
# print(dmat)
# for atom in ligand_test:
#     resname = atom.getResname()
#     print(atom, resname)
conn = pm.get_connectivity(ligand_test, dmat)
found = False
for ag in conn:
    resname = ag[0].getResname()
    if resname == '5QO':
        found = True
        break
print(found)
ligand = ag
for atom in ligand:
    resname = atom.getResname()
    print(atom, resname)

print(to_smi(ligand, strip=True))

ligand = sm.read_pdb_ligand('data/5eol_5QO.pdb')
ligand_block = to_sdf(ligand)
open('out1.sdf', 'wt').write(ligand_block)

protein = bio.read_pdb_protein('data/1mwt.pdb.gz')
ligand = sm.read_pdb_ligand('data/1mwt_PNM.pdb')
ligand_block = to_sdf(ligand)
smi = to_smi(ligand, strip=True)
print(smi)
open('out2.sdf', 'wt').write(ligand_block)

sm.read_sdf_mols('data/1mwt_PNM_docked.sdf', verbose=True)
    
