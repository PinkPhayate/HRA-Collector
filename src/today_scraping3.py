from bs4 import BeautifulSoup
from urllib import request


class OddsMan(object):
    def get_request_via_get(self, url):
        source = request.urlopen(url)
        return source

    def __find_hid(self, td):
        # get hid
        for link in td.findAll('a'):
            url = link.attrs['href']
            if "/horse/" in link.attrs['href']:
                tmp = url.split('/')
                return tmp[4]
        return None

    def __find_rid(self, td):
        # get rid
        for link in td.findAll('a'):
            url = link.attrs['href']
            if "&" in url:
                tmp = url.split('&')
                tmp = tmp[1].split('=')
                return tmp[1][1:]
        return None


    def scrape_race_info(self, source):
        soup = BeautifulSoup(source, "lxml")
        df = []
        # Extract status
        title = soup.find('h1')
        print(title.text)
        self.title = title.text
        # if title.text is not correct (e.g. another race), remove
        table = soup.find(class_='race_table_old nk_tb_common')
        for tr in table.findAll('tr', ''):
            row = []
            for td in tr.findAll('td', ''):
                # get house status
                word = " ".join(td.text.rsplit())
                row.append(word)

                hid = self.__find_hid(td)
                if hid is not None:
                    row.append(hid)
            df.append(row)
        return df

    def scrape_race_id(self, source):
        soup = BeautifulSoup(source, "lxml")
        df = []
        body = soup.find(id="race_list_body")
        for col in body.findAll(class_='race_top_hold_list'):
            row = []
            for div in col.findAll(class_='racename'):
                rid = self.__find_rid(div)
                if rid is not None:
                    row.append(rid)
            df.append(row)
        return df

    def get_race_odds(self, race_id):
        url = 'http://race.netkeiba.com/?pid=race_old&id=c' + str(race_id)
        source = self.get_request_via_get(url)
        self.df = self.scrape_race_info(source)
        odds_list = [x[10] for x in self.df if len(x) > 0]
        return odds_list

    def get_race_ids(self, date):
        url = 'http://race.netkeiba.com/?pid=race_list&id=c' + str(date)
        source = self.get_request_via_get(url)
        df = self.scrape_race_id(source)
        return df

# race_id = '201702010401'
odds_man = OddsMan()
todays_race_id = odds_man.get_race_ids('0625')


# odds_dict = odds_man.get_race_odds(race_id)
# print(odds_dict)
