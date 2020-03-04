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
    idxs = sorted(set(np.where(dmat < thres)[0]))
    chids = set([p_ag[i].getChid() for i in idxs])
    idxs = [i for i in range(p_ag.numAtoms()) if p_ag[i].getChid() in chids]
    chains = p_ag[idxs].toAtomGroup()
    return chains

def get_pocket_residues(p_ag, l_ag, thres=5.0):
    dmat = math.get_distance_matrix(p_ag, l_ag)
    idxs = sorted(set(np.where(dmat < thres)[0]))
    ress = set()
    for i in idxs:
        atom = p_ag[i]
        resname = atom.getResname()
        resnum = atom.getResnum()
        chid = atom.getChid()
        ress.add((resname, resnum, chid))
    idxs = []
    for i in range(p_ag.numAtoms()):
        atom = p_ag[i]
        resname = atom.getResname()
        resnum = atom.getResnum()
        chid = atom.getChid()
        if (resname, resnum, chid) in ress:
            idxs.append(i)
    residues = p_ag[idxs].toAtomGroup()
    return residues

