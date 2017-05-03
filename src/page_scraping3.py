import csv
import re
import json
import lxml
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import record_saver as saver

DOMAIN = 'http://db.netkeiba.com/'

def scrape_rid(words, source):
    """
    1. read page source
    2. scrape rid (race id)
    return -> race_id list
    """
    soup = BeautifulSoup(source, "lxml")
    table = soup.find("table", attrs={"class": "nk_tb_common race_table_01"})
    list = []
    # limitter for 10 years
    for tr in table.findAll('tr'):
        if len(list) > 12:
            break

        for td in tr.findAll("td", attrs={"class": "txt_l"}):
            for link in td.findAll('a'):
                url = link.attrs['href']
                title = link.attrs['title']
                if "race" in url and _validate_race_title(title, words):
                    tmp = url.split('/')
                    list.append(tmp[2])
    return list


def _validate_race_title(title, words):
    for word in words:
        if word not in title:
            return False
    return True

def scrape_race_info(source, output_file, word):
    # read page source code
    f = open('./../DATA/Race/' + output_file, 'w')
    csvWriter = csv.writer(f)
    # soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
    soup = BeautifulSoup(source, "lxml")
    hid_list = []
    # Extract status
    title = soup.find('h1')
    print(title.text)
    # if title.text is not correct (e.g. another race), remove
    if word not in title.text:
        return hid_list
    table = soup.find(class_='race_table_01 nk_tb_common')
    for tr in table.findAll('tr', ''):
        list = []
        for td in tr.findAll('td', ''):
            # get house status
            word = " ".join(td.text.rsplit())
            list.append(word)

            # get hid
            for link in td.findAll('a'):
                # if 'href' in link.attrs:
                url = link.attrs['href']
                # if horse instead of /horse/, cannot point at only hid
                if "/horse/" in link.attrs['href']:
                    tmp = url.split('/')
                    list.append(tmp[2])
                    hid_list.append(tmp[2])

        csvWriter.writerow(list)
    f.close()
    return hid_list


def scrape_res(source, output_file):
    f = open('./../DATA/Result/res_' + output_file, 'w')
    csvWriter = csv.writer(f)
    soup = BeautifulSoup(source, "lxml")

    table = soup.find(class_='pay_block')
    for tr in table.findAll('tr', ''):
        list = []
        th = tr.find('th').string
        list.append(th)
        for td in tr.findAll('td', ''):
            if td.string == None:
                td = td.get_text(separator=' ')
                list.append(td)
            else:
                list.append(td)
        csvWriter.writerow(list)
    f.close()


def normalize_race_odds(years):
    odds_dict = {}
    for year in years:
        y = str(year)
        output_file = y + '.csv'
        f = open('./../DATA/Result/res_' + output_file, "rt", encoding='utf-8')
        dataReader = csv.reader(f)
        dict = {}
        for row in dataReader:
            odds = row[2]
            if ' ' in odds:
                odds = odds.split('　')
            num = row[1].replace('→', '-')
            num = num.replace(' - ', '-')
            if ' ' in num:
                num = num.split('　')
            dict[row[0]] = {'num': num, 'odds': row[2]}

        odds_dict[y] = dict
    f = open("./../DATA/Result/odds_dict.json", "w")
    json.dump(odds_dict, f, ensure_ascii=False)
    f.close()


def scrape_horse_history(source, output_file):
    f = open('./../DATA/Horse/' + output_file, 'w')
    csvWriter = csv.writer(f)
    soup = BeautifulSoup(source, "lxml")
    soup.prettify(formatter=lambda s: s.replace(u'\xa0', 'None'))
    history_df = pd.DataFrame([])

    table = soup.find(
        "table", attrs={"class": "db_h_race_results nk_tb_common"})
    for tr in table.findAll('tr'):
        list = []
        flg = True
        for td in tr.findAll("td"):
            word = " ".join(td.text.rsplit())
            list.append(word.encode('utf-8'))

        csvWriter.writerow(list)
    f.close()



def get_request_via_post(word):
    # create paramator with consts x=0,y=0,pid=race_list
    _param = _param_creator(word=word)
    with urllib.request.urlopen(DOMAIN, data=_param.encode('utf8')) as res:
        html = res.read().decode('euc-jp', 'ignore')
        return html


def get_request_via_get(url):
    source = urllib.request.urlopen(url)
    return source

def _param_creator(word):
    prefix = 'y=0&word='
    keyword = urllib.parse.quote_plus(word, encoding="eucjp")
    suffix = '&pid=race_list&x=0'
    return prefix + keyword + suffix


def main(words):
    # 1. get supecified race ids
    source = get_request_via_post(words[0])
    rids = scrape_rid(words, source)
    filename = './../DATA/race_id_list.csv'
    saver.writeCsv(rids, filename)

    horce_dict = {}

    # 2. get list of hource_id who attend the race in year(rid)
    for rid in rids:
        print('get list of hource_id: ' + rid)
        url = DOMAIN + 'race/' + rid + '/'
        source = get_request_via_get(url)
        output_file = rid + '.csv'
        hids = scrape_race_info(source, output_file, words[0])
        horce_dict[rid] = hids
        # scrape RATE data
        source = get_request_via_get(url)
        scrape_res(source, output_file)

    # 3. get history data of entried horse
    for rid in rids:
        print('get history of house in ' + rid)
        old_hids = horce_dict[rid]
        for hid in old_hids:
            url = DOMAIN + 'horse/' + hid + '/'
            source = get_request_via_get(url)
            output_file = hid + '.csv'
            scrape_horse_history(source, output_file)

    # normalize rate data
    normalize_race_odds(rids)


if __name__ == '__main__':
    # word = '皐月賞'
    words = [u'NHKマイル']
    main(words)
