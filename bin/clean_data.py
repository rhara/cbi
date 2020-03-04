import os, glob, re, argparse
import subprocess as sp

parser = argparse.ArgumentParser()
parser.add_argument('datadir', type=str)
parser.add_argument('--level', '-l', type=str, default='dock', choices=['dock', 'all'])
args = parser.parse_args()

datadir = args.datadir
level = args.level

if level == 'all':
    pat = re.compile('^(.*)\.pdb\.gz$')

    for f in glob.glob(f'{datadir}/*/*'):
        if os.path.isdir(f):
            continue

        leave = False

        m = pat.search(f)
        if m:
            if m.group(1).endswith('.apo'):
                leave = False
            else:
                leave = True

        if not leave:
            print(f'remove {f}')
            sp.call(f'rm {f}', shell=True)

elif level == 'dock':
    for f in glob.glob(f'{datadir}/*/*'):
        if os.path.isdir(f):
            continue
        bname = os.path.basename(f)
        leave = False
        if f.endswith('.pdb.gz'):
            leave = True
        elif '.pocket_' in f and f.endswith('.pdb'):
            leave = True
        elif bname[4] == '_' and len(bname) == 12 and (bname.endswith('.pdb') or bname.endswith('.sdf')):
            leave = True

        if not leave:
            print(f'remove {f}')
            sp.call(f'rm {f}', shell=True)
