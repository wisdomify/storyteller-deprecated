import pandas as pd
from sqlalchemy import create_engine

from storyteller.secrets import DB_USER, DB_PW, DB_HOST, DB_PORT, STORYTELLER_SCHEMA


class DBController:
    def __init__(self,
                 user: str,
                 password: str,
                 address: str,
                 database: str,
                 charset: str = 'utf8mb4',
                 ):
        self._target_server = 'mysql+mysqldb://{user}:{pw}@{addr}/{db}?charset={charset}' \
            .format(user=user, pw=password, addr=address, db=database, charset=charset)

    def _get_engine(self):
        return create_engine(self._target_server, encoding='utf-8')

    def get_df_from_sql(self,
                        target_query: str) -> pd.DataFrame:
        global engine
        try:
            engine = self._get_engine()

        except:
            raise ConnectionError("DB connection establishment failed.")

        else:
            return pd.read_sql_query(sql=target_query, con=engine)

        finally:
            engine.dispose()

    def save_df_to_sql(self,
                       origin_df: pd.DataFrame,
                       target_table_name: str,
                       if_exists: str,
                       index: bool):
        global engine
        try:
            engine = self._get_engine()

        except:
            raise ConnectionError("DB connection establishment failed.")

        else:
            origin_df.to_sql(name=target_table_name,
                             con=engine,
                             if_exists=if_exists,
                             index=index
                             )

        finally:
            engine.dispose()

    def is_exist(self,
                 target_query: str) -> bool:
        global engine
        try:
            engine = self._get_engine()

        except:
            raise ConnectionError("DB connection establishment failed.")

        else:
            return True \
                if len(pd.read_sql_query(sql=target_query,
                                         con=engine)) != 0 \
                else False

        finally:
            engine.dispose()

    def is_table_exist(self,
                       target_db: str,
                       target_table: str) -> bool:

        return self.is_exist(target_query="select * from information_schema.tables "
                                          "where TABLE_SCHEMA = '{db}' and TABLE_NAME = '{table}'"
                             .format(db=target_db, table=target_table))


controller = DBController(user=DB_USER,
                          password=DB_PW,
                          address=f'{DB_HOST}:{DB_PORT}',
                          database=STORYTELLER_SCHEMA)
