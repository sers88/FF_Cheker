from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bsp1 = BeautifulSoup(html, features="html.parser")
for name in bsp1.find("table", {"id":"giftList"}).tr.next_siblings:
    print(name)
