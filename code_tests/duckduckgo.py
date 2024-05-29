from duckduckgo_search import DDGS

import bs4
import urllib.request


results = DDGS().text("current weather", max_results=3)
for result in results:
    webpage=str(urllib.request.urlopen(result['href']).read())
    soup = bs4.BeautifulSoup(webpage)   
    print(soup.get_text())