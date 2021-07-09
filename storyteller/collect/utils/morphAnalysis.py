from konlpy.tag import Kkma, Hannanum, Komoran, Mecab, Okt
from konlpy.utils import pprint


class MorphAnalyzer:
    def __init__(self):
        self.kkma = Kkma()
        self.komoran = Komoran()

    def get_morph_of(self, word: str):
        kkma_res = self.kkma.pos(word)
        komoran_res = self.komoran.pos(word)

        # 둘의 분석이 다른 경우, 꼬꼬마의 리턴 값으로 이용 (꼬꼬마가 분석자체는 정확함. 원형복원을 해서 그렇지)
        return kkma_res \
            if len(kkma_res) != len(komoran_res) \
            else map(
                # How to read => res = (kkma_char, kkma_tag), (komoran_char, komoran_tag)
                lambda res:
                # if tag is not 'NNP' (komoran_char, kkma_tag) else (komoran_char, 'NNG')
                (res[1][0], res[0][1]) if res[0][1] != 'NNP'
                else (res[1][0], 'NNG'),
                zip(kkma_res, komoran_res)
            )

    def get_query_format_of(self, word: str):
        target_tags = [     # 어간에 해당되는 태그 (부정확할 수 있음)
            'NNG',  # 일반 명사
            'NNP',  # 고유 명사
            'NNB',  # 의존 명사
            'NR',  # 수사
            'NP',  # 대명사

            'VV',  # 동사
            'VA',  # 형용사
            'VX',  # 보조 용언
            # 'VCP',  # 긍정 지정사
            # 'VCN',  # 부정 지정사

            'MM',  # 관형사

            'MAG',  # 일반 부사
            'MAJ',  # 접속 부사
        ]

        return '&'.join(list(      # join with & to fit into query
            filter(None.__ne__,     # removing None values
                   map(lambda cell:
                       # join analysed word and tag with '/' if the tag is in the target tags
                       '/'.join(cell) if cell[1] in target_tags
                       else None,
                       self.get_morph_of(word)
                       )
                   )
        ))

