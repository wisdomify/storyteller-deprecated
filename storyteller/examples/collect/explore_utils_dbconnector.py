import pandas as pd

from storyteller.collect.utils.DBConnector import DBController
from storyteller.secrets import DB_USER, DB_PW

if __name__ == '__main__':
    controller = DBController(user=DB_USER,
                              password=DB_PW,
                              schema='test')

    test = pd.read_csv('../../../data/examples/egs_koreaUniv.csv').drop('Unnamed: 0', axis=1)

    controller.start_tunnel()
    controller.save_df_to_sql(
        origin_df=test,
        target_table_name='testing',
        if_exists='replace',
        index=True,
        columns={
            "wisdom": "TEXT",
            "eg_id": "BIGINT",
            "prev": "TEXT",
            "eg": "TEXT",
            "next": "TEXT",
            "full": "TEXT"
        },
        primary_key='eg_id'
    )
    controller.close_tunnel()
