import page_scraping3 as ps3
import mongo_connector as mgcon
import MySQLdb

def test_insert_race_odds_into_mongo():
    DOMAIN = 'http://db.netkeiba.com/'
    rid = '201605020611'
    url = DOMAIN + 'race/' + rid + '/'
    source = ps3.get_request_via_get(url)
    dict = ps3.scrape_res(source, rid)
    nosql_connector = mgcon.NOSQL_connector()
    nosql_connector.insert_odds(rid=rid, odds_dict=dict)


def test_connect_sql():
    connector = MySQLdb.connect(
        user='root',
        passwd='root',
        port=3333,
        host='127.0.0.1',
        db='HRA')

    cursor = connector.cursor()
    cursor.execute("show columns from history")

    for row in cursor.fetchall():
        print(row)

    cursor.close
    connector.close


test_insert_race_odds_into_mongo()
test_connect_sql()
