import os, uuid, gzip
import subprocess as sp

class TLEAP:
    def __init__(self):
        self.basedir = os.path.dirname(__file__)
        self.template = open(self.basedir + '/etc/tleaprc.template').read()

    def __call__(self, pdb_iname):
        uid = uuid.uuid4().hex
        tmpdir = f'tmp/{uid}.tmpdir'
        os.makedirs(tmpdir, exist_ok=True, mode=0o755)
        template = self.template.replace('{{tmpdir}}', tmpdir)
        template_fname = f'{tmpdir}/tleaprc'
        open(template_fname, 'wt').write(template)
        openf = gzip.open if pdb_iname.endswith('.pdb.gz') else open
        pdb_oname = f'{tmpdir}/protein.pdb'
        open(pdb_oname, 'wt').write(openf(pdb_iname, 'rt').read())
        os.system(f'tleap -s -f {template_fname} > /dev/null 2>&1')
        iname1 = f'{tmpdir}/protein.mol2'
        iname2 = f'{tmpdir}/protein_H.pdb'
        oname = f'{tmpdir}/protein_H_charged.mol2'
        sp.check_output(f'cbi_fixprotein {iname1} {iname2} {oname}', shell=True, stderr=sp.DEVNULL)
        return tmpdir
