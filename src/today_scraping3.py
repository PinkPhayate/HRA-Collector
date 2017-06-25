import page_scraping3 as ps3
from bs4 import BeautifulSoup

def find_hid(td):
    # get hid
    for link in td.findAll('a'):
        # if 'href' in link.attrs:
        url = link.attrs['href']
        # if horse instead of /horse/, cannot point at only hid
        if "/horse/" in link.attrs['href']:
            tmp = url.split('/')
            return tmp[4]
    return None

def scrape_race_info(source):
    soup = BeautifulSoup(source, "lxml")
    hid_list = []
    list = []
    # Extract status
    title = soup.find('h1')
    print(title.text)
    # if title.text is not correct (e.g. another race), remove
    table = soup.find(class_='race_table_old nk_tb_common')
    for tr in table.findAll('tr', ''):
        # list = []
        for td in tr.findAll('td', ''):
            # get house status
            word = " ".join(td.text.rsplit())
            list.append(word)

            hid = find_hid(td)
            if hid is not None:
                list.append(hid)

    hid_list.append(list)
    return hid_list

url = 'http://race.netkeiba.com/?pid=race_old&id=c201702010401'
source = ps3.get_request_via_get(url)
list = scrape_race_info(source)
print(list)
