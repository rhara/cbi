import numpy as np

def get_distance_matrix(ag1, ag2):
    a = ag1.getCoords()
    b = ag2.getCoords()
    x = np.tile(a, (1, b.shape[0])).reshape(a.shape[0], b.shape[0], 3)
    y = np.tile(b, (a.shape[0], 1)).reshape(a.shape[0], b.shape[0], 3)
    d = x - y
    D = np.sqrt(np.sum(d*d, axis=2))
    return D

def get_connectivity(ag, dmat, thres=2.2):
    conn = []
    for i, j in zip(*np.where(dmat < thres)):
        if i == j:
            continue
        if len(conn) == 0:
            conn.append(set([i, j]))
            continue
        found = False
        for k in range(len(conn)):
            if i in conn[k] or j in conn[k]:
                conn[k].add(i)
                conn[k].add(j)
                found = True
                break
        if not found:
            conn.append(set([i,j]))
    for k in range(len(conn)):
        conn[k] = sorted(conn[k])
    conn.sort()

    atom_groups = []
    for c in conn:
        atom_groups.append(ag[c].toAtomGroup())
    return atom_groups
