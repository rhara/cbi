#!/usr/bin/env python

import sys, os, argparse
import cbi

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('apo_iname', type=str)
    parser.add_argument('mol_iname', type=str)
    args = parser.parse_args()

    apo_iname = args.apo_iname
    mol_iname = args.mol_iname

    pdbid = os.path.basename(apo_iname)[:4]

    tleap = cbi.TLEAP()
    workdir = tleap(apo_iname)
    protein_fname = f'{workdir}/{pdbid}_protein_H_charged.mol2'
    ncpu = max(os.cpu_count()-2, 1)
    cbi.smina_dock(protein_fname, mol_iname, ncpu=ncpu)
    print(f'{workdir}/{os.path.basename(mol_iname)[:-4]}_docked.sdf')

    ### cleaning
    for f in os.listdir(workdir):
        if '_tmp_' in f:
            os.system(f'rm {workdir}/{f}')

if __name__ == '__main__':
    main()
