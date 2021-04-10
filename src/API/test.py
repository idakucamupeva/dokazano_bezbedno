from googlesearch import search
import sys
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd


def scrapSite(urls, searchInput):
    unscraped = deque(urls)
    scraped = set()

    while len(unscraped):
        url = unscraped.popleft()
        scraped.add(url)

        #test = 'https://www.blic.rs/vanredno-stanje'
        print("Crawling URL %s" % url)
        try:
            response = requests.get(url)
            print("Successful request!")
            # print(response.text)      # html format
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            print("Unsuccessful request!")
            continue

        r = re.compile(rf"{searchInput}|(\bvanredno stanje\b)|(\bpožar\b)|(\bzemljotres\b)|(\bpoplava\b)|(\brat\b)|(\bepidemija\b)|(\bpandemija\b)|(\bprirodna katastrofa\b)", flags= re.I | re.X)
        requiredWords = r.findall(response.text)

        print("\n----->URL: ", url)
        for x in requiredWords:
            print(x)







#-----------------------------
def googleSearch(searchInput):
    '''
    searchResult = search(searchInput, num_results=4)  # 5 links
    for l in searchResult:
        print(l);
    #scrapSite(searchResult[0])
    #scrapSite(searchResult[1])
    '''

    searchResult = [
        'https://www.blic.rs/vanredno-stanje',
        'https://rs.n1info.com/tag/vanredno-stanje/',
        'https://nova.rs/tag/vanredno-stanje/'
    ]

    #           links         cityName
    scrapSite(searchResult, searchInput)


#------------------------
if __name__ == "__main__":

    ''' Zakomentarisano zbog testiranja
    if len(sys.argv) == 1:
        print("Fali argument!")
        exit()
    '''

    argv = sys.argv
    #cityName = argv[1:]
    cityName = "Beograd"
    searchInput = "" + cityName + " "

    googleSearch(searchInput)
