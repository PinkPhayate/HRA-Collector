import string_exchanger as se
import pandas as pd
import MySQLdb
import re
import json
args = {
    "host": "localhost",
    "database": "hra",
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
    df = _validate_df(df)
    return df

def _validate_df(df):
    df = df.apply(lambda x: _validate_race_id(x),axis=1)
    df = df.apply(lambda x: _validate_rank(x),axis=1)
    return df

def _validate_race_id(d):
    pattern = r"^\d+$"
    matchOB = re.match(pattern , str(d['race_id']))
    d['race_id'] = d['race_id'] if matchOB else 'NULL'
    return d

def _validate_rank(d):
    pattern = r"^\d+$"
    matchOB = re.match(pattern , str(d['rank']))
    d['rank'] = d['rank'] if matchOB else 0
    return d


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
def save_dict(word, rids):
    print("start to save race-id dict into mysql ")
    insertDb(word, rids)
    # json_obj = json.dumps({ word: rids })
    # with MySQLdb.connect(**args) as cur:
    #     cur.execute("INSERT INTO json_col VALUES %s", (json_obj))

def dbconnect():
    try:
        db = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='hra'
        )
    except Exception as e:
        sys.exit("Can't connect to database")
    return db

def insertDb(word, rids):
    try:
        data = { word: rids }
        json_data = json.dumps({ word: rids })
        db = dbconnect()
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO test_table(title,rids) \
        VALUES (%s,%s) """, (word, rids))
        # cursor.execute("""
        # INSERT INTO test_table2(rids) \
        # VALUES (%s) """, [json_data])
        cursor.close()
    except Exception as e:
        print (e)

# @FOR TEST
# hid = '2011105000'
# df = _clean_df(hid)
# print(df)
# _connect_db(df)
