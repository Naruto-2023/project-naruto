import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime


class naruto_load:
    def __init__(self,pg_db_host, pg_db_name, pg_db_user, pg_db_password, pg_db_tables,email_file_loc,email_arc_loc, pgdb_schema):
        self.pg_db_host = pg_db_host
        self.pg_db_name = pg_db_name
        self. pg_db_user = pg_db_user
        self.pg_db_password = pg_db_password
        self.pg_db_tables = pg_db_tables
        self.email_file_loc = email_file_loc
        self.email_arc_loc = email_arc_loc
        self.pgdb_schema = pgdb_schema

        #creating postgres connection
        self.conn = psycopg2.connect(host=self.pg_db_host, dbname=self.pg_db_name, user=self.pg_db_user,
                                password=self.pg_db_password, port=5432)
        self.cur = self.conn.cursor()


    # def create_pg_db_connection(self):
    #     print(self.pg_db_password)
    #     conn = psycopg2.connect(host=self.pg_db_host, dbname=self.pg_db_name, user=self. pg_db_user, password=self.pg_db_password, port=5432)
    #     self.cur = self.conn.cursor()
    #     return self.conn,self.cur

    def engine_conn(self):
       #conn_string =  "postgresql+psycopg2://postgres:Naruto2023@13.201.93.105:5432/postgres"
        conn_string = "postgresql+psycopg2://"+self.pg_db_user+":"+self.pg_db_password+"@" +self.pg_db_host+"/"+self.pg_db_name
        print(conn_string)
        engine = create_engine(conn_string)
        print(engine)
        return engine



    def reading_and_loading_data_into_pg_db(self,engine):

        col_count = 0
        print(self.email_file_loc+'/school_data.xlsx')
        with pd.ExcelFile(self.email_file_loc+'/school_data.xlsx') as f:
            sheets = f.sheet_names
            for sht in sheets:
                print("sht:", sht)
                data = pd.read_excel(self.email_file_loc+'/school_data.xlsx', sheet_name=sht)
                try:
                    data.to_sql(
                        self.pg_db_tables[col_count],
                        con=engine,
                        schema=self.pgdb_schema,
                        index=False,
                        if_exists='append',
                        method=None
                    )
                    print("Loaded successfully")
                    col_count = col_count + 1

                except Exception as err:
                    print(err)

    def deleting_duplicates(self):
        for table in self.pg_db_tables:
            query = f"delete from {self.pgdb_schema}.{table} a using {self.pgdb_schema}.{table} b where a = b and a.ctid < b.ctid".format(self.pgdb_schema,table)
            print(query)
            self.cur.execute(query)

        print("duplicated recprds deleted successfully")
        self.conn.commit()







def code_start(pg_db_host, pg_db_name, pg_db_user, pg_db_password, pg_db_tables,email_file_loc,email_arc_loc, pgdb_schema):
    load_obj = naruto_load(pg_db_host, pg_db_name, pg_db_user, pg_db_password, pg_db_tables,email_file_loc,email_arc_loc, pgdb_schema)
    engine  = load_obj.engine_conn()
    load_obj.reading_and_loading_data_into_pg_db(engine)
    load_obj.deleting_duplicates()