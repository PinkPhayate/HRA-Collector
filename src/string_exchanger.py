import pandas as pd
FIELD_LIST = ['良','稍','不','重']
def beautify_df(filename):
    df = pd.read_csv(filename, header=None)
    fs = convert_field_status2dummy(df.ix[:,16])
    dist = divide_columns(df.ix[:,15])
    df = pd.concat([df.ix[:,:14], dist, fs, df.ix[:,17:]], axis=1)
    # print(df)
    df.to_csv(filename)

# divide field type and course distance
def divide_columns(d):
    tmp = d.str.extract('(.)([0-9]+)', expand=False)
    # print(tmp)
    dmy = pd.get_dummies(tmp.ix[:,0])
    df = pd.concat([dmy, tmp.ix[:,1]], axis=1)
    return df



#  convert field status
def convert_field_status2dummy(d):
    [validate_field_status(x) for x in d]
    dmy = pd.get_dummies(d)
    k = len(FIELD_LIST)-len(dmy.columns)
    for i in range(k):
        dmy = add_columns(dmy)
    return dmy

def add_columns(dmy):
    if '良' not in dmy.columns:
        dmy['良'] = 0.0
    if '稍' not in dmy.columns:
        dmy['稍'] = 0.0
    if '不' not in dmy.columns:
        dmy['不'] = 0.0
    if '重' not in dmy.columns:
        dmy['重'] = 0.0
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
