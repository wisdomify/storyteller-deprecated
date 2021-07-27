import json
import os
import re
from functools import reduce

import pandas as pd
import requests

from bs4 import BeautifulSoup
from collections import Counter
from http import HTTPStatus

from storyteller.collect.utils.proverbUtils import get_proverbs, get_target_proverbs
from storyteller.collect.utils.morphAnalysis import MorphAnalyzer
from storyteller.paths import DATA_DIR


class KoreaUniversityCorpusSearcher:
    def __init__(self):
        self.morph_analyzer = MorphAnalyzer()
        self.sent_id_parser = re.compile(r"showAnalysis\('(\d*)'\)")

        self._corpus_url = 'http://corpus.korea.ac.kr'
        self._base_url = self._corpus_url + '/t21/webconc/'

        self.list_view_url = self._base_url + 'ListView.php'
        self.sentence_view_url = self._base_url + 'SentenceView.php'
        self.morph_analysis_view_url = self._base_url + 'morphAnalysisView.php'
        self.news_view_url = self._base_url + 'NewsView.php'

    @staticmethod
    def _get_list_sentence_request_body(target_word: str):
        return {
            'listSize': 500,
            'page': 1,
            'unit': 'm',
            'keyword': target_word,
            'x': 8,
            'y': 16,
            'year': 'all',
            'Content-Type': 'multipart/form-data'
        }

    @staticmethod
    def _get_morph_news_request_base_body(sent_id: int):
        return {
            'sent_id': sent_id,
            'year': 'all',
            'Content-Type': 'multipart/form-data'
        }

    def _get_base_fake_header(self):
        return {
            'Origin': self._corpus_url,
            'Referer': self._base_url + 'search.php?keyword=&year='
        }

    def _get_news_fake_header(self):
        return {
            'Origin': self._corpus_url,
            'Referer': self.morph_analysis_view_url
        }

    def get_full_text(self, word_id):
        res = requests.post(url=self.news_view_url,
                            headers=self._get_news_fake_header(),
                            data=self._get_morph_news_request_base_body(word_id)) \
            .content \
            .decode('utf-8')

        return pd.read_html(res)[0][0].str.cat(sep=' /n')

    def get_close_contexts(self, prev_id):
        res = requests.post(url=self.morph_analysis_view_url,
                            headers=self._get_base_fake_header(),
                            data=self._get_morph_news_request_base_body(prev_id)) \
            .content \
            .decode('utf-8')
        return pd.read_html(res)[1].iloc[0].to_string().split('    ')[-1]

    def get_examples_of(self, word: str, is_manual: bool) -> [str, pd.DataFrame]:
        def _get_words_counts(word: str, which: str):
            # 문장에서 특수 문자를 거른 뒤에 구문분석 (특수문자랑 붙어있는 경우 해당 글자가 스킵되기도 함.)
            word = re.sub('\s+', ' ', re.sub('[^A-Za-z0-9가-힣\s]', ' ', word))

            if which == 'sentence':
                return Counter(filter(None.__ne__,
                                      map(lambda analysis:
                                          analysis[0],
                                          self.morph_analyzer.get_morph_of(word)
                                          )
                                      ))
            elif which == 'word':
                return Counter(filter(None.__ne__,
                                      map(lambda analysis:
                                          analysis[0] if analysis[1] in self.morph_analyzer.target_tags
                                          else None,
                                          self.morph_analyzer.get_morph_of(word)
                                          )
                                      ))

        def _filter_word_not_mentioned(word: str, eg_sentence: str):
            """
            This function filters whether the proverb is mentioned by counting the 글자 in example sentence
            eg. 산 넘어 산 -> 산(2), 넘(1) -> 예시 문장에서 산이 2번, 넘이 1번 이상 사용된 문장만 필터링 된다.
            """

            sentence_counts = _get_words_counts(eg_sentence, 'sentence')
            target_counts = _get_words_counts(word, 'word')

            return reduce(lambda x, y: x and y,
                          map(lambda kv: True if sentence_counts[kv[0]] >= kv[1] else False,
                              target_counts.items()
                              )
                          )
        if is_manual:
            query_word = word
        else:
            query_word = self.morph_analyzer.get_query_format_of(word=word)

        print(' ->', query_word, end=' ')
        res = requests.post(url=self.sentence_view_url,
                            headers=self._get_base_fake_header(),
                            data=self._get_list_sentence_request_body(target_word=query_word))

        if res.status_code != HTTPStatus.OK:
            print('NO EXAMPLE', end=' ')
            return ''

        res = res.content \
            .decode('utf-8')

        df = pd.read_html(res)
        if len(df) > 0:
            example_df = df[0].rename(columns={0: 'eg'})
        else:
            print('Example load failed')
            print(df)
            return ''

        soup = BeautifulSoup(res, 'lxml')

        sent_ids = list(filter(
            None.__ne__,
            map(lambda row:
                int(self.sent_id_parser.search(row.attrs['onclick']).group(1)) if 'onclick' in row.attrs
                else None,
                soup.body.find_all('tr'))
        ))

        example_df['eg_id'] = sent_ids
        example_df['wisdom'] = word

        example_df['legit'] = example_df[['wisdom', 'eg']] \
            .apply(lambda x: _filter_word_not_mentioned(x.wisdom, x.eg), axis=1)


        example_df = example_df[example_df['legit']]

        return example_df[['wisdom', 'eg_id', 'eg']]

    def get_total_data_of(self, word: str, is_manual: bool) -> [str, pd.DataFrame]:
        df = self.get_examples_of(word, is_manual)
        if len(df) > 0:
            print('(egs: {count})\n\t-> base eg loaded'.format(count=len(df)), end=' ')

            df['prev'] = df[['eg_id']] \
                .apply(lambda x: self.get_close_contexts(x - 1), axis=1)
            print('-> prev loaded', end=' ')

            df['next'] = df[['eg_id']] \
                .apply(lambda x: self.get_close_contexts(x + 1), axis=1)
            print('-> next loaded', end=' ')

            df['full'] = df[['eg_id']] \
                .apply(lambda x: self.get_full_text(x), axis=1)
            print('-> full text loaded', end=' ')

            df = df[['wisdom', 'eg_id', 'prev', 'eg', 'next', 'full']]

            return df
        return ''


