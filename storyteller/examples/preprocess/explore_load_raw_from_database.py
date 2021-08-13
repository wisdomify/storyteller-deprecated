import os

from storyteller.paths import DATA_DIR
from storyteller.preprocess.load_raw_from_database import get_definitions, get_examples, save_data


def main():
    print(get_definitions(['wikiquote']))
    print(get_examples(definition_origins=['wikiquote'], example_origins=['KoreaUnivCorpus']))
    save_data(of='example', to=os.path.join(DATA_DIR, 'version_1', 'from_db', 'wisdom2eg.tsv'),
              definition_from=['wikiquote'], example_from=['KoreaUnivCorpus'])
    save_data(of='definition', to=os.path.join(DATA_DIR, 'version_1', 'from_db', 'wisdom2def.tsv'),
              definition_from=['wikiquote'], example_from=['KoreaUnivCorpus'])


if __name__ == '__main__':
    main()
