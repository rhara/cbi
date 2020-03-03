import sys
import openbabel
import numpy as np

status = False

vs = []
for line in open('tmp/89c61fbcd4ed45d48630a98e35eb60ff.tmpdir/protein.mol2', 'rt'):
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
    vs.append(float(it[8]))

vs = np.array(vs)
print(vs)

conv = openbabel.OBConversion()
conv.SetInAndOutFormats('.pdb', '.mol2')

mol = openbabel.OBMol()
conv.ReadFile(mol, 'tmp/89c61fbcd4ed45d48630a98e35eb60ff.tmpdir/protein_H.pdb')
conv.WriteFile(mol, 'out1.mol2')
mol.UnsetPartialChargesPerceived()
for d in dir(mol):
    print(d)

for i in range(mol.NumAtoms()):
    atom = mol.GetAtomById(i)
    print(atom.GetAtomicNum(), atom.GetPartialCharge(), vs[i])
    atom.SetPartialCharge(vs[i])

# mol.SetPartialChargesPerceived()
cont = conv.WriteString(mol).rstrip().split('\n')
cont[1] = 'PROTEIN'
cont[3] = 'PROTEIN'
cont[4] = 'USER_CHARGES'
print('\n'.join(cont))
