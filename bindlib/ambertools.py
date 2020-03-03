import os, uuid, gzip

class TLEAP:
    def __init__(self):
        bdir = os.path.dirname(__file__)
        self.template = open(bdir + '/etc/tleaprc.template').read()

    def __call__(self, pdb_iname):
        uid = uuid.uuid4().hex
        print(uid)
        tmpdir = f'tmp/{uid}.tmpdir'
        os.makedirs(tmpdir, exist_ok=True, mode=0o755)
        template = self.template.replace('{{tmpdir}}', tmpdir)
        template_fname = f'{tmpdir}/tleaprc'
        open(template_fname, 'wt').write(template)
        openf = gzip.open if pdb_iname.endswith('.pdb.gz') else open
        pdb_oname = f'{tmpdir}/protein.pdb'
        open(pdb_oname, 'wt').write(openf(pdb_iname, 'rt').read())
        os.system(f'tleap -s -f {template_fname}')
