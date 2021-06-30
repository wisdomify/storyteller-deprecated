import os
import pandas as pd

from collect.main import paths

base_dir = paths.DATA_DIR+'/examples/tmp'
files = os.listdir(base_dir)

base_df = pd.DataFrame()

for file in files:
    cur_df = pd.read_excel(base_dir + '/' + file).fillna('')
    cur_df['eg'] = cur_df['앞문맥'] + cur_df['검색어'] + cur_df['뒷문맥']
    cur_df.drop(['출전', '앞문맥', '검색어', '뒷문맥', '번호'], axis=1, inplace=True)

    base_df = base_df.append(cur_df)


egs_df = base_df \
    .drop('Unnamed: 0', axis=1)\
    .sort_values(by='proverb')
egs_df.set_index('proverb', inplace=True)

egs_df.to_csv(paths.DATA_DIR+'/examples/egs.csv', sep='\t')



