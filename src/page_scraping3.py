import csv
import re
import json
import lxml
import pandas as pd
from bs4 import BeautifulSoup
from os import path
from urllib import request
from urllib import parse
import record_saver as saver
import codecs
import string_exchanger as se
import sql_connector as sqlcn
import mongo_connector as mgcon
import logging

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
    # f = open('./../DATA/Race/' + output_file, 'w')
    # csvWriter = csv.writer(f)
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
        # list = []
        for td in tr.findAll('td', ''):
            # get house status
            word = " ".join(td.text.rsplit())
            # list.append(word)

            # get hid
            for link in td.findAll('a'):
                # if 'href' in link.attrs:
                url = link.attrs['href']
                # if horse instead of /horse/, cannot point at only hid
                if "/horse/" in link.attrs['href']:
                    tmp = url.split('/')
                    # list.append(tmp[2])
                    hid_list.append(tmp[2])

        # csvWriter.writerow(list)
    # f.close()
    return hid_list


def scrape_res(source, rid):
    soup = BeautifulSoup(source, "lxml")

    dict = {}
    table = soup.find(class_='pay_block')
    for tr in table.findAll('tr', ''):
        th = tr.find('th').string
        key = th
        value = []
        for td in tr.findAll('td', ''):
            if td.string is None:
                td = td.get_text(separator='*')
                td = td.replace(' ', '')
                td = td.split('*')
                value.append(td)
            else:
                td = td.string
                td = td.replace(' ', '')
                td = td.replace('→', '-')
                value.append(td)
        dict[key] = value
    return dict



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
    with codecs.open("./../DATA/Result/odds_dict.json", 'w', 'utf-8') as f:
        dump = json.dumps(odds_dict, ensure_ascii=False)
        f.write(dump)

def scrape_horse_history(source, hid):
    output_file = hid + '.csv'
    filename = './../DATA/Horse/' + output_file
    f = open(filename, 'w')
    csvWriter = csv.writer(f)
    soup = BeautifulSoup(source, "lxml")
    soup.prettify(formatter=lambda s: s.replace(u'\xa0', 'None'))
    history_df = pd.DataFrame([])

    table = soup.find(
        "table", attrs={"class": "db_h_race_results nk_tb_common"})
    for tr in table.findAll('tr'):
        list = []
        for td in tr.findAll("td"):
            word = " ".join(td.text.rsplit())
            list.append(word)
            # get race id
            # aタグのhref属性にraceという文字を含んでいる　かつ　title属性が一文字以上ある
            for a in td.find_all('a', href=re.compile("race"),
                                 title=re.compile(".+")):
                tmp = a.attrs['href'].split('/')
                list.append(tmp[2])

        csvWriter.writerow(list)
    f.close()
    # write to mysql
    sqlcn.save(hid)


def get_request_via_post(word):
    logging.info('send post request to '+DOMAIN)
    # create paramator with consts x=0,y=0,pid=race_list
    _param = _param_creator(word=word)
    with request.urlopen(DOMAIN, data=_param.encode('utf8')) as res:
        html = res.read().decode('euc-jp', 'ignore')
        return html


def get_request_via_get(url):
    logging.info('send get request to ' + url)
    source = request.urlopen(url)
    return source


def _param_creator(word):
    prefix = 'y=0&word='
    keyword = parse.quote_plus(word, encoding="eucjp")
    suffix = '&pid=race_list&x=0'
    return prefix + keyword + suffix


def main(words):
    # 1. get supecified race ids
    nosql_connector = mgcon.NOSQL_connector()

    rids = nosql_connector.get_rids_by_name(race_name=words[0])
    if not rids:
        logging.info('could not find rids from origin.')
        print('could not find rids from origin.')
        source = get_request_via_post(words[0])
        try:
            rids = scrape_rid(words, source)
        except Exception:
            logging.warning('could not get rids by get_request_via_post')
            print('could not get rids by get_request_via_post')
        # filename = './../DATA/race_id_list.csv'
        # saver.writeCsv(rids, filename)
        nosql_connector.insert_race_history(race_name=words[0], rids=rids)

    horce_dict = {}

    # 2. get list of hource_id who attends the race in year(rid)
    if not rids:
        logging.warning('exception has occured. could not find rids ')
        print('exception has occured. could not find rids ')
        return
    for rid in rids:
        logging.info('get list of race_id: ' + rid)
        hids = nosql_connector.get_hids_by_rid(rid=rid)
        source = None
        if not hids:
            print('scraping for hource_id')
            url = DOMAIN + 'race/' + rid + '/'
            source = get_request_via_get(url)
            # doc = source.read()
            output_file = rid + '.csv'
            hids = scrape_race_info(source, output_file, words[0])
            nosql_connector.insert_hids(rid=rid, hids=hids)
        horce_dict[rid] = hids

        # scrape RATE data
        # TODO: save to nosql
        race_results = nosql_connector.get_race_result(rid=rid)
        # output_file = './../DATA/Result/res_' + rid + '.csv'
        # if not path.isfile(output_file):
        if source is None and race_results is None:
            print("start to scrape race id: " + rid)
            url = DOMAIN + 'race/' + rid + '/'
            source = get_request_via_get(url)
        if race_results is None:
            try:
                dict = scrape_res(source, rid)
                nosql_connector.insert_odds(rid=rid, odds_dict=dict)
            except Exception:
                print('failt to scrape result of race id: '+rid)

    # 3. get history data of entried horse
    for rid in rids:
        print('get history of house in race that id: ' + rid)
        old_hids = horce_dict[rid]
        for hid in old_hids:
            url = DOMAIN + 'horse/' + hid + '/'
            source = get_request_via_get(url)
            output_file = hid + '.csv'
            scrape_horse_history(source, hid)

    # normalize rate data
    normalize_race_odds(rids)

if __name__ == '__main__':
    words = [u'宝塚記念']
    main(words)

# @FOR TEST
# hid = '2001110060'
# url = DOMAIN + 'horse/' + hid + '/'
# source = get_request_via_get(url)
# output_file = hid + '.csv'
# scrape_horse_history(source, output_file)
# words = [u'NHKマイル']
# source = get_request_via_post(words[0])
# rids = scrape_rid(words, source)
# nosql_connector = mgcon.NOSQL_connector()
# nsql.insert_race_history(race_name=words[0], rids=rids)
# nsql.get_rids_by_name(race_name=u'NHKマイル')
# rs_list = nosql_connector.get_rids_by_name(race_name='NHK')
