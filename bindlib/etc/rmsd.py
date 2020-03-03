import bindlib as bl
import sys

if __name__ == "__main__":
    iname1 = sys.argv[1]
    iname2 = sys.argv[2]
    refmol = bl.OBMolPDBReader()(iname1)
    fitmols = bl.OBMolSDFReader()(iname2)

    count = 0
    for fitmol in fitmols:
        count += 1
        rmsd = bl.get_rmsd(refmol, fitmol)
        print(count, rmsd)
