import os

import wandb
import pandas as pd
import numpy as np

from storyteller.paths import DATA_DIR

spec = {
    'ver': '4',
    'dtype': 'eg',
}

conf = {
    'ENTITY_NAME': 'wisdomify',
    'PROJECT_NAME': 'wisdomify',

    'job_type': 'load_opendict_raw_data',

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


if __name__ == '__main__':
    load_and_log()
