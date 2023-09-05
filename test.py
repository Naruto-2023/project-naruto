import psycopg2
import os
import pandas as pd
import re

def conection(user_name,pwd,host_name):
    try:
        conn = psycopg2.connect(host=host_name, dbname='new_db', user=user_name, password=pwd, port=5432)

        print("successfully connected")
        cur = conn.cursor()

        return cur

    except Exception as er:
        print(er)

def get_col_headers(cur):
    try:
        print("col headers called")
        cur.execute("SELECT column_name  "
                    "FROM information_schema.columns "
                    "WHERE table_name = 'stud_dtl' AND  table_schema = 'public';")
        headers=[]
        # So while we are fetching the col headers the data are coming like ('studrollno'), as a tuple
         # for this reason we used regular expression library here to remove the (' from the string
        for col_head in cur.fetchall():
            headers.append(re.sub(r"[^a-zA-Z0-9 ]", "", str(col_head)))
        return headers

    except Exception as er:
        print(er)
def get_sql_data(cur):
    try:
        cur.execute("SELECT * FROM public.stud_dtl;")
        data = cur.fetchall()
        #print(data)
        return data

    except Exception as er:
        print(er)

def do_start():
    user_name = os.environ.get('db_username')
    pwd = os.environ.get('db_password')
    host_name = os.environ.get('db_host')


    #step: 1
    cur = conection(user_name,pwd,host_name)
    #step: 2
    headers = get_col_headers(cur)

    #step: 3
    data = get_sql_data(cur)
    data_df = pd.DataFrame(data,columns=headers)

    print(data_df)


if __name__ == '__main__':
    do_start()



