#import library
import os
import sys
import logging
from datetime import datetime
import configparser

import naruto_email_1

LOCAL_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Config/Config.cnf'))


#additional attachment of utility file

#logger object to log the necessary information
logging.getLogger().setLevel(logging.INFO)
curr_time = datetime.now().strftime('%m%d%Y%H%M%S')



# f_name = 'logfile'+str(curr_time)+'.log'
# print(f_name)
# logging.basicConfig(filename=f_name, filemode='w', format='%(asctime)s - %(levelname)s -%(funcName)s - %(message)s')
#
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


    return email_file_loc, email_arc_loc, email_user, email_password

#code_start function
def code_start():
    print("Code execution started ...")
    email_file_loc, email_arc_loc, email_user, email_password = read_configfile()



    #Step 1: Triggering email fucntionality to Read the Excel file and drop into the Server file location
    naruto_email_1.code_start(email_file_loc, email_arc_loc, email_user, email_password)





#main method
if __name__ == '__main__':
    code_start()












