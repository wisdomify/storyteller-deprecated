import os

from storyteller.paths import DATA_DIR
from storyteller.preprocess.load_raw_from_database import get_definitions, get_examples, save_data


def main():
    ver = 4
    def_origin = 'opendict'
    ex_origin = 'KoreaUnivCorpus'

    # print(get_definitions([def_origin]))
    # print(get_examples(definition_origins=[def_origin], example_origins=[ex_origin]))
    save_data(of='example', to=os.path.join(DATA_DIR, f'version_{ver}', 'from_db', 'wisdom2eg.tsv'),
              definition_from=[def_origin], example_from=[ex_origin])
    save_data(of='definition', to=os.path.join(DATA_DIR, f'version_{ver}', 'from_db', 'wisdom2def.tsv'),
              definition_from=[def_origin], example_from=[ex_origin])


if __name__ == '__main__':
    main()
