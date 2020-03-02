import proobr.biomolecule as bio
import proobr.smallmolecule as sm

to_sdf = sm.PDBConv(to='sdf')
to_smi = sm.PDBConv(to='smi')

protein = bio.read_pdb_protein('data/5eol.pdb.gz')
ligand = sm.read_pdb_ligand('data/5eol_5QO.pdb')
ligand_block = to_sdf(ligand)
smi = to_smi(ligand, strip=True)
print(smi)
open('out1.sdf', 'wt').write(ligand_block)

protein = bio.read_pdb_protein('data/1mwt.pdb.gz')
ligand = sm.read_pdb_ligand('data/1mwt_PNM.pdb')
ligand_block = to_sdf(ligand)
smi = to_smi(ligand, strip=True)
print(smi)
open('out2.sdf', 'wt').write(ligand_block)

sm.read_sdf_mols('data/1mwt_PNM_docked.sdf', verbose=True)
    
