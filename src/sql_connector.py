import pandas as pd
import MySQLdb

args = {"hostname": "localhost",
        "db": "HRA",
        "user": "root",
        "passwd": "",
        "charset": "utf-8"
        }

# with MySQLdb.connect(**args) as cur:
#     # cur.execute("INSERT INTO Horse (id, poko_name) VALUES (%s, %s)", (id, poko_name))
#     cur.execute("INSERT INTO Horse VALUES (%s, %s)", (id, poko_name))


def insert_horse_history(df):
    for i, row in hid_dfs.iterrows():
        with MySQLdb.connect(**args) as cur:
            cur.execute("INSERT INTO Horse VALUES (%s, %s)", (id, poko_name))


# @FOR  TEST
import string_exchanger as se
import pandas as pd
hid = '2014110014'
output_file = hid + '.csv'
filename = './../DATA/Horse/' + output_file
df = pd.read_csv(filename, header=None)
df =  df.ix[:,:16]
dvd = se.divide_columns(df.ix[:,15])
df = df.drop([1,6,15],axis=1)
df = pd.concat([df,dvd],axis=1)
col = ["date","race","whether","race_name","race_id","all","frame","no","odds","fav","rank","jockey","hande","course","course_status","distance"]
df.columns = col
