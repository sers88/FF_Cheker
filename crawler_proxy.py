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
driver = webdriver.Firefox(executable_path='geckodriver.exe',options=options)
driver.get('http://spys.one/free-proxy-list/CZ/')
time.sleep(2)
driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/font/select[1]/option[6]").click()# add 500 proxy on site
fake = Faker()
time.sleep(10)
regx_ip_re = re.compile(r'\d+\.\d+\.\d+\.\d+')
regx_port_re = re.compile(r'(\d\d\d\d\d|\d\d\d\d)')
headers = {'user-agent':fake.user_agent()}
parse_spys = BeautifulSoup(driver.page_source, features="html.parser")
driver.quit()
proxies_list = parse_spys.findAll("font", {'class':'spy14'})
for proxy in proxies_list:#перебор по регулярке
    regx_ip = regx_ip_re.search(proxy.get_text())
    regx_port = regx_port_re.search(proxy.get_text())
    if (regx_ip and regx_port):
        check_ip.append(regx_ip.group()+':'+regx_port.group())
    else:
        continue
for ip in check_ip:#check proxy
    t = time.time()
    proxies = {'https':'https://'+ip}
    try:
        req_2 = requests.get("https://yandex.ru/robots.txt", timeout=10, proxies=proxies, headers=headers)
    except requests.ConnectTimeout:
        print(ip + ' ConnectTimeout Delete')
        check_ip.remove(ip)
        continue
    except requests.exceptions.ProxyError:
        print(ip + ' ProxyError Delete')
        check_ip.remove(ip)
        continue
    except requests.exceptions.SSLError:
        print(ip + ' SSLError Delete')
        check_ip.remove(ip)
        continue
    except requests.exceptions.ConnectionError:
        print(ip + ' ConnectionError Delete')
        check_ip.remove(ip)
        continue
    if req_2.status_code >= 200 and req_2.status_code < 300:#проверка ссылок
        b = time.time()
        if (b-t) > 3:
            print('Delete ' + ip + ' high timeout')
            print(str(b-t) + 's')
            check_ip.remove(ip)
            continue
        print(ip + "   OK")
        print(str(b-t) + 's')
    else:
        check_ip.remove(ip)
        print(ip + ' Delete')
        b = time.time()
        print(b-t)