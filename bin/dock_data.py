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
    protein_fname = f'{datadir}/{pdbid}/{pdbid}.apo.pdb.gz'
    ligand_fname = f'{datadir}/{pdbid}/{pdbid}_{ligname}.sdf'
    ret = dict(count=count, pdbid=pdbid, ligname=ligname)
    output_fname = f'{datadir}/{pdbid}/{pdbid}_{ligname}.docked.sdf'
    if os.path.exists(output_fname):
        ret['success'] = True
        return ret
    if not os.path.exists(protein_fname) or not os.path.exists(ligand_fname):
        ret['success'] = False
        return ret
    sp.call(f'cbi_dock {protein_fname} {ligand_fname} -q', shell=True)
    ret['success'] = os.path.exists(output_fname)
    return ret

def main():
    global datadir
    parser = argparse.ArgumentParser()
    parser.add_argument('iname', type=str)
    parser.add_argument('datadir', type=str)
    parser.add_argument('--label', '-l', type=str)
    args = parser.parse_args()

    datadir = os.path.abspath(args.datadir)
    iname = args.iname
    q_labels = args.label.split(':') if args.label else None

    os.makedirs(datadir, mode=0o755, exist_ok=True)

    df = pd.read_csv(iname)

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
        success, count, pdbid, ligname = ret['success'], ret['count'], ret['pdbid'], ret['ligname']
        print(count, pdbid, ligname, success)

if __name__ == '__main__':
    main()
