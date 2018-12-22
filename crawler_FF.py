import requests
from faker import Faker
from bs4 import BeautifulSoup
import sys
from selenium import webdriver

options = webdriver.FirefoxOptions()
options.set_headless(headless=True)#disable GUI Firefox
driver = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
driver.get('http://spys.one/free-proxy-list/CZ/')
fake = Faker()
#headers = {'user-agent':fake.user_agent()}
#response = requests.get('http://spys.one/free-proxy-list/CZ/', headers=headers )
parse_spys = BeautifulSoup(driver.page_source, features="html.parser")
proxies_list = parse_spys.findAll("font", {'class':'spy14'})
for proxy in proxies_list:
    print(proxy.get_text())