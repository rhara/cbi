import openbabel
import prody
import io

class PDBConv(openbabel.OBConversion):
    """
    Convert prody.AtomGroup to molecule block text of any format

    eg)
    ligand = read_ligand_pdb(some_pdb_file)
    conv = PDBConv(to='sdf')
    text = conv(ligand)
    print(text)
    """
    def __init__(self, to):
        openbabel.OBConversion.__init__(self)
        self.SetInAndOutFormats('pdb', to)

    def read(self, ag):
        sio = io.StringIO()
        prody.writePDBStream(sio, ag)
        cont = sio.getvalue().rstrip()
        sio.close()
        mol = openbabel.OBMol()
        self.ReadString(mol, cont)
        return mol

    def __call__(self, ag, strip=False):
        mol = self.read(ag)
        ocont = self.WriteString(mol)
        if strip:
            ocont = ocont.rstrip()
        return ocont

class PDBReader(openbabel.OBConversion):
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

class SDFReader(openbabel.OBConversion):
    """
    Read multimolecule SDF file to array of openbabel.OBMol()

    eg)
    reader = SDFReader()
    obmols = reader(your_sdf_multimol_file)
    """
    def __init__(self):
        openbabel.OBConversion.__init__(self)
        self.SetInAndOutFormats('sdf', 'smi')

    def __call__(self, iname):
        mols = []
        mol = openbabel.OBMol()
        ret = self.ReadFile(mol, iname)
        mols.append(mol)
        while ret:
            mol = openbabel.OBMol()
            ret = self.Read(mol)
            if ret:
                mols.append(mol)
        return mols

    def check_smiles(self, mol):
        return self.WriteString(mol).rstrip()

def read_pdb_ligand(iname, removeHs=True):
    ligand = prody.parsePDB(iname)
    if removeHs:
        ligand = ligand.select('not hydrogen').toAtomGroup()
    return ligand

def read_sdf_mols(iname, verbose=False):
    reader = SDFReader()
    mols = reader(iname)
    if verbose:
        for mol in mols:
            print(reader.check_smiles(mol))
    return mols

