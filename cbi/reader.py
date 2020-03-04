import openbabel
import prody
import sys

class OBMolPDBReader(openbabel.OBConversion):
    """
    Read single molecule PDB file to openbabel.OBMol()

    eg)
    reader = PDBReader()
    obmol = reader(your_pdb_file)
    """
    def __init__(self):
        openbabel.OBConversion.__init__(self)
        self.SetInAndOutFormats('pdb', 'smi')

    def __call__(self, iname):
        mol = openbabel.OBMol()
        self.ReadFile(mol, iname)
        return mol

class OBMolSDFReader(openbabel.OBConversion):
    """
    Read multimolecule SDF file to array of openbabel.OBMol()

    eg)
    reader = SDFReader()
    obmols = reader(your_sdf_multimol_file)
    """
    def __init__(self, verbose=False):
        self.verbose = verbose
        openbabel.OBConversion.__init__(self)
        self.SetInAndOutFormats('sdf', 'smi')

    def __call__(self, iname):
        mols = []
        mol = openbabel.OBMol()
        ret = self.ReadFile(mol, iname)
        if ret:
            if self.verbose:
                print(self.to_smiles(mol), file=sys.stderr)
        else:
            return []
        mols.append(mol)
        while ret:
            mol = openbabel.OBMol()
            ret = self.Read(mol)
            if ret:
                if self.verbose:
                    print(self.to_smiles(mol))
                mols.append(mol)
        return mols

    def to_smiles(self, mol):
        return self.WriteString(mol).replace('\t', ' ').rstrip()

class AtomGroupPDBReader:
    def __init__(self, select=None):
        self.select = select

    def __call__(self, iname):
        try:
            ag = prody.parsePDB(iname)
            if self.select:
                ag = ag.select(self.select).toAtomGroup()
            return ag
        except:
            return None
