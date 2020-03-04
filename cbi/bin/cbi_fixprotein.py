#!/usr/bin/env python

import argparse
import openbabel as ob

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('iname_charge', type=str)
    parser.add_argument('iname_protein_H', type=str)
    parser.add_argument('oname', type=str)
    args = parser.parse_args()

    iname_charge = args.iname_charge
    iname_protein_H = args.iname_protein_H
    oname = args.oname

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

if __name__ == '__main__':
    main()
