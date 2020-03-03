import openbabel
import prody
import io

class AtomGroupConv(openbabel.OBConversion):
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
