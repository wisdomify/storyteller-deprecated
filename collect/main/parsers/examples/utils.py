from collect.main.paths import DATA_DIR

import pandas as pd


def get_proverbs(target_csv: str):
    return sorted(set(pd.read_csv(DATA_DIR+'/definitions/'+target_csv)['wisdom']))


def get_target_proverbs(downloaded: list, proverbs: list):
    return list(filter(
        None.__ne__,
        map(
            lambda word: word if word not in downloaded else None,
            proverbs
        )
    ))
