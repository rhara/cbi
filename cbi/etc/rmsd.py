import cbi
import sys

if __name__ == "__main__":
    iname1 = sys.argv[1]
    iname2 = sys.argv[2]
    refmol = cbi.OBMolPDBReader()(iname1)
    fitmols = cbi.OBMolSDFReader()(iname2)

    count = 0
    for fitmol in fitmols:
        count += 1
        rmsd = cbi.get_rmsd(refmol, fitmol)
        print(count, rmsd)
