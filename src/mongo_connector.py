import pymongo


class NOSQL_connector(object):
    def __init__(self):
        self.cli = pymongo.MongoClient('localhost',27017)
        self.db = self.cli.hra

    def  _insert_to_nosql(self, dict):
        self.db.hist.save(dict)
        print('SUCCESS: save race_ids ')

    def insert_race_history(self,race_name, rids):
        dict = {'race_name':race_name, 'rids':rids}
        self._insert_to_nosql(dict)

    def insert_hids(self,rid, hids):
        dict = {'rid':rid, 'hids':hids}
        self._insert_to_nosql(dict)

    def insert_history_rids(self,hid, rids):
        dict = {'hid':hid, 'hids':rids}
        self._insert_to_nosql(dict)

    def insert_race_result(self,rid, res_dict):
        dict = {'race_res':rid, 'res_dict':res_dict}
        self._insert_to_nosql(dict)

    def get_rids_by_name(self,race_name):
        dict = self.db.hist.find_one({'race_name': race_name})
        if dict:
            # print(dict['rids'])
            return dict['rids']
        else:
            print(race_name+' : doesnt have data')
            return None

    def get_hids_by_rid(self,rid):
        dict = self.db.hist.find_one({'rid': rid})
        if dict:
            # print(dict['hids'])
            return dict['hids']
        else:
            print('hids dont be found - key name is : ' + rid)
            return None

    def get_history_rids(self,hid):
        dict = self.db.hist.find_one({'hid': hid})
        if dict:
            # print(dict['rids'])
            return dict['rids']
        else:
            print('rids dont be found - key name is : ' + hid)
            return None

    def get_race_result(self, rid):
        dict = self.db.hist.find_one({'race_res': rid})
        if dict:
            # print(dict)
            return dict
        else:
            print('race_res dont be found - key name is : ' + rid)
            return None
