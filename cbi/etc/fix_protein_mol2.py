import sys
import openbabel as ob

iname_charge = sys.argv[1]
iname_protein_H = sys.argv[2]
oname = sys.argv[3]

status = False

vs = []
for line in open(iname_charge, 'rt'):
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

conv = ob.OBConversion()
conv.SetInAndOutFormats('pdb', 'mol2')

mol = ob.OBMol()
conv.ReadFile(mol, iname_protein_H)
mol.UnsetPartialChargesPerceived()

for i in range(mol.NumAtoms()):
    atom = mol.GetAtomById(i)
    v = atom.GetPartialCharge()
    atom.SetPartialCharge(vs[i])

mol.SetPartialChargesPerceived()

cont = conv.WriteString(mol).rstrip().split('\n')
cont[1] = 'PROTEIN'
cont[3] = 'PROTEIN'
cont[4] = 'USER_CHARGES'
out = open(oname, 'wt')
print('\n'.join(cont), file=out)
