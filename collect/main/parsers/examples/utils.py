from collect.main.paths import DATA_DIR

import pandas as pd


def get_proverbs(target_csv: str):
    return sorted(set(pd.read_csv(DATA_DIR+'/definitions/'+target_csv)['wisdom']))
