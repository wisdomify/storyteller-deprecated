import pandas as pd
import string
import csv
import re
from os import path
from collections import Counter
from sklearn.utils import resample
from storyteller.paths import DATA_DIR

def remove_word_segment_with_proverb(raw_data):
    data_df = pd.DataFrame(raw_data)

    # 예시가 비어있는 경우 필터링.
    data_df = data_df.loc[data_df['context'].str.len() > 0]

    # 속담이 직접적으로 언급된 문장만 필터링
    # 5324 -> 556개로 축소됨.
    data_df = data_df[data_df.apply(lambda r: r['wisdom'] in r['context'], axis=1)].copy()

    # Remove Emails
    data_df['context'] = data_df.loc[:, 'context'].apply(lambda r: re.sub(r'\S*@\S*\s?', '', r))

    # Remove new line characters
    data_df['context'] = data_df.loc[:, 'context'].apply(lambda r: re.sub(r'\s+', ' ', r))

    # Remove distracting single quotes
    data_df['context'] = data_df.loc[:, 'context'].apply(lambda r: re.sub("\'", "", r))

    # 특수 따옴표 제거
    data_df['context'] = data_df.loc[:, 'context'].apply(lambda r: re.sub("“", "", r))
    data_df['context'] = data_df.loc[:, 'context'].apply(lambda r: re.sub("”", "", r))

    # back slash remove
    data_df['context'] = data_df.loc[:, 'context'].apply(lambda r: re.sub('\\\\', "", r))

    # forward slash remove
    data_df['context'] = data_df.loc[:, 'context'].apply(lambda r: re.sub('/', " ", r))

    # Punctuation remove
    data_df['context'] = data_df.loc[:, 'context'].apply(
        lambda r: r.translate(str.maketrans('', '', string.punctuation))
    )

    # blank space remove at the end of string
    data_df['context'] = data_df.loc[:, 'context'].apply(lambda r: str(r).strip())

    # wisdom fit into vocab.py form
    data_df['wisdom'] = data_df.loc[:, 'wisdom'].apply(lambda r: str(r).strip())
    data_df['wisdom'] = data_df.loc[:, 'wisdom'].apply(lambda r: "꿩 대신 닭" if r == '꿩 대신 닭이다' else r)

    first_pattern = re.compile(r'WISDOM[이인\.].*? ')
    for idx, row in data_df.iterrows():
        wisdom, context = row[0], row[1]
        if wisdom in context:
            context: str
            context = context.replace(wisdom, "WISDOM")
            context = re.sub(r'([\'\"]|\(.+?\))', "", context)  # get rid of the punctuations
            if first_pattern.search(context):
                context = first_pattern.sub(" ", context)
                if 'WISDOM' in context:
                    context = context.replace('WISDOM', '')
                    print(context)
                row[1] = context
    counts = sorted(Counter(data_df['wisdom']).items(), key=lambda r: r[1], reverse=True)
    major = counts[0]
    print(counts)
    # Upsample minority class
    total_df = data_df.loc[data_df['wisdom'] == major[0]]
    for wis, ct in counts[1:]:
        df_minority_upsampled = resample(data_df[data_df['wisdom'] == wis],
                                            replace=True,  # sample with replacement
                                            n_samples=major[1],  # to match majority class
                                            random_state=123)  # reproducible results

        total_df = total_df.append(df_minority_upsampled)

    return total_df.to_dict(orient='records')

def get_wisdom_and_eg(wisdom2eg_path):
    with open(wisdom2eg_path, 'r') as fh:
        tsv_reader = csv.reader(fh, delimiter="\t")
        next(tsv_reader)  # skip the header
        return [
            (row[0], row[1])  # wisdom, sent pair
            for row in tsv_reader
            if row[1] is not ''
        ]
def get_parsed_df(wisdom2eg_df):
    wisdom2context_df = wisdom2eg_df[['wisdom', 'context']]
    wisdom2context_df = wisdom2context_df.dropna()
    wisdom2context_parsed_df = remove_word_segment_with_proverb(wisdom2context_df)
    return wisdom2context_parsed_df

def main():
    ver_src_dir = path.join(DATA_DIR, 'version_1')
    ver_dst_dir = path.join(DATA_DIR, 'version_5')

    raw_src_dir = path.join(ver_src_dir, 'raw')
    raw_dst_dir = path.join(ver_dst_dir, 'raw')

    wisdom2eg_src_path = path.join(raw_src_dir, 'wisdom2eg.tsv')
    wisdom2eg_dst_path = path.join(raw_dst_dir, 'wisdom2eg.tsv')


    src = get_wisdom_and_eg(wisdom2eg_src_path)
    df = pd.DataFrame.from_records(src, columns =['wisdom', 'context'])
    dst = get_parsed_df(df)
    dst = pd.DataFrame.from_records(dst, columns =['wisdom', 'context'])
    dst = dst.sort_values(by='wisdom')
    dst.to_csv(wisdom2eg_dst_path, sep='\t', index=False)


if __name__ == "__main__":
    main()