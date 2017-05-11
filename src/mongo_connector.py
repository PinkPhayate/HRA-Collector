import pymongo


cli = pymongo.MongoClient('localhost',27017)
db =cli.hra

def insert_race_history(race_name, rids):
    dict = {'race_name':race_name, 'rids':rids}
    db.hist.save(dict)
    print('SUCCESS: save race_ids ')

def get_history_rids(race_name):
    dict = db.hist.find_one({'race_name': race_name})
    print(dict['rids'])
