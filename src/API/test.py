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

        requiredWords = set(re.findall(rf"{searchInput}|(vanredno stanje)|(požar)|(zemljotres)|(poplava)|(rat)|(epidemija)|(pandemija)|(prirodna katastrofa)", response.text, re.IGNORECASE))
        print(requiredWords)



        '''
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all("a"):
            if "href" in anchor.attrs:
                link = anchor.attrs["href"]
            else:
                link = ''

                if link.startswith('/'):
                    link = base_url + link

                elif not link.startswith('http'):
                    link = path + link

                if not link.endswith(".gz"):
                    if not link in unscraped and not link in scraped:
                        unscraped.append(link)



    # df = pd.DataFrame(emails, columns=["Email"]).
    # emails.add("info@ekologija.gov.rs");
    # print(df["Email"][0])
    vector_emails = []
    for e in emails:
        # print(e)
        vector_emails.append(e)

    vector_emails.append("info@ekologija.gov.rs")

    for e in vector_emails:
        print(e)
    '''





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
    cityName = "Kraljevo"
    searchInput = "" + cityName + " "

    googleSearch(searchInput)
