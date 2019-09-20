#! /usr/bin/env/python
#coding:utf-8
import requests
from bs4 import BeautifulSoup
import datetime
headers = {
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
}

url_list = [
'http://www.job1001.com/SearchResult.php?page=0&sums=&&parentName=&key=&region_1=&region_2=&region_3=&keytypes=&jtzw=%D2%BB%BC%B6%BD%A8%D4%EC%CA%A6&data=&dqdh_gzdd=&jobtypes=&edus=&titleAction=&provinceName=&sexs=&postidstr=&postname=&searchzwtrade=&gznum=&rctypes=&salary=&showtype=list&sorttype=score#main_search'
]
res = requests.get(url_list[0], headers=headers)
res.encoding = 'gb2312'
soup = BeautifulSoup(res.content)

result = soup.find_all(attrs={"class": "search_result"})

url_list = list()
now_day  = datetime.datetime.now()
cur_datetime = datetime.datetime(now_day.year, now_day.month, now_day.day)
for i in result:
    str_date = i.find(attrs={"class":"search_date"}).string
    new_datetime = datetime.datetime.strptime(str_date, '%Y-%m-%d')
    day = (cur_datetime - new_datetime).days
    if day > 1:
        continue
    url_list.append(i.find(attrs={"class":"search_post"}).a.get('href'))
