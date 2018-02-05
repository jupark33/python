# Web crawling, naver 페이지 html 파싱
import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
r = http.request('GET', 'http://naver.com')

soup = BeautifulSoup(r.data)
print(b'r.date : ' + r.data)

print('[title]')
print(soup.title)

ah_k = soup.find_all('span', {'class':"ah_k"})

print(ah_k)
print(type(ah_k))

# 성공 <span class="ah_k">집행유예</span> -> "집행유예"
for i in ah_k:
    print(i.get_text())
