import requests
from faker import Faker
from bs4 import BeautifulSoup
import sys

fake = Faker()
headers = {'user-agent':fake.user_agent()}
response = requests.get('http://spys.one/free-proxy-list/CZ/', headers=headers )
parse_spys = BeautifulSoup(response.content, features="html.parser")
proxies_list = parse_spys.findAll("font", {'class':'spy14'})
for proxy in proxies_list:
    print(proxy.get_text())