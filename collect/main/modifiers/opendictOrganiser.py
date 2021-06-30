import pandas as pd
import os

from collect.main import paths

base_dir = paths.DATA_DIR+'/opendict'

files = os.listdir(base_dir)

base_df = pd.DataFrame()

for file in files:
    cur_df = pd.read_csv(base_dir+file).drop('Unnamed: 0', axis=1)
    base_df = base_df.append(cur_df)

base_df.to_csv(paths.DATA_DIR+'/definitions/opendict.csv', index=False)

