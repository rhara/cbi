import openbabel as ob
import math
import numpy as np

def __vec_rmsd(a, b):
    v = a - b
    return math.sqrt(np.sum(v*v)/a.shape[0])
    
def get_coords(mol):
    coords = []
    for i in range(mol.NumAtoms()):
        atom = mol.GetAtomById(i)
        if not atom.IsHydrogen():
            coords.append([atom.GetX(), atom.GetY(), atom.GetZ()])
    return np.array(coords)

def get_rmsd(refmol, fitmol):
    mappings = ob.vvpairUIntUInt()
    bitvec = ob.OBBitVec()
    lookup = []
    for i in range(refmol.NumAtoms()):
        atom = refmol.GetAtomById(i)
        if not atom.IsHydrogen():
            bitvec.SetBitOn(i+1)
            lookup.append(i)
    success = ob.FindAutomorphisms(refmol, mappings, bitvec)

    refcoords = get_coords(refmol)
    fitcoords = get_coords(fitmol)
    minrmsd = 1e10
    for mapping in mappings:
        automorph_coords = [None]*len(refcoords)
        for x, y in mapping:
            automorph_coords[lookup.index(x)] = refcoords[lookup.index(y)]
        mapping_rmsd = __vec_rmsd(fitcoords, automorph_coords)
        if mapping_rmsd < minrmsd:
            minrmsd = mapping_rmsd
    minrmsd = round(minrmsd, 3)
    return minrmsd
