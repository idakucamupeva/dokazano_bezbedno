import sys
import re
import requests
from collections import deque
import bs4

def scrapSite(searchInput):
    urls = [
        # ----------------------------------------------------------Portali
        'https://www.blic.rs/vanredno-stanje',
        'https://rs.n1info.com/tag/vanredno-stanje/',
        'https://nova.rs/tag/vanredno-stanje/'
        'https://www.juznevesti.com/Tagovi/vanredno-stanje.sr.html'

        # ----------------------------------------------------------Regioni
        'https://akv.org.rs/category/vanredno-stanje/?script=lat',
        'http://www.rtvsumadija.com/tag/vanredno-stanje/'
         #'https://www.juznevesti.com/Tagovi/vanredno-stanje.sr.html',
    ]

    unscraped = deque(urls)
    scraped = set()
    dangerIndex = 0

    while len(unscraped):
        url = unscraped.popleft()
        scraped.add(url)

        #print("Crawling URL %s" % url)
        try:
            response = requests.get(url)
            #print("Successful request!")
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            print("Unsuccessful request!")
            continue

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # r = re.compile(
        #    rf"{searchInput}|(\bvanredno stanje\b)|(\bpožar\b)|(\bzemljotres\b)|(\bpoplava\b)|(\brat\b)|(\bepidemija\b)|(\bpandemija\b)|(\bprirodna katastrofa\b)",
        #    flags=re.I | re.X)
        # r = re.compile(rf"^.*?{searchInput}.*?\bvanredno stanje\b.*?\bpožar\b.*?\bzemljotres\b.*?\bpoplava\b.*?\brat\b.*?\bepidemija\b.*?\bpandemija\b.*?\bprirodna katastrofa\b.*?$", flags= re.I | re.X)
        # r = re.compile(rf".*?{searchInput}.*?(\bvanredno stanje\b).*?", flags= re.I | re.X)
        r = re.compile(
            rf"{searchInput}", flags=re.I | re.X)

        results = soup.body.find_all(string=r, recursive=True)
        dangerIndex = dangerIndex + len(results) * 50

        for s in results:
            s = s.lower()
            fire = 1 if s.find("požar", 0, len(s)) > 0 else 0
            flood = 1 if s.find("poplav", 0, len(s)) > 0 else 0
            war = 1 if s.find("rat", 0, len(s)) > 0 else 0
            virus = 1 if s.find("epidemij", 0, len(s)) + s.find("pandemij", 0, len(s)) > 0 else 0
            eq = 1 if s.find("zemljotre", 0, len(s)) > 0 else 0

            dangerIndex = dangerIndex + fire * 30 + flood * 50 + war * 100 + virus * 10 + eq * 30

    return dangerIndex

# ------------------------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Fale argumenti!")
        exit()

    allCities = sys.argv[1:]
    allDangerIndices = []

    for i in range(len(allCities)):
        searchInput = "" + allCities[i]

        # The only city in Serbia that is translated into English
        if searchInput == "Belgrade":
            searchInput = "Beograd"

        # Case where city has two words in its name
        index = searchInput.find('_', 0, len(searchInput))
        if index > 0:
            searchInput = searchInput[:index] + " " + searchInput[index + 1:]
            allCities[i] = searchInput  # for output

        tmpDangerIndex = scrapSite(searchInput)
        allDangerIndices.append(tmpDangerIndex)

    # print(sys.argv)
    # print("Broj gradova: ",  str(len(sys.argv)-1))
    bezbedno = " je potpuno BEZBEDAN"
    srednje = " je prohodan uz dodatni OPREZ"
    uzas = " treba IZBEGAVATI"
    for i in range(len(allDangerIndices)):
        if (allDangerIndices[i] < 50):
            print("Grad " + allCities[i] + bezbedno + '(' + str(allDangerIndices[i]) + ')')
        elif (allDangerIndices[i] >= 50 and allDangerIndices[i] < 200):
            print("Grad " + allCities[i] + srednje + '(' + str(allDangerIndices[i]) + ')')
        else:
            print("Grad " + allCities[i] + uzas + '(' + str(allDangerIndices[i]) + ')')


    # Tests
    # cityName = "Pančevo"
    # cityName = "Beograd"
    # cityName = "Novi Sad"
    # cityName = "Niš"
    # cityName = "Vranje"
    # cityName = "Kragujev"
    # cityName = "Jagodin"
    # cityName = "Kruševac"
    # cityName = "Paraćin"
    # cityName = "Ćuprija"