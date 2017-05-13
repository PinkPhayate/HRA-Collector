import pymongo


class NOSQL_connector(object):
    def __init__(self):
        cli = pymongo.MongoClient('localhost',27017)
        self.db =cli.hra

    def insert_race_history(self,race_name, rids):
        dict = {'race_name':race_name, 'rids':rids}
        self.db.hist.save(dict)
        print('SUCCESS: save race_ids ')

    def get_history_rids(self,race_name):
        dict = self.db.hist.find_one({'race_name': race_name})
        if dict and dict.has_key('rids'):
            print(dict['rids'])
            return dict['rids']
        else:
            print(race_name+' : doesnt have data')
            return None
