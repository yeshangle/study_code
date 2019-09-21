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

        self.qixin_url = "https://www.qixin.com/search?from=baidusem8&key={0}&page=1"
        # 用于存放爬取所有的获取的url
        self.spider_url = list()
        # 用于存储公司的信息以字典存储，value为列表由于公司名可能一样
        self.company_contend = dict()

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
        # 用于存储所有获取的公司信息
        all_commpany = list()
        # 用于存储单个公司的信息
        time = datetime.datetime.now()
        date_time = time.strftime("%Y-%m-%d")
        for url in self.spider_url:
            model = dict()
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html5lib')
            # 公司名称
            model['company_name'] = soup.find(name='div', attrs={"class": "company_name"}).get_text().split("\n")[1].strip().encode('utf-8')
            # # 职位
            model['position'] = soup.find(attrs={"class": "job_post_name"}).a['title']
            # # 职位要求
            positive_info = soup.find(name='div', attrs={"class": "job_depict"}).get_text().split(" ")
            result_list = [i.replace(" ", "") for i in positive_info]
            result_list_new = [r.replace("\n", "") for r in result_list]
            new_list = list()
            for r in result_list_new:
                index = 0
                if r.find(u'职位类别') != -1:
                    index = r.find(u'职位类别')
                if index:
                    r = r[:index]
                new_list.append(r)
            # 职位要求
            model['position_contend'] = "".join(new_list).strip().replace(u"举报", "")
            model['date'] = date_time
            all_commpany.append(model)
        # 将相同的公司名字的需求放在一个列表中
        for r in all_commpany:
            cp_name = r.get('company_name')
            print cp_name
            if cp_name not in self.company_contend:
                self.company_contend[cp_name] = list()
            self.company_contend[cp_name].append(r)

        # 以上完成将所有公司的数据存入self.company_contend中

    def get_company_number(self):
        # 首先获取所有的公司名字
        # cp_name_list = self.company_contend.keys()
        # for name in cp_name_list:
        #     url = self.qixin_url.format(name)
        #     print url + "\n"
        url = "https://www.qixin.com/search?from=baidusem8&key=广东建邦兴业集团有限公司&page=1"
        res = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'html5lib')

        result = soup.find_all(attrs={"class": "legal-person"})
        for i in result:
            print i








    def run(self):
        # self.spider_company_url()
        # self.spider_apllication_data()
        # self.get_company_number()
        self.get_company_number()


if __name__ == "__main__":
    DataSpider().run()






