from storyteller.collect.parsers.definitions.namuwikiParser import get_namuwiki_definitions
from storyteller.collect.parsers.definitions.opendictParser import get_opendict_definitions
from storyteller.collect.parsers.definitions.wikiquoteParser import get_wikiquote_definitions


def main():
    get_namuwiki_definitions()
    get_opendict_definitions()
    get_wikiquote_definitions()


if __name__ == '__main__':
    main()
