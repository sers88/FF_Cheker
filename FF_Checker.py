import re
import requests

check_lists = list()
separ_newline = '\n'
with open('bookmarks.html', 'r', encoding='utf8') as file:
    out_file = file.read()
links_list = list(out_file.split(separ_newline))#преобразую из хтмла в список
print(links_list)
comp = re.compile(r'((http|https)://[A-Za-z0-9\.\?\&_\s=/-]+)')
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
            req = requests.request('GET', value, timeout=10)# allow_redirects=False на всякий случай
            if req.status_code >= 200 and req.status_code < 300:
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
        except requests.ConnectionError:
            del links_list[idx]
            print("Error delete ",value)
        except requests.exceptions.Timeout:
            print("Error time")
print(links_list)