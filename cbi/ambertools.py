import os, gzip
import subprocess as sp

class TLEAP:
    def __init__(self):
        self.basedir = os.path.dirname(__file__)
        self.template = open(self.basedir + '/etc/tleaprc.template').read()

    def __call__(self, pdb_iname):
        workdir = os.path.dirname(os.path.abspath(pdb_iname))
        pdbid = os.path.basename(pdb_iname)[:4]
        template = self.template.replace('{{workdir}}', workdir).replace('{{pdbid}}', pdbid)
        template_fname = f'{workdir}/{pdbid}.tleaprc'
        open(template_fname, 'wt').write(template)
        openf = gzip.open if pdb_iname.endswith('.pdb.gz') else open
        pdb_oname = f'{workdir}/{pdbid}_tmp_protein.pdb'
        open(pdb_oname, 'wt').write(openf(pdb_iname, 'rt').read())
        os.system(f'tleap -s -f {template_fname} > /dev/null 2>&1')
        iname1 = f'{workdir}/{pdbid}_tmp_protein_H.pdb'
        iname2 = f'{workdir}/{pdbid}_tmp_protein.mol2'
        oname = f'{workdir}/{pdbid}_protein_H_charged.mol2'
        sp.check_output(f'cbi_fixprotein {iname1} {iname2} {oname}', shell=True, stderr=sp.DEVNULL)
        return workdir