def get_korea_university_corpus_result(target_dictionary: str):
    def _get_downloaded_list(destination_existence: bool, location: str):
        if not destination_existence:
            return []
        return set(pd.read_csv(location)['wisdom'])

    corpusSearcher = KoreaUniversityCorpusSearcher()

    save_location = DATA_DIR + '/examples/{}_koreaUniv.csv'.format(target_dictionary)
    is_save_destination_exist = os.path.isfile(save_location)

    raw_wisdoms = get_proverbs(target_csv=target_dictionary + '.csv')
    downloaded = _get_downloaded_list(destination_existence=is_save_destination_exist,
                                      location=save_location)

    wisdoms = get_target_proverbs(downloaded=downloaded, proverbs=raw_wisdoms)

    for idx, wisdom in enumerate(wisdoms):
        if idx != 0:
            is_save_destination_exist = os.path.isfile(save_location)
        print('current({}/{}):'.format(idx + 1, len(wisdoms)), wisdom, end=' ')
        examples_df = corpusSearcher.get_total_data_of(wisdom, is_manual=False)
        if len(examples_df) > 0:
            if is_save_destination_exist:
                examples_df.to_csv(save_location, mode='a', header=False)
            else:
                examples_df.to_csv(save_location)

        print()


def manual_download(target_dictionary: str, word: str):
    corpusSearcher = KoreaUniversityCorpusSearcher()

    save_location = DATA_DIR + '/examples/{}_koreaUniv.csv'.format(target_dictionary)
    is_save_destination_exist = os.path.isfile(save_location)

    examples_df = corpusSearcher.get_total_data_of(word, is_manual=True)

    if is_save_destination_exist:
        examples_df.to_csv(save_location, mode='a', header=False)
    else:
        examples_df.to_csv(save_location)


if __name__ == '__main__':
    # get_korea_university_corpus_result('egs')
    manual_download('egs', '산/NNG&넘/VV&어/EM&산/NNG')