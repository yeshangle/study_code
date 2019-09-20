#! /usr/bin/env/python
#coding:utf-8
import requests
from bs4 import BeautifulSoup
import datetime


class DataSpider(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
        }
        # 源网页
        self.url_list = [
            'http://www.job1001.com/SearchResult.php?page=0&sums=&&parentName=&key=&region_1=&region_2=&region_3=&keytypes=&jtzw=%D2%BB%BC%B6%BD%A8%D4%EC%CA%A6&data=&dqdh_gzdd=&jobtypes=&edus=&titleAction=&provinceName=&sexs=&postidstr=&postname=&searchzwtrade=&gznum=&rctypes=&salary=&showtype=list&sorttype=score#main_search'
        ]
        # 用于存放爬取所有的获取的url
        self.spider_url = list()

    def spider_company_url(self):
        """用于获取公司简介的url"""

        for url in self.url_list:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'gb2312'
            soup = BeautifulSoup(res.content)
            result = soup.find_all(attrs={"class": "search_result"})
            now_day = datetime.datetime.now()
            cur_datetime = datetime.datetime(now_day.year, now_day.month, now_day.day)
            for i in result:
                str_date = i.find(attrs={"class": "search_date"}).string
                new_datetime = datetime.datetime.strptime(str_date, '%Y-%m-%d')
                day = (cur_datetime - new_datetime).days
                if day > 1:
                    continue
                url = i.find(attrs={"class": "search_post"}).a.get('href')
                self.spider_url.append(url)

    def spider_apllication_data(self):
        """
        用于获取公司名字和招聘信息.......
        :return:
        """
        url = ['http://www.lqjob88.com/jobs/52961392.html']
        res = requests.get(url[0], headers=self.headers)
        res.encoding = 'gb2312'
        soup = BeautifulSoup(res.content)
        # 公司名称
        company_name = soup.find(attrs={"class": "company_name"}).span['title']
        # 职位
        position_name = soup.find(attrs={"class": "job_post_name"}).a['title']
        # 职位要求
        order_list = list()
        opsition_info = soup.find_all(attrs={"class": "job_depict"})
        result = opsition_info.get_text()

        print company_name, position_name, result

if __name__ == "__main__":
    DataSpider().spider_apllication_data()






