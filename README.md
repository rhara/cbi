# CBI prep

NOTE: This is going to be chained.

```
pip install .

$ cbi_dock example_data/1mwt.apo.pdb.gz example_dat/1mwt_PNM.sdf
tmp/669acb2ca0cf49ceaa662233d7b3f901.tmpdir/docked.sdf
$ cbi_rmsd example_dat/1mwt_PNM.sdf tmp/669acb2ca0cf49ceaa662233d7b3f901.tmpdir/docked.sdf
```
