import page_scraping3 as ps3
import mongo_connector as mgcon


def test_insert_race_odds_into_mongo():
    DOMAIN = 'http://db.netkeiba.com/'
    rid = '201605020611'
    url = DOMAIN + 'race/' + rid + '/'
    source = ps3.get_request_via_get(url)
    dict = ps3.scrape_res(source, rid)
    nosql_connector = mgcon.NOSQL_connector()
    nosql_connector.insert_odds(rid=rid, odds_dict=dict)


test_insert_race_odds_into_mongo()
