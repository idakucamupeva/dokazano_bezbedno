from googlesearch import search
import sys
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import bs4
import pandas as pd
import string


def scrapSite(searchInput):
    urls = [
        # ----------------------------------------------------------Portali
        'https://www.blic.rs/vanredno-stanje',
        'https://rs.n1info.com/tag/vanredno-stanje/',
        'https://nova.rs/tag/vanredno-stanje/'
        'https://www.juznevesti.com/Tagovi/vanredno-stanje.sr.html'

        # ----------------------------------------------------------Regioni
        'https://akv.org.rs/category/vanredno-stanje/?script=lat',
        # 'https://www.juznevesti.com/Tagovi/vanredno-stanje.sr.html',
        'http://www.rtvsumadija.com/tag/vanredno-stanje/'

    ]

    unscraped = deque(urls)
    scraped = set()
    dangerIndex = 0

    while len(unscraped):
        url = unscraped.popleft()
        scraped.add(url)

        try:
            response = requests.get(url)
            # print(response.text)      # html format
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # rb = re.compile(
        #    rf"{searchInput}|(\bvanredno stanje\b)|(\bpožar\b)|(\bzemljotres\b)|(\bpoplava\b)|(\brat\b)|(\bepidemija\b)|(\bpandemija\b)|(\bprirodna katastrofa\b)",
        #    flags=re.I | re.X)
        # r = re.compile(rf"^.*?{searchInput}.*?\bvanredno stanje\b.*?\bpožar\b.*?\bzemljotres\b.*?\bpoplava\b.*?\brat\b.*?\bepidemija\b.*?\bpandemija\b.*?\bprirodna katastrofa\b.*?$", flags= re.I | re.X)
        # r = re.compile(rf".*?{searchInput}.*?(\bvanredno stanje\b).*?", flags= re.I | re.X)
        r = re.compile(
            rf"{searchInput}", flags=re.I | re.X)

        results = soup.body.find_all(string=r, recursive=True)
        #print(results)

        dangerIndex = dangerIndex + len(results) * 50

        for s in results:
            s = s.lower()
            fire = 1 if s.find("požar", 0, len(s)) > 0 else 0
            flood = 1 if s.find("poplav", 0, len(s)) > 0 else 0
            war = 1 if s.find("rat", 0, len(s)) > 0 else 0
            virus = 1 if s.find("epidemij", 0, len(s)) + s.find("pandemij", 0, len(s)) > 0 else 0
            eq = 1 if s.find("zemljotre", 0, len(s)) > 0 else 0

            dangerIndex = dangerIndex + fire * 30 + flood * 50 + war * 100 + virus * 10 + eq * 30


    #print("************************")
    #print(searchInput + str(dangerIndex))
    #print("************************")
    # return (searchInput, dangerIndex)

    # requiredWords = r.findall(response.text)
    # print("\n----->URL: ", url)
    # for x in requiredWords:
    #    print(x)
    return dangerIndex

# ------------------------
if __name__ == "__main__":
    if len(sys.argv) == 5:
        print("Fali argument!")
        exit()

    argv = sys.argv

    allCities = sys.argv[1:]
    allDangerIndices = []
    for city in  allCities:
        searchInput = "" + city
        tmpDangerIndex = scrapSite(searchInput)
        allDangerIndices.append(tmpDangerIndex)

    for i in range(len(allDangerIndices)):
        print(allCities[i] + " : " + str(allDangerIndices[i]))








    # cityName = argv[1:]
    # cityName = "Pančevo"
    #cityName = "Beograd"
    # cityName = "Novi Sad"
    # cityName = "Niš"
    # cityName = "Vranje"
    #cityName = "Kragujev"
    #cityName = "Jagodin"
    # cityName = "Kruševac"
    #cityName = "Paraćin"
    #cityName = "Ćuprija"

'''
Beograd  250
Nis      200
Pancevo  50
Krusevac 50
Vranje   50
Kragujevac 50
Jagodina  0
Novi Sad 0
Cuprija  0 
Paracin  0

'''