import json
import re

import pandas as pd
import requests
from urllib.parse import quote

from bs4 import BeautifulSoup

from collect.main.parsers.utils.morphAnalysis import MorphAnalyzer


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
            'listSize': 50,
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

    def get_examples_of(self, word: str) -> pd.DataFrame:
        query_word = self.morph_analyzer.get_query_format_of(word=word)
        res = requests.post(url=self.sentence_view_url,
                            headers=self._get_base_fake_header(),
                            data=self._get_list_sentence_request_body(target_word=query_word)) \
            .content \
            .decode('utf-8')

        example_df = pd.read_html(res)[0].rename(columns={0: 'eg'})

        soup = BeautifulSoup(res, 'lxml')

        sent_ids = list(filter(
            None.__ne__,
            map(lambda row:
                int(self.sent_id_parser.search(row.attrs['onclick']).group(1)) if 'onclick' in row.attrs
                else None,
                soup.body.find_all('tr'))
        ))

        example_df['eg_id'] = sent_ids

        return example_df[['eg_id', 'eg']]

    def get_total_data_of(self, word: str) -> pd.DataFrame:
        df = self.get_examples_of(word)

        df['prev'] = df[['eg_id']] \
            .apply(lambda x: self.get_close_contexts(x - 1), axis=1)

        df['next'] = df[['eg_id']] \
            .apply(lambda x: self.get_close_contexts(x + 1), axis=1)

        df['full'] = df[['eg_id']] \
            .apply(lambda x: self.get_full_text(x), axis=1)

        df = df[['eg_id', 'prev', 'eg', 'next', 'full']]

        df.to_csv('./tmp.csv')

        return df


if __name__ == '__main__':
    corpusSearcher = KoreaUniversityCorpusSearcher()
    corpusSearcher.get_total_data_of('가는 날이 장날')
