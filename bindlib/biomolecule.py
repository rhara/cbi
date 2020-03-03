import prody

def read_pdb_protein(iname, only_protein=False, removeHs=True):
    protein = prody.parsePDB(iname)
    if only_protein:
        protein = protein.select('protein').toAtomGroup()
    if removeHs:
        protein = protein.select('not hydrogen').toAtomGroup()
    return protein
