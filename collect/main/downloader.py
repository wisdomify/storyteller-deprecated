import argparse
import os

from collect.main import paths
from collect.main.parsers.definitions.namuwikiParser import get_namuwiki_definitions
from collect.main.parsers.definitions.opendictParser import get_opendict_definitions
from collect.main.parsers.definitions.wikiquoteParser import get_wikiquote_definitions
from collect.main.parsers.examples.daumDictCrawl import get_daumdict_examples_from
from collect.main.parsers.examples.naverDictCrawl import get_naverdict_examples_from


def _make_folder(directory: str):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def main():
    definitions = ['wikiquote', 'opendict', 'namuwiki']
    examples = ['naverdict', 'daumdict', 'koreauniveristy', 'corpuskorean', 'kaist']

    parser = argparse.ArgumentParser()
    parser.add_argument("--which", type=str,
                        default="definition")
    parser.add_argument("--where", type=str,
                        default="wikiquote")
    parser.add_argument("--target", type=str,
                        default="wikiquote")
    args = parser.parse_args()

    which = args.which
    where = args.where
    target = args.target

    _make_folder(paths.DATA_DIR)

    if which == 'definition':
        _make_folder(paths.DATA_DIR + '/definitions')

        if where == 'wikiquote':
            get_wikiquote_definitions()

        elif where == 'opendict':
            get_opendict_definitions()

        elif where == 'namuwiki':
            get_namuwiki_definitions()

        else:
            raise ValueError("This definition is unavailable. Choose from: ", definitions)

    elif which == 'example':
        if not os.path.isfile(paths.DATA_DIR + '/definitions/' + target + '.csv'):
            raise FileExistsError("Definition file is not exist. Download definition first")

        _make_folder(paths.DATA_DIR + '/examples')

        if where == 'naverdict':
            get_naverdict_examples_from(target)

        elif where == 'daumdict':
            get_daumdict_examples_from(target)

        elif where == 'koreauniveristy':
            raise NotImplementedError("Korea University's university corpus data crawler is not yet implemented.")
        elif where == 'corpuskorean':
            raise NotImplementedError("Corpus korean data crawler is not yet implemented.")
        elif where == 'kaist':
            raise NotImplementedError("KAIST corpus data crawler is not yet implemented.")
        else:
            raise ValueError("This example is unavailable. Choose from: ", examples)

    elif which == 'all':
        raise NotImplementedError


if __name__ == '__main__':
    main()
