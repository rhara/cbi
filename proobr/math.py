import numpy as np

def get_distance_matrix(ag1, ag2):
    a = ag1.getCoords()
    b = ag2.getCoords()
    x = np.tile(a, (1, b.shape[0])).reshape(a.shape[0], b.shape[0], 3)
    y = np.tile(b, (a.shape[0], 1)).reshape(a.shape[0], b.shape[0], 3)
    d = x - y
    D = np.sqrt(np.sum(d*d, axis=2))
    return D

def get_connectivity(dmat):
    print(dmat < 2.2)
