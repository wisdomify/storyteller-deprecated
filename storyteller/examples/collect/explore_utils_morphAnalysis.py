from storyteller.collect.utils.morphAnalysis import MorphAnalyzer


def main():
    proverbs = ['가는 날이 장날이다',
                '가는 날이 장날',
                '갈수록 태산',
                '꿩 대신 닭',
                '등잔 밑이 어둡다',
                '산 넘어 산',
                '소문난 잔치에 먹을 것 없다',
                '원숭이도 나무에서 떨어진다',
                '핑계 없는 무덤 없다',
                ]

    analyser = MorphAnalyzer()

    for proverb in proverbs:
        print(list(analyser.get_morph_of(proverb)))
        print(analyser.get_query_format_of(proverb))


if __name__ == '__main__':
    main()
