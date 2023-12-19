#import library
import os
import sys
import logging
from datetime import datetime
import configparser

import naruto_email_1
import naruto_read_xl_load_db

LOCAL_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Config/Config.cnf'))

#logger object to log the necessary information
logging.getLogger().setLevel(logging.INFO)
curr_time = datetime.now().strftime('%m%d%Y%H%M%S')


#additional attachment of utility file


# f_name = 'logfile'+str(curr_time)+'.log'
# print(f_name)
# #
# logging.basicConfig(filename=log_fname, filemode='w', format='%(asctime)s - %(levelname)s -%(funcName)s - %(message)s')
# def hurra():
#     logging.info("hurrraa")
# hurra()
#primary class


#primary class fucntions


#local config function
def read_configfile():
    print("reading config files")
    n_lcl_config = LOCAL_CONFIG_FILE
    config = configparser.ConfigParser()
    config.read(n_lcl_config)

    email_file_loc = config.get('FOLDER_SECTION', 'email_file_location')
    email_arc_loc = config.get('FOLDER_SECTION', 'email_archive_location')
    email_user = config.get('EMAIL_CREDENTIAL', 'user_id')
    email_password = config.get('EMAIL_CREDENTIAL', 'password')

    pg_db_host = config.get('POSTGRES_DB','host')
    pg_db_name = config.get('POSTGRES_DB','db_name')
    pg_db_user = config.get('POSTGRES_DB','user_name')
    pg_db_password = config.get('POSTGRES_DB','pwd')
    pgdb_tables = config.get('POSTGRES_DB','table_names')
    pgdb_schema = config.get('POSTGRES_DB','schema')
    pg_db_tables = pgdb_tables.split(",")

    return email_file_loc, email_arc_loc, email_user, email_password, pg_db_host, pg_db_name, pg_db_user, pg_db_password, pg_db_tables, pgdb_schema


#code_start function
def code_start():
    print("Code execution started ...")
    email_file_loc, email_arc_loc, email_user, email_password,pg_db_host, pg_db_name, pg_db_user, pg_db_password, pg_db_tables, pgdb_schema = read_configfile()
    print(email_file_loc)

    #Step 1: Triggering email fucntionality to Read the Excel file and drop into the Server file location
    #naruto_email_1.code_start(email_file_loc, email_arc_loc, email_user, email_password)

    #Step 2: Triggering excel read function and load into DB tables
    #print(pg_db_host, pg_db_name, pg_db_user, pg_db_password, pg_db_tables)

    naruto_read_xl_load_db.code_start(pg_db_host, pg_db_name, pg_db_user, pg_db_password, pg_db_tables,email_file_loc,email_arc_loc, pgdb_schema)







#main method
if __name__ == '__main__':
    pass
    code_start()












