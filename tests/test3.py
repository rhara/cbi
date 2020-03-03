import os, sys
import pandas as pd
import bindlib as bl
import prody

def get_catalog():
    df = pd.read_csv('../cbi_prep/data.csv')
    D = {}
    for i in df.index:
        r = df.loc[i]
        pdbid = r['pdbid']
        ligname = r['ligname']
        D[pdbid] = ligname
    return D

def gen():
    done = False
    for root, dirs, files in os.walk('../cbi_prep/data'):
        if done:
            break
        for f in files:
            if f.endswith('.pdb.gz') and not f.endswith('.apo.pdb.gz'):
                fname = f'{root}/{f}'
                yield fname
                done = True

cat = get_catalog()

tleap = bl.TLEAP()
tleap(sys.argv[1])

for fname in gen():
    pdbid = os.path.basename(fname)[:4]

    ligname = cat.get(pdbid)
    if ligname is None:
        print(pdbid, f'Error: no ligname entry')
        continue
    apo = bl.AtomGroupPDBReader('protein and not hydrogen')(fname)
    hetero = bl.AtomGroupPDBReader('hetero and not hydrogen and not water')(fname)
    if hetero is None:
        print(pdbid, f'Error: no appropriate hetero entry in PDB')
        continue

    ligand = bl.pick_ligand(hetero, ligname)

    if ligand is None:
        print(pdbid, f'Error: no ligand "{ligname}"')
        continue

    chains = bl.get_contact_chains(apo, ligand)
    if chains is None:
        print(pdbid, f'Error: no contact with protein "{pdbid}" and {ligand.getTitle()}')
        continue
