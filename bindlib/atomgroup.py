import numpy as np
from . import math

def split_by_res(ag):
    ress = {}
    for i, atom in enumerate(ag):
        resname = atom.getResname()
        resnum = atom.getResnum()
        chid = atom.getChid()
        if (resname, resnum, chid) not in ress:
            ress[resname, resnum, chid] = []
        ress[resname, resnum, chid].append(i)
    ress = list(ress.items())
    ress.sort(key=lambda r: (-len(r[1]), r[0][2], r[0][1]))
    ags = []
    for r in ress:
        idxs = r[1]
        ags.append(ag[idxs].toAtomGroup())
        ags[-1].setTitle(f'{r[0][0]} {r[0][1]} {r[0][2]}')
    return ags

def pick_ligand(ag, name):
    ags = split_by_res(ag)
    for ag in ags:
        if ag.getTitle().split()[0] == name:
            return ag
    return None

def get_contact_chains(p_ag, l_ag, thres=5.0):
    dmat = math.get_distance_matrix(p_ag, l_ag)

    idxs = set()
    for i, j in zip(*np.where(dmat < thres)):
        idxs.add(i)

    if len(idxs) == 0:
        return None

    contact_atoms = p_ag[sorted(idxs)].toAtomGroup()

    chids = set()
    for atom in contact_atoms:
        chid = atom.getChid()
        chids.add(chid)

    query = ' or '.join([f'chain {ch}' for ch in sorted(chids)])
    chains = p_ag.select(query).toAtomGroup()

    return chains
