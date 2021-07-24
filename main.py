import requests
from aiohttp import ClientSession, TCPConnector
import asyncio
import datetime
import logging
from bs4 import BeautifulSoup, SoupStrainer
from sheets import SheetsHandler
from file_html import html1
import work_with_csv_sheet

logging.basicConfig(level=logging.DEBUG, filename='log_file', filemode='a', format='%(asctime)s -%(name)s - %(levelname)s - %(message)s')
PROXY = { 'https': 'http://wAuZRG:JMGrgQ@186.65.117.54:9690' }
# WITH_ADDITIONAL = ['https://skladchiki.com/forums/xobbi-i-rukodelie.73/','https://skladchiki.com/forums/zdorove.10/',
#                    'https://skladchiki.com/forums/foto.19/','https://skladchiki.com/forums/video.20/']
# #1st get all links with all catalog
# urls = []
# result = requests.get('https://skladchiki.com/#skladchikam-kursy.6', proxies=PROXY)
# only_script = SoupStrainer('div',{'class': 'block block--category block--category6 collapsible-nodes'})
# soup = BeautifulSoup(result.text, "html.parser", parse_only=only_script)
# print(soup.prettify())
# headers = soup.find_all("div", {"class": "node-main js-nodeMain"})
# for tag in headers:
#     url = 'https://skladchiki.com'+tag.find('a').attrs['href']
#     if url not in WITH_ADDITIONAL:
#         urls.append(url)
# #dond add from WITH_ADDITIONAL
# for i in WITH_ADDITIONAL:
#     result = requests.get(i, proxies=PROXY)
#     soup = BeautifulSoup(result.text, "html.parser")
#     headers = soup.find_all("div", {"class": "node-main js-nodeMain"})
#     for tag in headers:
#         url = 'https://skladchiki.com' + tag.find('a').attrs['href']
#         urls.append(url)



# #2nd usual
# query_handler = SheetsHandler()
# with requests.Session() as s:
#     urls = ['https://skladchiki.com/forums/psixologija.7/']
#     for url in urls:
#         #result = s.get(url, proxies=PROXY)
#         soup = BeautifulSoup(html1, "html.parser", )
#
#         page_count = soup.find('ul', {'class':'pageNav-main'})
#         page_count.find_all('li')
#         page_count = int(page_count.find_all('li').pop().text)
#
#         logging.info('В разделе %s\n%s страниц' % (url, page_count))
#
#         for i in range(page_count+1):
#             i = url+'page-{}'.format(i)
#             # #result = s.get(i, proxies=PROXY)
#             # #if result.status_code == 200:
#             logging.info('Парсю %s' % (i))
#             soup = BeautifulSoup(html1, "html.parser")
#
#             topics = soup.find_all('div',{'class':'structItem-title'})
#             for topic in topics:
#                 if topic.find("span", string="Доступно"):
#                     topic = topic.find('a',{'data-xf-init': 'preview-tooltip'}).text
#                     query_handler.query_add(topic)
#             #else: logging.error('Нет доступа к странице %s' % (i))
# 2nd usual
query_handler = SheetsHandler()
with requests.Session() as s:
    urls = ['https://skladchiki.com/forums/psixologija.7/']
    for url in urls:
        result = s.get(url, proxies=PROXY,timeout=30)
        soup = BeautifulSoup(result.text, "html.parser", )

        page_count = soup.find('ul', {'class': 'pageNav-main'})
        page_count.find_all('li')
        page_count = int(page_count.find_all('li').pop().text)

        logging.info('В разделе %s\n%s страниц' % (url, page_count))

        for i in range(page_count + 1):
            i = url + 'page-{}'.format(i)
            result = s.get(i, proxies=PROXY)
            if result.status_code == 200:
                logging.info('Парсю %s' % (i))
                soup = BeautifulSoup(result.text, "html.parser")
                rows = []
                topics = soup.find_all('div', {'class': 'structItem-title'})
                for topic in topics:
                    if topic.find("span", string="Доступно"):
                        topic = topic.find('a', {'data-xf-init': 'preview-tooltip'}).text
                        rows.append(topic)
                #query_handler.query_add(rows)
                work_with_csv_sheet.append_list_as_row(rows)
            else:
                logging.error('Нет доступа к странице %s' % (i))
