from storyteller.paths import FROM_DB_WISDOM2EG_TSV
import pandas as pd
import re
from konlpy.tag import Kkma, Okt, Komoran


komoran = Komoran()
kkma = Kkma()
okt = Okt()
# these... support morphs, pos and nouns.


def main():
    wisdom2eg_df = pd.read_csv(FROM_DB_WISDOM2EG_TSV, sep="\t")
    # I just need the first two columns; wisdom & context
    # https://stackoverflow.com/a/11287278
    wisdom2context_df = wisdom2eg_df[['wisdom', 'context']]
    # drop the null values
    wisdom2context_df = wisdom2context_df.dropna()
    # so, we have 5324 non-null counts.
    print(wisdom2context_df.info())
    # now.. have a look at the data

    # --- 가는 날이 장날 --- #
    first2context_df = wisdom2context_df[wisdom2context_df['wisdom'] == "가는 날이 장날"]
    # "인": 지난 주말 오랜만에 제주도엘 내려갔다.  WISDOM인지 날이 몹시 궂었다. 폭설이 내리고 바람이 세차 온종일 비행기마저 결항되고 말았다.
    # ".": 남부로를 따라 나란히 주택가 골목으로 이어진 풍물시장 자리는 옛 약사천 물길을 복개한 곳이다.  WISDOM. 뒷골목까지 시끌벅적하다.
    # 필요하지 않은 패턴들:
    # "에": 다른 한 쪽에는 이야기를 통한 해설과 각종 정보를 넣는다.  WISDOM에 비슷한 속담으로 술 익자 체 장수 지나간다를 알려주고, It never rains but pours라는 영어 속담을 곁들이는 식이다. 소파에 편하게 누워 책장을 넘기면서도 교양을 쌓을 수 있다는 편안한 인상을 준 점, 논술이 강조되는 시점에 기초 어휘력 향상과 상식 습득에 필요한 속담.명언.고사성어 등의 분야로 접근한 점 등이 독자들에게 먹혀든 것으로 보인다.
    # "은": 트위터를 통해 친구에게 재미있는 책을 소개하는 140자 서평 기능도 눈에 띈다.  WISDOM은 전국 1600여 재래시장의 정보를 담고 있다. 사용자 주변에 있는 재래시장을 안내하고, 친환경 농산물 가격, 주부들이 직접 조사한 소비자 물가, 시장에 관한 뉴스와 블로그 등 생활 정보도 담고 있다.
    # 그 어떤 조사도 없음: 근현대에 접어들어서는 각종 집회와 궐기대회 장소로 사용되기도 했다.  WISDOM 망건 쓰자 파장이라는 시간의 중요함을 알리는 속담의 진원지였다. 전통시장은 왜 살아남지 못하고 사라졌어요?
    first_pattern = re.compile(r'WISDOM[이인\.].*? ')
    for idx, row in first2context_df.iterrows():
        wisdom, context = row[0], row[1]
        if wisdom in context:
            context: str
            context = context.replace(wisdom, "WISDOM")
            context = re.sub(r'([\'\"]|\(.+?\))', "", context)  # get rid of the punctuations
            if first_pattern.search(context):
                context = first_pattern.sub("DELETED ", context)
                print(wisdom, "|", context)

    # ---  갈수록 태산 --- #



if __name__ == '__main__':
    main()
