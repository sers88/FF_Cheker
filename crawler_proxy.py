import requests
from faker import Faker
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import re
import time

check_ip = list()
options = webdriver.FirefoxOptions()
options.set_headless(headless=True)#disable GUI Firefox
driver = webdriver.Firefox(executable_path='geckodriver.exe')
driver.get('http://spys.one/free-proxy-list/CZ/')
time.sleep(2)
driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/font/select[1]/option[6]").click()# add 500 proxy on site
fake = Faker()
time.sleep(2)
regx_ip_re = re.compile(r'\d+\.\d+\.\d+\.\d+')
regx_port_re = re.compile(r'(\d\d\d\d\d|\d\d\d\d)')
headers = {'user-agent':fake.user_agent()}
#response = requests.get('http://spys.one/free-proxy-list/CZ/', headers=headers )
parse_spys = BeautifulSoup(driver.page_source, features="html.parser")
driver.quit()
proxies_list = parse_spys.findAll("font", {'class':'spy14'})
for proxy in proxies_list:
    regx_ip = regx_ip_re.search(proxy.get_text())
    regx_port = regx_port_re.search(proxy.get_text())
    if (regx_ip and regx_port):
        check_ip.append(regx_ip.group()+':'+regx_port.group())
    else:
        continue
for ip in check_ip:
    t = time.time()
    proxies = {'http':'http://'+ip}
    req = requests.request('GET', "https://www.google.com/", timeout=10, proxies=proxies, headers=headers)
    if req.status_code >= 200 and req.status_code < 300:#проверка ссылок
        print(ip + "   OK")
        b = time.time()
        print(b-t)
    else:
        check_ip.remove(ip)
        print(ip + ' Delete')
        b = time.time()
        print(b-t)