import os
import pandas as pd
import bindlib as bl

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
    for root, dirs, files in os.walk('../cbi_prep/data'):
        for f in files:
            if f.endswith('.pdb.gz') and not f.endswith('.apo.pdb.gz'):
                fname = f'{root}/{f}'
                yield fname

cat = get_catalog()

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

    pocket = bl.get_pocket_residues(apo, ligand)

    if pocket is None:
        print(pdbid, f'Error: could not find pocket of {ligand.getTitle()} in "{pdbid}"')
        continue

    print(pdbid, ligand.getTitle(), ligand.numAtoms(), apo.numAtoms(), '->', chains.numAtoms(), '->', pocket.numAtoms())
