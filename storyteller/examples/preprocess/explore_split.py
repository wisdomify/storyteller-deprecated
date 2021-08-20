import os

from storyteller.paths import DATA_DIR
from storyteller.preprocess.split import split_and_save, make_zip_files


def explore():
    # ver = 4
    for ver in range(2, 5):
        ver_dir = os.path.join(DATA_DIR, f'version_{ver}/')

        split_and_save(os.path.join(ver_dir, 'raw/wisdom2def.tsv'), 80, 10, 10)
        make_zip_files(ver_dir, 'definition')
        print()

        split_and_save(os.path.join(ver_dir, 'raw/wisdom2eg.tsv'), 80, 10, 10)
        make_zip_files(ver_dir, 'example')


if __name__ == '__main__':
    explore()
