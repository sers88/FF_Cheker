import re
import requests
from faker import Faker

fake = Faker()
headers = {'user-agent':fake.user_agent()}
check_lists = list()
proxies = {'http':'http://176.74.140.5:57476'}
separ_newline = '\n'
with open('bookmarks.html', 'r', encoding='utf8') as file:
    in_file = file.read()
links_list = list(in_file.split(separ_newline))#преобразую из хтмла в список
comp = re.compile(r'((http|https)://[A-Za-z0-9\.\?\&_\s=/-]+)')#доработать!! не воспринимает русские ссылки и пробелы
for box_str in links_list:
    link_n = comp.search(box_str)#извлекает из списка регулярным выражением ссылки
    if link_n:
        check_lists.append(link_n.group())
    else:
        check_lists.append(' ')
for idx, value in enumerate(check_lists):
    if ' ' in value:
        continue
    else:
        try:
            req = requests.request('GET', value, timeout=10, proxies=proxies, headers=headers)# allow_redirects=False на всякий случай!
            if req.status_code >= 200 and req.status_code < 300:#проверка ссылок
                continue
            elif req.status_code >= 300 and req.status_code < 400:
                print("3xx возможна блокировка ", value)
            elif req.status_code == 401:
                print("проверить 401 ", idx,"  ",value)
            elif req.status_code >= 400 and req.status_code < 500:
                del links_list[idx]
                print("delete ", value)
            elif req.status_code >= 500:
                print("ошибка сервера ", req.status_code, " ", idx, " ",value)
            else:
                print("unknow error", value)
        except requests.ConnectionError:
            del links_list[idx]
            print("Error delete ", value)
        except requests.exceptions.Timeout:
            print("Error time", value)
out_file = separ_newline.join(links_list)
with open('bookmarks2.html', 'wt', encoding='utf8') as file:
    file.write(out_file)
