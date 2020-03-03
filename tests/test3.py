import os, sys
import pandas as pd
import bindlib as bl
import prody

iname = sys.argv[1] #apo
tleap = bl.TLEAP()
tleap(sys.argv[1])
