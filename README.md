# CBI prep

NOTE: This is going to be chained.

## Requirements

```
conda install -c bioconda autodock-vina smina
conda install -c insilichem prody
conda install -c ambermd ambertools
conda install -c openbabel openbabel
```

No `rdkit` required.


```
pip install .
```

## Per data

```
$ cbi_prep example_data/1mwt.pdb.gz PNM
$ cbi_dock example_data/1mwt.apo.pdb.gz example_data/1mwt_PNM.sdf
$ cbi_rmsd example_data/1mwt_PNM.pdb example_data/1mwt_PNM.docked.sdf

```

## Data-driven

```
$ bin/fetch_data example_data/data.csv data
$ bin/prep_data example_data/data.csv data
$ bin/prep_dock example_data/data.csv data
```