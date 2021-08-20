import os

import pandas as pd

from storyteller.collect.utils.proverbUtils import get_proverbs, get_target_proverbs, concat_context_example_from, \
    clear_definition_for_hug
from storyteller.paths import DATA_DIR


def main():
    def _get_downloaded_list(destination_existence: bool, location: str):
        if not destination_existence:
            return []
        return set(pd.read_csv(location)['wisdom'])

    save_location = DATA_DIR + '/examples/{}_koreaUniv.csv'.format('wikiquote')
    is_save_destination_exist = os.path.isfile(save_location)

    raw_wisdoms = get_proverbs(target_csv='wikiquote' + '.csv')
    downloaded = _get_downloaded_list(destination_existence=is_save_destination_exist,
                                      location=save_location)

    wisdoms = get_target_proverbs(downloaded=downloaded, proverbs=raw_wisdoms)
    print(wisdoms)


def explore_concat():
    # concat_context_example_from(directory=DATA_DIR + '/version_2/raw/wisdom2eg.tsv')
    # concat_context_example_from(directory=DATA_DIR + '/version_3/raw/wisdom2eg.tsv')
    # concat_context_example_from(directory=DATA_DIR + '/version_4/raw/wisdom2eg.tsv')

    clear_definition_for_hug(directory=DATA_DIR + '/version_2/raw/wisdom2def.tsv')
    clear_definition_for_hug(directory=DATA_DIR + '/version_3/raw/wisdom2def.tsv')
    clear_definition_for_hug(directory=DATA_DIR + '/version_4/raw/wisdom2def.tsv')


if __name__ == '__main__':
    explore_concat()
