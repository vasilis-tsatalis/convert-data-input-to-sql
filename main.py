#!/usr/bin/env python
# coding=utf-8

import argparse
import sys
import os
from datetime import datetime
# import pandas lib as pd
import pandas as pd

ENVIRONMENT_LIBRARY = os.environ.get('ENV_LIBRARY_DB')
DATA_FILE_PATH = os.environ.get('DATA_FILE_PATH')
SQL_FILE_PATH = os.environ.get('SQL_FILE_PATH')

async def open_sql_file(SQL_FILE):
    f = open(SQL_FILE_PATH + SQL_FILE, "a")
    f.write(f"CONNECT TO {ENVIRONMENT_LIBRARY};" + "\n")
    f.write("-----------------------------------------------------------------------------------------" + "\n")
    f.close()
    
async def close_sql_file(SQL_FILE):
    f = open(SQL_FILE_PATH + SQL_FILE, "a")
    f.write("CONNECT RESET;" + "\n")
    f.write("-----------------------------------------------------------------------------------------" + "\n")
    f.close()

async def read_excel_file(DATA_FILE, _SQL_FILE):
    
    dataframe1 = pd.read_excel(DATA_FILE_PATH + DATA_FILE)
    
    # First row of excel file is a header row
    # read by default 1st sheet of an excel file
    # Read all columns
    df = pd.DataFrame(dataframe1)
    # df = pd.DataFrame(dataframe1, columns=["col1", "col2", "col3"]) # Read specific columns

    counter = 0
    ########################################
    open_sql_file(_SQL_FILE)

    for ind in df.index:  

        _ID = str(df['ID'][ind])
        _USERNAME = df['Active Directory Username'][ind]

        counter += 1
        
        f = open("update_wbo_users.sql", "a")

        if (type(_USERNAME) != float): # there is no username - value is nan

            update_statement = f'UPDATE "ATBPROD"."WBOUSER" SET "USERNAME" = "{df['Active Directory Username'][ind]}" WHERE "ID" = {_ID};'

            f.write("--" + " " + str(counter) + "=> Username: '" + df['USERNAME'][ind] + "' update to: '" + _USERNAME + "'" + "\n")

        else: # if there is no need for access

            update_statement = f'UPDATE "ATBPROD"."WBOUSER" SET "ACTIVE" = "0" WHERE "ID" = {_ID};'

            f.write("--" + " " + str(counter) + "=> Username: '" + df['USERNAME'][ind] + "' set as Inactive" + "\n")


        f.write(update_statement + "\n")
        f.write("-----------------------------------------------------------------------------------------" + "\n")
        f.close()

        view_statement = f'SELECT * FROM "ATBPROD"."WBOUSER" WHERE WHERE "ID" = {_ID};'

        f2 = open("select_wbo_users.sql", "a")
        f2.write("--" + " " + str(counter) + "=> Check Username: '" + df['USERNAME'][ind] + "'" + "\n")
        f2.write(view_statement + "\n")
        f2.write("-----------------------------------------------------------------------------------------" + "\n")
        f2.close()


    close_sql_file(_SQL_FILE) 
    ########################################
    ########################################

def main(args):
    try:      
        if args.filetype == 'xlsx':
            read_excel_file(args.filename, args.sqlfile)
        elif args.filetype == 'csv':
            pass
        elif args.filetype == 'txt':
            pass
    except ValueError:
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Turn Data File to SQL File')
    parser.add_argument('--filename', type=str, dest='filename', help='Sample file name value', required=True)
    parser.add_argument('--filetype', type=str, dest='filetype', choices = ['xlsx', 'csv', 'txt'], help='File type,format', required=True)
    parser.add_argument('--sqlfile', type=str, dest='sqlfile', help='SQL file name value (*.sql)', required=True)
    
    args = parser.parse_args()
    main(args)
