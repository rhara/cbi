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
