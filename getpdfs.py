import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparse
from os.path import exists, join
from os import makedirs
import re
from slugify import slugify_url
from urlparse import urljoin
import json
import errno


STASH_DIR = join('pdfs', 'fetched')
HOMEPAGE_URL = 'http://www.cityofpaloalto.org/gov/agendas/council/default.asp'
BASE_URL = 'http://www.cityofpaloalto.org/gov/agendas/council/'

MIN_YEAR = 2002
MAX_YEAR = 2017 #exclusive

# gets all the pdf links over all years of city council
def get_year_urls(year):
    links_arr = []
    page_url = BASE_URL + str(year) + '.asp'
    resp = requests.get(page_url)
    soup = BeautifulSoup(resp.text, 'lxml')
    rows = soup.select('table tbody > tr')
    for row in rows:
        datetd = row.find('td')
        if datetd:
            rawdate = row.find('td').text
            if 'PIC' not in rawdate and re.search(r'\w+ +\d+ *, 20\d\d', rawdate):
                date = dateparse.parse(rawdate).strftime('%Y-%m-%d')
                for cell in row.select('td'):
                    link = cell.find('a')
                    if link and 'Video' not in link.text:
                        fname = date + '_' + slugify_url(link.text) + '.pdf'
                        url = urljoin(page_url, link['href'])
                        links_arr.append((url, fname))
    return links_arr

# download the url to specified filename
def download_and_save(url, filename):
    if not exists(filename):
        print("Downloading: " + url)
        resp = requests.get(url)
        with open(filename, 'wb') as f:
            print("Saving to:" + filename)
            f.write(resp.content)
    else:
        print('{} already exists'.format(filename))


def update_jsonmap(jsonmap, url, fname):
    jsonmap[fname] = url
    return jsonmap

if __name__ == '__main__':
    # makedirs(STASH_DIR, exist_ok=True)
    try:
        makedirs(STASH_DIR)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    years = list(range(MIN_YEAR, MAX_YEAR)) + ['default']
    jsonmap = {};

    for year in years:
        print(year)
        things = get_year_urls(year)
        for url, fname in things:
            fullname = join(STASH_DIR, fname)
            download_and_save(url, fullname)
            jsonmap = update_jsonmap(jsonmap, url, fname)

    with open('datamap.json', 'w') as outfile:
        json.dump(jsonmap, outfile)
