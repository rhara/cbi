import subprocess as sp

def get_rmsd_from_files(ref_pdb, fit_sdf):
    output = sp.check_output(f'obrms -firstonly {ref_pdb} {fit_sdf}', shell=True, universal_newlines=True).rstrip()
    rmsds = []
    try:
        for line in output.split('\n'):
            it = line.split()
            rmsd = round(float(it[1]), 3)
            rmsds.append(rmsd)
    except IndexError:
        return []
    return rmsds

"""
# This code does not work as expected

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
    rmsd = 1e10
    for mapping in mappings:
        automorph_coords = [None]*refcoords.shape[0]
        for x, y in mapping:
            automorph_coords[lookup.index(x)] = refcoords[lookup.index(y)]
        rmsd_of_mapping = __vec_rmsd(fitcoords, np.array(automorph_coords))
        if rmsd_of_mapping < rmsd:
            rmsd = rmsd_of_mapping
    rmsd = round(rmsd, 3)
    return rmsd
"""
