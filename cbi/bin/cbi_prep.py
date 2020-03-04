#!/usr/bin/env python

import cbi
import sys, os, argparse
import prody

to_sdf = cbi.AtomGroupConv(to='sdf')
to_smi = cbi.AtomGroupConv(to='smi')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pdb_iname', type=str)
    parser.add_argument('ligand_name', type=str)
    parser.add_argument('--pocket-thres', '-p', type=float, default=5.0)
    parser.add_argument('--quiet', '-q', action='store_true')
    args = parser.parse_args()

    pdb_iname = args.pdb_iname
    ligand_name = args.ligand_name
    pocket_thres = args.pocket_thres
    quiet = args.quiet

    basedir = os.path.abspath(os.path.dirname(pdb_iname))
    pdbid = os.path.basename(pdb_iname)[:4]

    protein = cbi.AtomGroupPDBReader('not hydrogen and not water')(pdb_iname)

    apo = protein.select('protein').toAtomGroup()

    hetero = protein.select('hetero').toAtomGroup()
    if hetero is None:
        print(pdbid, f'Error: no HETATM entry', file=sys.stderr)
        sys.exit(-1)

    ligands = cbi.split_by_res(hetero)
    ligand = cbi.pick_ligand(hetero, ligand_name)
    if ligand is None:
        print(pdbid, f'Error: {ligand_name} not found', file=sys.stderr)
        sys.exit(-1)

    print(pdbid, to_smi(ligand), ligand_name)

    chains = cbi.get_contact_chains(apo, ligand)
    if chains is None:
        print(pdbid, f'Error: no contact chains with {ligand_name}')
        sys.exit(-1)

    chains_oname = f'{basedir}/{pdbid}.apo.pdb.gz'
    if not quiet:
        print(f'write to {chains_oname}')
    prody.writePDB(chains_oname, chains)

    pocket = cbi.get_pocket_residues(chains, ligand)

    pocket_oname = f'{basedir}/{pdbid}.pocket_{pocket_thres}.pdb'
    if not quiet:
        print(f'write to {pocket_oname}')
    prody.writePDB(pocket_oname, pocket)

    ligand_block = to_sdf(ligand)
    ligand_oname = f'{basedir}/{pdbid}_{ligand_name}.sdf'
    if not quiet:
        print(f'write to {ligand_oname}')
    open(ligand_oname, 'wt').write(ligand_block)
    ligand_oname = f'{basedir}/{pdbid}_{ligand_name}.pdb'
    if not quiet:
        print(f'write to {ligand_oname}')
    prody.writePDB(ligand_oname, ligand)

if __name__ == "__main__":
    main()
