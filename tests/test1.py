import bindlib as bl

to_sdf = bl.AtomGroupConv(to='sdf')
to_smi = bl.AtomGroupConv(to='smi')

protein = bl.AtomGroupPDBReader('not hydrogen and not water')('data/5eol.pdb.gz')
ligand_test = protein.select('hetero').toAtomGroup()

ligands = bl.split_by_res(ligand_test)
for ligand in ligands:
    print(to_smi(ligand), ligand.getTitle())

ligand = bl.pick_ligand(ligand_test, '5QO')
print('-'*50)
print(to_smi(ligand), ligand.getTitle())
print('-'*50)

# print(ligand_test.getCoords())
print(ligand_test.getCoords().shape)
dmat = bl.get_distance_matrix(ligand_test, ligand_test)
# print(dmat)
# for atom in ligand_test:
#     resname = atom.getResname()
#     print(atom, resname)
conn = bl.get_connectivity(ligand_test, dmat)

for ag in conn:
    print(to_smi(ag))
    for atom in ag:
        print(atom, atom.getResname(), atom.getResnum(), atom.getChid())

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

print(to_smi(ligand))

ligand = bl.AtomGroupPDBReader()('data/5eol_5QO.pdb')
ligand_block = to_sdf(ligand)
open('out1.sdf', 'wt').write(ligand_block)

protein = bl.AtomGroupPDBReader('not hydrogen and not water')('data/1mwt.pdb.gz')
ligand = bl.AtomGroupPDBReader()('data/1mwt_PNM.pdb')
ligand_block = to_sdf(ligand)
smi = to_smi(ligand)
print(smi)
open('out2.sdf', 'wt').write(ligand_block)

mols = bl.OBMolSDFReader(verbose=True)('data/1mwt_PNM_docked.sdf')
