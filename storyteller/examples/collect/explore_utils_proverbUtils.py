import os

import pandas as pd

from storyteller.collect.utils.proverbUtils import get_proverbs, get_target_proverbs
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


if __name__ == '__main__':
    main()
