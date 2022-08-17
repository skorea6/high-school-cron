from bs4 import BeautifulSoup
import pymysql
import requests

conn = pymysql.connect(host='DB 호스트', user='unjung', password='DB 비번', db='unjung', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)

unjung_main_url = 'http://unjung.hs.kr'


url = unjung_main_url + '/?act=lunch.main&month=12/01/2021'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

trs = soup.find(id="foodListArea").find_all('td')
for tr in trs:
    if tr.select_one('font') is not None:
        td_day = tr.select_one('font').text.strip()
        print(td_day)
        if tr.find('div', {'class': 'tabContent on'}):
            if tr.find('div', {'class': 'tabContent on'}).select_one('a'):
                td_content = tr.find('div', {'class': 'tabContent on'}).select_one('a').text.strip()
                print(td_content)

                now_date = "2021-12-" + str(td_day).zfill(2) + " 00:00:00"

                cursor.execute(
                    'INSERT INTO food_schedule (content, datetime) VALUES (%s, %s)',
                    (td_content, now_date))


conn.commit()
