import pandas as pd
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from paramiko import SSHClient, AutoAddPolicy
import MySQLdb as db
from storyteller.secrets import GW_HOST, DB_PORT, DB_HOST, GW_PORT, DB_USER, DB_PW, GW_PKEY, GW_USER


class SSHTunnel:
    def __init__(self,
                 gateway_addr: str,
                 gateway_port: int,
                 gateway_user: str,
                 gateway_public_key: str,

                 database_addr: str,
                 database_port: int,
                 ):
        self.__local_port = 33600

        self.gateway_addr = gateway_addr
        self.gateway_port = gateway_port
        self.gateway_user = gateway_user
        self.gateway_public_key = gateway_public_key
        self.database_addr = database_addr
        self.database_port = database_port

        self.tunnel = self._establish_tunnel()

    def _establish_tunnel(self):
        return SSHTunnelForwarder(
            ssh_address_or_host=(self.gateway_addr, self.gateway_port),
            ssh_username=self.gateway_user,
            ssh_pkey=self.gateway_public_key,
            remote_bind_address=(self.database_addr, self.database_port),
            local_bind_address=('127.0.0.1', self.__local_port)
        )

    def get_DB_engine(self, database_user: str, database_pw: str):
        return create_engine('mysql+mysqldb://{user}:{pw}@{addr}'
                             .format(user=database_user, pw=database_pw,
                                     addr='127.0.0.1:{port}'.format(port=self.__local_port)),
                             encoding='utf-8')


class DBController:
    """
    if the DB can be accessed only via SSH, you must start tunnel to use other methods.
    and you must close tunnel when you finish to use DB engine.
    """
    def __init__(self,
                 user: str,
                 password: str,
                 schema: str
                 ):

        self.database_user = user
        self.database_pw = password
        self.database_schema = schema

        self._tunnel_builder = SSHTunnel(
            gateway_addr=GW_HOST,
            gateway_port=GW_PORT,
            gateway_user=GW_USER,
            gateway_public_key=GW_PKEY,

            database_addr=DB_HOST,
            database_port=DB_PORT,
        )

    def start_tunnel(self):
        if not self._tunnel_builder.tunnel.is_active:
            try:
                self._tunnel_builder.tunnel.start()
                print("Tunnel Establish Succeed")

            except:
                raise ConnectionError("SSH Tunnel Establish Failed")

    def close_tunnel(self):
        if self._tunnel_builder.tunnel.is_active:
            self._tunnel_builder.tunnel.close()

    def _get_engine(self):
        global engine
        if self._tunnel_builder.tunnel.is_active:
            return self._tunnel_builder.get_DB_engine(database_user=self.database_user, database_pw=self.database_pw)

        else:
            raise ConnectionRefusedError("To obtain DB engine, you must start the tunnel.")

    def get_df_from_sql(self,
                        target_query: str) -> pd.DataFrame:
        global engine, query_result

        try:
            engine = self._get_engine()

        except:
            raise ConnectionError("DB connection Establish Failed.")

        else:
            query_result = pd.read_sql_query(sql=target_query, con=engine)

        finally:
            engine.dispose()

        return query_result

    def _create_table(self,
                      columns: dict,
                      index: bool,
                      target_table_name: str,
                      primary_key: str = None
                      ):
        request_columns = ',\n'.join(map(lambda row: "{colName} {colType}".format(colName=row[0], colType=row[1]),
                                         columns.items()))
        if index:
            request_columns += ",\n`index` BIGINT"
            if primary_key is None:
                primary_key = "`index`"

        request_columns += ',\nprimary key({primary_key})'.format(primary_key=primary_key)

        self.execute_query(
            query="CREATE TABLE {schema}.{table} ({cols})".format(schema=self.database_schema,
                       table=target_table_name,
                       cols=request_columns
                       )
        )

    def save_df_to_sql(self,
                       origin_df: pd.DataFrame,
                       target_table_name: str,
                       if_exists: str,
                       index: bool,
                       columns: dict,
                       primary_key: str = None
                       ):
        """
        :param primary_key: primary key for DB saving
        :param origin_df:
        :param target_table_name:
        :param if_exists:
        :param index:
        :param columns: this dictionary should have key-value form as column_name: data_type(SQL type)
        :return:
        """
        global engine

        if not index and not primary_key:
            raise ValueError("If index is False, you must provide information about primary key.")

        try:
            engine = self._get_engine()

        except:
            raise ConnectionError("DB connection Establish Failed.")

        else:
            if if_exists == 'replace':
                if self.is_table_exist(target_db=self.database_schema, target_table=target_table_name):
                    self.drop_table(schema=self.database_schema, table=target_table_name)

                self._create_table(
                    target_table_name=target_table_name,
                    index=index,
                    columns=columns,
                    primary_key=primary_key
                )

                origin_df.to_sql(
                    con=engine,
                    name=target_table_name,
                    schema=self.database_schema,
                    if_exists='append',
                    index=index
                )

            else:
                if not self.is_table_exist(target_db=self.database_schema, target_table=target_table_name):
                    self._create_table(
                        target_table_name=target_table_name,
                        index=index,
                        columns=columns,
                        primary_key=primary_key
                    )

                origin_df.to_sql(
                    con=engine,
                    name=target_table_name,
                    schema=self.database_schema,
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
            raise ConnectionError("DB connection Establish Failed.")

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

    def execute_query(self,
                      query: str):
        global engine

        try:
            engine = self._get_engine()

        except:
            raise ConnectionError("DB connection Establish Failed.")

        else:
            with engine.connect() as conn:
                conn.execute(query)

        finally:
            engine.dispose()

    def drop_table(self,
                   schema: str,
                   table: str):
        self.execute_query(
            query="DROP TABLE {schema}.{table}".format(schema=schema, table=table),
        )
