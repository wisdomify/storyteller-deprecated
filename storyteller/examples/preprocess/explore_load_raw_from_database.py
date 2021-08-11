from storyteller.preprocess.load_raw_from_database import get_definitions, get_examples


def main():
    print(get_definitions(['wikiquote']))
    print(get_examples(definition_origins=['wikiquote'], example_origins=['KoreaUnivCorpus']))


if __name__ == '__main__':
    main()
