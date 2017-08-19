from bs4 import BeautifulSoup
from urllib import request
import urllib.request
import csv, lxml
import page_scraping3 as ps
import mongo_connector as mgcon

DOMAIN = 'http://db.netkeiba.com/'
def scraping(url, output_file):
    # read page source code
    f = open('./../Data/' + output_file, 'w')
    csvWriter = csv.writer(f)


    soup = BeautifulSoup(request.urlopen(url), "lxml")
    # Extract status
    # title = soup.find('h1')
    # print title.text

    table = soup.find(class_='race_table_01 nk_tb_common shutuba_table')
    hid_list = []
    for tr in table.findAll('tr',''):
        list = []
        for td in tr.findAll('td',''):
            word = " ".join(td.text.rsplit())
            list.append( word.encode('utf-8') )

            # get hid only MAIN horse
            for link in td.findAll('a'):
                if 'target' not in link.attrs:  # if not MAIN horse, it doesn't have taget attribute.
                    break
                url = link.attrs['href']
                if "/horse/" in url: # if horse instead of /horse/, cannot point at only hid
                    tmp = url.split('/')
                    list.append(tmp[4])
                    hid_list.append(tmp[4])

        csvWriter.writerow(list)
    return hid_list

if __name__ == '__main__':

    # view.draw_title(version='1.1.0')
    # view.draw_race_title("Stayer's Stakes")

    rid = '201704020811'       #  TODO : args
    url = 'http://race.netkeiba.com/?pid=race&id=c'+str(rid)+'&mode=shutuba'
    output_file = str(rid) + '.csv'
    # scrape  TARGET RACE data
    hid_list = scraping(url, output_file=output_file)
    nosql_connector = mgcon.NOSQL_connector()
    nosql_connector.insert_hids(rid=rid, hids=hid_list)

    for hid in hid_list:
        url = DOMAIN + 'horse/' + hid + '/'
        print(url)
        source = ps.get_request_via_get(url)
        output_file = hid + '.csv'
        ps.scrape_horse_history(source, hid)
