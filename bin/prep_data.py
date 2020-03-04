#!/usr/bin/env python

import prody
import os
import pandas as pd
import multiprocessing as mp
import argparse
import subprocess as sp

datadir = None

def worker(args):
    count, pdbid, ligname = args
    protein_fname = f'{datadir}/{pdbid}/{pdbid}.pdb.gz'
    sp.call(f'cbi_prep {protein_fname} {ligname}', shell=True)
    return dict(count=count, pdbid=pdbid, ligname=ligname)

def main():
    global datadir
    parser = argparse.ArgumentParser()
    parser.add_argument('iname', type=str)
    parser.add_argument('datadir', type=str)
    parser.add_argument('--label', '-l', type=str)
    args = parser.parse_args()

    datadir = os.path.abspath(args.datadir)
    q_labels = args.label.split(':') if args.label else None

    os.makedirs(datadir, mode=0o755, exist_ok=True)

    df = pd.read_csv(args.iname)

    def gen():
        count = 0
        for i in df.index:
            r = df.loc[i]
            labels = r['label'].split(':')
            ok = True
            if q_labels:
                for q_label in q_labels:
                    if not q_label in labels:
                        ok = False
                        break
            if not ok:
                continue
            count += 1
            pdbid = r['pdbid']
            ligname = r['ligname']
            yield count, pdbid, ligname

    pool = mp.Pool(mp.cpu_count())
    for ret in pool.imap_unordered(worker, gen()):
        count, pdbid, ligname = ret['count'], ret['pdbid'], ret['ligname']
        print(count, pdbid)

if __name__ == '__main__':
    main()
