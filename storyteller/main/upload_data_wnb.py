import os

import wandb
import pandas as pd
import string
from collections import Counter

import re

from datasets import load_dataset
from pprint import pprint as pp

from sklearn.utils import resample

from storyteller.paths import DATA_DIR

spec = {
    'ver': '4',
    'dtype': 'eg',
}

conf = {
    'ENTITY_NAME': 'wisdomify',
    'PROJECT_NAME': 'wisdomify',

    'job_type': 'replace_proverb_to_wisdom_token',

    'artifact_name': f"opendict_wisdom2{spec['dtype']}-raw",
    'description': f"""
    opendict Raw wisdom2{spec['dtype']} data crawled, split into train/val/test
    """,

    'metadata': {
        'source': [
            'namuwiki',
            'Korea University Corpus'
        ]
    }
}


def load():
    ver_dir = os.path.join(DATA_DIR, f"version_{spec['ver']}")
    return [
        pd.read_csv(os.path.join(ver_dir, f"train_wisdom2{spec['dtype']}.tsv"), sep='\t'),
        pd.read_csv(os.path.join(ver_dir, f"val_wisdom2{spec['dtype']}.tsv"), sep='\t'),
        pd.read_csv(os.path.join(ver_dir, f"test_wisdom2{spec['dtype']}.tsv"), sep='\t')
    ]


def load_and_log():
    # 🚀 start a run, with a type to label it and a project it can call home
    with wandb.init(project=conf['PROJECT_NAME'],
                    entity=conf['ENTITY_NAME'],
                    job_type=conf['job_type']) as run:
        datasets = load()  # separate code for loading the datasets
        names = ["training", "validation", "test"]

        # 🏺 create our Artifact
        raw_data = wandb.Artifact(
            conf['artifact_name'],
            type="dataset",
            description=conf['description'],
            metadata={"source": conf['metadata']['source'],
                      "sizes": {
                          'training': len(datasets[0]),
                          'validation': len(datasets[1]),
                          'test': len(datasets[2]),
                      }}
        )

        for name, data in zip(names, datasets):
            # 🐣 Store a new file in the artifact, and write something into its contents.
            with raw_data.new_file(name + ".tsv", mode="wb") as file:
                data.to_csv(file, sep='\t')
                # np.savez(file, x=data[spec['dtype']], y=data['wisdom'])

        # ✍️ Save the artifact to W&B.
        run.log_artifact(raw_data)


def pre_process(raw_data):
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

    return data_df


def read(data_dir, split):
    filename = split + ".tsv"
    return pd.read_csv(os.path.join(data_dir, filename), sep='\t')


def preprocess_and_log():
    with wandb.init(project=conf['PROJECT_NAME'],
                    entity=conf['ENTITY_NAME'],
                    job_type=conf['job_type']) as run:
        # 새롭게 저장할 아티펙트
        processed_data = wandb.Artifact(
            "init_kuniv-preprocess_wisdom_token", type="dataset",
            description="PreProcessed initial example sentences from Korea University Coropus where the proverbs are "
                        "replaced to [WISDOM].",
            metadata={
                'proverb_exist': False
            })

        # ✔️ declare which artifact we'll be using (기존에 있던 데이터셋)
        raw_data_artifact = run.use_artifact('init_kuniv_wisdom2eg-raw:latest')

        # 📥 if need be, download the artifact
        raw_dataset = raw_data_artifact.download()

        for split in ["training", "validation", "test"]:
            raw_split = read(raw_dataset, split)
            processed_dataset = pre_process(raw_split)

            with processed_data.new_file(split + ".tsv", mode="wb") as file:
                processed_dataset.to_csv(file, sep='\t')

        run.log_artifact(processed_data)


if __name__ == '__main__':
    # load_and_log()
    preprocess_and_log()
