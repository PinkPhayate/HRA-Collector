import string_exchanger as se
import pandas as pd
import MySQLdb
args = {
    "host": "localhost",
    "database": "HRA",
    "user": "root",
    "password": "",
    "port":3306
}

def _clean_df(hid):
    output_file = hid + '.csv'
    filename = './../DATA/Horse/' + output_file
    df = pd.read_csv(filename, header=None)
    df =  df.ix[:,:16]
    dvd = _divide_columns(df.ix[:,15])
    df = df.drop([1,6,15],axis=1)
    df = pd.concat([df,dvd],axis=1)
    df.loc[:, -1] = int(hid)
    col = ["date","race","whether","race_name","race_id","all","frame","no","odds","fav","rank","jockey","hande","course","course_status","distance","hid"]
    df.columns = col
    _validate_df(df)
    return df

def _validate_df(df):
    df = df.apply(lambda)

def _divide_columns(d):
    tmp = d.str.extract('(.)([0-9]+)', expand=False)
    return tmp


def _connect_db(df):
    con = MySQLdb.connect(**args)
    table_name = "history"
    df.to_sql(table_name, con, flavor='mysql', index=False, if_exists='append')

def save(hid):
    print("start to save history data HID: " + hid)
    df = _clean_df(hid)
    _connect_db(df)

# @FOR TEST
# hid = '2001110060'
# df = _clean_df(hid)
# _connect_db(df)
