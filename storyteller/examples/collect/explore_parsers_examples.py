from storyteller.collect.parsers.examples.daumDictCrawl import get_daumdict_examples_from
from storyteller.collect.parsers.examples.koreaUniversityCrawl import get_korea_university_corpus_result
from storyteller.collect.parsers.examples.naverDictCrawl import get_naverdict_examples_from


def main():
    target_dictionary = 'egs'

    get_daumdict_examples_from(target_dictionary)
    get_naverdict_examples_from(target_dictionary)
    get_korea_university_corpus_result(target_dictionary)


if __name__ == '__main__':
    main()
