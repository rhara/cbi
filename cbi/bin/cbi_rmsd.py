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

    rmsds = cbi.get_rmsd_from_files(ref_iname, fit_iname)

    for count, rmsd in enumerate(rmsds, start=1):
        print(count, rmsd)

if __name__ == "__main__":
    main()
