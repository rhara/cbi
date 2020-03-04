# CBI prep

NOTE: This is going to be chained.

```
pip install .

$ cbi_prep example_data/1mwt.apo.pdb.gz PNM
$ cbi_dock example_data/1mwt.apo.pdb.gz example_data/1mwt_PNM.sdf
$ cbi_rmsd example_data/1mwt_PNM.pdb example_data/1mwt_PNM.docked.sdf

$ cbi_prep example_data/5eol.pdb.gz 5QO
$ cbi_dock example_data/5eol.apo.pdb.gz example_data/5eol_5QO.sdf
$ cbi_rmsd example_data/5eol.pdb example_data/5eol_5QO.docked.sdf
```
