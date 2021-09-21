import string
from collections import Counter

import pandas as pd
import re

from datasets import load_dataset
from pprint import pprint as pp

from sklearn.utils import resample


def parse_proverb(raw_data):
    data_df = pd.DataFrame(raw_data)

    # 예시가 비어있는 경우 필터링.
    data_df = data_df.loc[data_df['eg'].str.len() > 0]

    # 속담이 직접적으로 언급된 문장만 필터링
    # 5324 -> 556개로 축소됨.
    data_df = data_df[data_df.apply(lambda r: r['wisdom'] in r['eg'], axis=1)].copy()

    # Remove Emails
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub('\S*@\S*\s?', '', r))

    # Remove new line characters
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub('\s+', ' ', r))

    # Remove distracting single quotes
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub("\'", "", r))

    # 특수 따옴표 제거
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub("“", "", r))
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub("”", "", r))

    # back slash remove
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub('\\\\', "", r))

    # forward slash remove
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub('/', " ", r))

    # Punctuation remove
    data_df['eg'] = data_df.loc[:, 'eg'].apply(
        lambda r: r.translate(str.maketrans('', '', string.punctuation))
    )

    # special symbol filter
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub('◆', " ", r))
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub('·', " ", r))

    # blank space remove at the end of string
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: str(r).strip())

    # space more than twice to once
    data_df['eg'] = data_df.loc[:, 'eg'].apply(lambda r: re.sub(' +', ' ', r))

    # wisdom fit into vocab.py form
    data_df['wisdom'] = data_df.loc[:, 'wisdom'].apply(lambda r: str(r).strip())
    data_df['wisdom'] = data_df.loc[:, 'wisdom'].apply(lambda r: "꿩 대신 닭" if r == '꿩 대신 닭이다' else r)

    data_df['eg'] = data_df.loc[:, ['wisdom', 'eg']].apply(lambda r: re.sub(r[0], '[WISDOM]', r[1]), axis=1)

    data_df = data_df.drop('example_morph', axis=1)

    return data_df.to_dict(orient='records')


if __name__ == '__main__':
    story = load_dataset(path="wisdomify/story",
                         name='example',
                         script_version=f"version_1")
    train = parse_proverb(story['train'])
    val = parse_proverb(story['validation'])
    test = parse_proverb(story['test'])

    total = pd.DataFrame(train + val + test)

    counts = sorted(Counter(total['wisdom']).items(), key=lambda r: r[1], reverse=True)
    major = counts[0]

    # Upsample minority class
    total_df = total.loc[total['wisdom'] == major[0]]
    for wis, ct in counts[1:]:
        df_minority_upsampled = resample(total[total['wisdom'] == wis],
                                         replace=True,  # sample with replacement
                                         n_samples=major[1],  # to match majority class
                                         random_state=0)  # reproducible results

        total_df = total_df.append(df_minority_upsampled)

    total_df.info(verbose=True, null_counts=True, max_cols=True)

    total_df.to_csv('../../../data/version_6/raw/wisdom2eg.tsv', sep='\t', index=False)
