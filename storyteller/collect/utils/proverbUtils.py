import pandas as pd

from storyteller.paths import DATA_DIR


def get_proverbs(target_csv: str):
    return sorted(set(pd.read_csv(DATA_DIR + '/legacy/definitions/' + target_csv)['wisdom']))


def get_target_proverbs(downloaded: list, proverbs: list):
    return list(filter(
        None.__ne__,
        map(
            lambda word: word if word not in downloaded else None,
            proverbs
        )
    ))


def concat_context_example_from(directory: str) -> None:
    total_df = pd.read_csv(directory, sep='\t')

    total_df['eg'] = total_df['prev'] + ' ' + total_df['example'] + ' ' + total_df['next']

    total_df = total_df[['wisdom', 'eg']]
    total_df.to_csv(directory, sep='\t', index=False)


def clear_definition_for_hug(directory: str):
    total_df = pd.read_csv(directory, sep='\t')[['wisdom', 'definition']]\
        .rename(columns={'definition': 'def'})

    total_df = total_df[['wisdom', 'def']]
    total_df.to_csv(directory, sep='\t', index=False)
