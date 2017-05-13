import pymongo


class NOSQL_connector(object):
    def __init__(self):
        cli = pymongo.MongoClient('localhost',27017)
        self.db =cli.hra

    def insert_race_history(self,race_name, rids):
        dict = {'race_name':race_name, 'rids':rids}
        self.db.hist.save(dict)
        print('SUCCESS: save race_ids ')

    def insert_hids(self,rid, hids):
        dict = {'rid':rid, 'hids':hids}
        self.db.hist.save(dict)
        print('SUCCESS: save race_ids ')

    def get_history_rids(self,race_name):
        dict = self.db.hist.find_one({'race_name': race_name})
        if dict:
            print(dict['rids'])
            return dict['rids']
        else:
            print(race_name+' : doesnt have data')
            return None

    def get_hids_by_rid(self,rid):
        dict = self.db.hist.find_one({'rid': rid})
        if dict:
            print(dict['hids'])
            return dict['hids']
        else:
            print('doesnt be found - key name is : ' + rid)
            return None
