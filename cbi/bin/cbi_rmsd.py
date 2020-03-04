#!/usr/bin/env python

import cbi
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ref_iname', type=str)
    parser.add_argument('fit_iname', type=str)
    args = parser.parse_args()

    ref_iname = args.ref_iname
    fit_iname = args.fit_iname

    refmol = cbi.OBMolPDBReader()(ref_iname)
    fitmols = cbi.OBMolSDFReader()(fit_iname)

    count = 0
    for fitmol in fitmols:
        count += 1
        rmsd = cbi.get_rmsd(refmol, fitmol)
        print(count, rmsd)

if __name__ == "__main__":
    main()
