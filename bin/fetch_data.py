#!/usr/bin/env python

import prody
import os
import pandas as pd
import multiprocessing as mp
import argparse

datadir = None

def worker(args):
    count, pdbid = args
    os.makedirs(f'{datadir}/{pdbid}', mode=0o755, exist_ok=True)
    os.chdir(f'{datadir}/{pdbid}')
    prody.fetchPDB(pdbid)
    return dict(count=count, pdbid=pdbid)

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
            yield count, pdbid

    pool = mp.Pool(mp.cpu_count())
    for ret in pool.imap_unordered(worker, gen()):
        count, pdbid = ret['count'], ret['pdbid']
        print(count, pdbid)

if __name__ == '__main__':
    main()
