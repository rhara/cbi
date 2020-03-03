import subprocess as sp
import uuid
import os

def smina_dock(protein_fname, ligand_fname, ncpu=None, num_modes=4, seed=0, workdir=None):
    basedir = os.path.dirname(__file__)
    if workdir is None:
        uid = uuid.uuid4().hex
        workdir = f'tmp/{uid}.tmpdir'
    os.makedirs(workdir, exist_ok=True, mode=0o755)
    if ncpu is None:
        ncpu = os.cpu_count()
    oname = f'{workdir}/docked.sdf'
    logname = f'{workdir}/smina.log'
    script = f'{basedir}/etc/center.py'
    boxpars = sp.check_output(f'python {script} {ligand_fname}', shell=True).decode().strip()
    sp.call(f'smina -r {protein_fname} -l {ligand_fname} {boxpars} --cpu {ncpu} --num_modes {num_modes} --seed {seed} -o {oname} --log {logname}', shell=True)
    return workdir

