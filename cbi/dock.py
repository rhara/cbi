import subprocess as sp
import os

def smina_dock(protein_fname, ligand_fname, ncpu=None, num_modes=4, seed=0, quiet=False):
    basedir = os.path.dirname(__file__)
    workdir = os.path.dirname(os.path.abspath(protein_fname))
    pdbid = os.path.basename(protein_fname)[:4]
    if ncpu is None:
        ncpu = os.cpu_count()
    oname = f'{workdir}/{os.path.basename(ligand_fname)[:-4]}.docked.sdf'
    logname = f'{workdir}/{os.path.basename(ligand_fname)[:-4]}.smina.log'
    center_script = f'{basedir}/etc/center.py'
    boxpars = sp.check_output(f'python {center_script} {ligand_fname}', shell=True).decode().strip()
    command = f'smina -r {protein_fname} -l {ligand_fname} '\
              f'{boxpars} --cpu {ncpu} --num_modes {num_modes} --seed {seed} -o {oname} --log {logname}'
    if quiet:
        sp.call(command, shell=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
    else:
        sp.call(command, shell=True)
    return workdir

