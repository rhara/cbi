import prody

def read_pdb_protein(iname, removeHs=True):
    protein = prody.parsePDB(iname)
    if removeHs:
        protein = protein.select('protein and not hydrogen').toAtomGroup()
    return protein
