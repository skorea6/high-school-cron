from bs4 import BeautifulSoup
import pymysql
import requests

conn = pymysql.connect(host='DB 호스트', user='unjung', password='DB 비번', db='unjung', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)

unjung_main_url = 'http://unjung.hs.kr'

url = unjung_main_url + '/?act=board.list&code=1131&page=' + '1'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

trs = soup.find('div', {'class': 'boardListForm'}).find_all('a')
for tr in trs:
    if tr.get('href'):
        read_url = tr.get('href')
        if tr.select_one('strong'):
            print('공지 건너뜀')
        else:
            print(read_url)

            cursor.execute('SELECT COUNT(*) AS counter FROM board_notice WHERE duplicate_url = %s;', read_url)
            duplicate_result_1 = cursor.fetchone()['counter']

            if duplicate_result_1 == 0:  # 새로 업데이트 된 공지사항 게시글이 있을 경우
                url2 = unjung_main_url + read_url
                req2 = requests.get(url2)
                soup2 = BeautifulSoup(req2.content, 'html.parser')
                read_title = soup2.find('div', {'class': 'infoArea'}).find('dd', {'class': 'title'}).text
                read_name = soup2.find('dl', {'class': 'infoNext float_wrap'}).find_all('dd')[0].text
                read_date = soup2.find('dl', {'class': 'infoNext float_wrap'}).find_all('dd')[1].text
                read_content = soup2.find('div', {'class': 'boardReadBody'})

                print(read_title)
                print(read_name)
                print(read_date)
                print(read_content)

                cursor.execute(
                    'INSERT INTO board_notice (title, name, content, date, duplicate_url, full_url) VALUES (%s, %s, '
                    '%s, %s, %s, %s)', (read_title, read_name, read_content, read_date, read_url, url2))
            else:
                print('이미 등록된 게시물')
conn.commit()
