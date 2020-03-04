#!/usr/bin/env python

import prody
import os
import pandas as pd

os.makedirs('data', mode=0x755, exist_ok=True)

df = pd.read_csv('example_data/data.csv')

for i in df.index:
    r = df.loc[i]
    if 'select' not in r['label'] or '2019' not in r['label']:
        print(r['label'])
