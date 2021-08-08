import pandas as pd
from unittest import TestCase

from storyteller.collect.parsers.examples.koreaUniversityCrawl import KoreaUniversityCorpusSearcher


class TestKoreaUniversityCorpusSearcher(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.koreaUniversityCorpusSearcher = KoreaUniversityCorpusSearcher()
        cls.test_morph_word = '궁/NNG&통하/VV'
        cls.test_word = '궁하면 통한다'
        cls.test_id = 234221

    def test_get_full_text(self):
        text_df = self.koreaUniversityCorpusSearcher.get_full_text(self.test_id)
        self.assertEqual(str, type(text_df))  # 해당 함수 리턴 값은 문자열.
        self.assertLessEqual(1, len(text_df))  # 해당 데이터 프레임에 문장을 반드시 하나 포함해야한다.

    def test_get_morph_analysis(self):
        morph_df = self.koreaUniversityCorpusSearcher.get_morph_analysis(self.test_id)
        self.assertEqual(str, type(morph_df))  # 해당 함수 리턴 값은 문자열.
        self.assertLessEqual(1, len(morph_df))  # 해당 데이터 프레임에 문장을 반드시 하나 포함해야한다.

    def test_get_close_contexts(self):
        cont_df = self.koreaUniversityCorpusSearcher.get_close_contexts(self.test_id)
        self.assertEqual(str, type(cont_df))  # 해당 함수 리턴 값은 문자열.
        self.assertLessEqual(1, len(cont_df))  # 해당 데이터 프레임에 문장을 반드시 하나 포함해야한다.

    def test_get_total_eg_length(self):
        eg_counts = self.koreaUniversityCorpusSearcher.get_total_eg_length(self.test_morph_word)
        self.assertEqual(int, type(eg_counts))  # 해당 함수 리턴 값은 정수.
        self.assertEqual(221, eg_counts)  # 해당 단어의 전체 용례 개수는 221개로 현재 확인됨.

    def test_get_examples_of(self):
        egs_df = self.koreaUniversityCorpusSearcher.get_examples_of(self.test_word, is_manual=False)
        self.assertEqual(pd.DataFrame, type(egs_df))  # 해당 함수 리턴 값은 데이터 프레임.
        self.assertEqual(220, len(egs_df))  # 해당 단어의 전체 용례 개수는 220개여야함.
        # 고려대 시스템에서는 221개여야한다고 하지만 실제 출력되는 용례는 220개.
        # 아마도 빈 공간으로 출력되는 문장이 하나 있다.
        # 이유는 해당 문장과 관련없는 경우 인거 같다.

