import pandas as pd
FIELD_LIST = ['良','稍','不','重']
def beautify_df(filename):
    df = pd.read_csv(filename, header=None)
    df =  df.ix[:,:16]
    dvd = se.divide_columns(df.ix[:,15])
    df = df.drop([1,6,15],axis=1)
    df = pd.concat([df,dvd],axis=1)
    col = ["date","race","whether","race_name","race_id","all","frame","no","odds","fav","rank","jockey","hande","course","course_status","distance"]
    df.columns = col
    return df

def divide_columns(d):
    tmp = d.str.extract('(.)([0-9]+)', expand=False)
    # print(tmp)
    # dmy = pd.get_dummies(tmp.ix[:,0])
    # dmy = add_columns_ft(dmy)
    # df = pd.concat([dmy, tmp.ix[:,1]], axis=1)
    # return df
    return tmp


#  convert field status
def convert_field_status2dummy(d):
    [validate_field_status(x) for x in d]
    dmy = pd.get_dummies(d)
    k = len(FIELD_LIST)-len(dmy.columns)
    for i in range(k):
        dmy = add_columns_fs(dmy)
    return dmy

def add_columns_fs(dmy):
    if '良' not in dmy.columns:
        dmy['良'] = 0.0
    if '稍' not in dmy.columns:
        dmy['稍'] = 0.0
    if '不' not in dmy.columns:
        dmy['不'] = 0.0
    if '重' not in dmy.columns:
        dmy['重'] = 0.0
    return dmy

def add_columns_ft(dmy):
    if 'ダ' not in dmy.columns:
        dmy['ダ'] = 0.0
    if '芝' not in dmy.columns:
        dmy['芝'] = 0.0
    return dmy

def validate_field_status(e):
    if e == '良':
        return '0'
    elif e == '稍':
        return '1'
    elif e == '不':
        return '2'
    elif e == '重':
        return '3'
    else :
        print (' ==========unexpected field status==========: ' + e)
        return '4'

# @FOR TEST
# filename = './../DATA/Horse/2012103129.csv'
# beautify_df(filename)
