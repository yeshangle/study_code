#! /usr/bin/env/python
#coding:utf-8
import requests
from bs4 import BeautifulSoup
import datetime
import xlsxwriter


class DataSpider(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
        }
        # 源网页
        self.url = 'http://www.job1001.com/SearchResult.php?page={0}&sums=&&parentName=&key=&region_1=&region_2=&region_3=&keytypes=&jtzw=%D2%BB%BC%B6%BD%A8%D4%EC%CA%A6&data=&dqdh_gzdd=&jobtypes=&edus=&titleAction=&provinceName=&sexs=&postidstr=&postname=&searchzwtrade=&gznum=&rctypes=&salary=&showtype=list&sorttype=score#main_search'

        self.qixin_url = "https://www.qixin.com/search?from=baidusem8&key={0}&page=1"
        # 用于存放爬取所有的获取的url
        self.spider_url = list()
        # 用于存储公司的信息以字典存储，value为列表由于公司名可能一样
        self.company_contend = dict()

    def spider_company_url(self):
        """用于获取公司简介的url"""

        for num in range(6):
            url = self.url.format(num)
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
            model['position_detail'] = "".join(new_list).strip().replace(u"举报", "")
            model['date'] = date_time
            all_commpany.append(model)
        # 将相同的公司名字的需求放在一个列表中
        for r in all_commpany:
            cp_name = r.get('company_name')
            print cp_name
            if cp_name not in self.company_contend:
                self.company_contend[cp_name] = list()
            self.company_contend[cp_name].append(r)
        return all_commpany
        # 以上完成将所有公司的数据存入self.company_contend中

    def write_excel(self, filename, headers=[], data = []):
        print(filename)
        # 创建一个Excel文件
        work = xlsxwriter.Workbook(filename)
        # 添加一个sheet
        cur_date = time.strftime("%Y-%m-%d", time.localtime())
        worksheet = work.add_worksheet(cur_date)

        # 设置表格属性
        colums = len(headers)
        # 设置表格的列宽
        worksheet.set_column(1, colums, 20)

        # 设置表格头部
        nrows = 0
        ncols = 0
        for i in range(colums):
            worksheet.write(nrows, ncols + i, headers[i])
        # 写入数据
        nrows = nrows + 1
        for d in data:
            company_name = d['company_name']
            position = d['position']
            position_detail = d['position_detail']
            tel = d.get('telephon_num', 0)
            date = d['date']

            worksheet.write(nrows, ncols + 0, date)
            worksheet.write(nrows, ncols + 1, company_name)
            worksheet.write(nrows, ncols + 2, position)
            worksheet.write(nrows, ncols + 3, position_detail)
            worksheet.write(nrows, ncols + 4, tel)
            nrows = nrows + 1

        work.close()

    def get_company_number(self):
        # 首先获取所有的公司名字
        # cp_name_list = self.company_contend.keys()
        # for name in cp_name_list:
        #     url = self.qixin_url.format(name)
        #     print url + "\n"
        url = "https://www.qixin.com/search?from=baidusem8&key=广东建邦兴业集团有限公司&page=1"
        headers = {
            # '8fdc2cbcd4825a0e7899': "f91575a11717935114dfc97b7fb86042b5e71825cab7c690d1fdf145d6a0a1ae24391912dc6f899d86c0cc6a2979ea54ca5fb7928886e89425c22a341ea3e73a",
            # 'accept': "application/json, text/plain, */*",
            # 'accept-encoding': "gzip, deflate, br",
            # 'accept-language': "zh-CN,zh;q=0.9",
            # 'connection': "keep-alive",
            # 'content-length': "118",
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cookie': "acw_tc=707c9f9815685596523042673e110f54e17f3dcee76b21dd7f381dd2da1564; channel=%2Bbaidusem17; Hm_lvt_52d64b8d3f6d42a2e416d59635df3f71=1568559652,1569077261,1569077433,1569126570; cookieShowLoginTip=3; sid=s%3ANWf53ulR5wza2PQlrc1nTarSDuKbDY2E.9Jd3i3SRHQFZjuHhcS7EZbhdHhEVRmh%2BDa3tJi%2FJHfY; Hm_lpvt_52d64b8d3f6d42a2e416d59635df3f71=1569144476",
            'host': "www.qixin.com",
            'origin': "https://www.qixin.com",
            'referer': "https://www.qixin.com/search?from=baidusem8&key=%E5%B9%BF%E4%B8%9C%E5%BB%BA%E9%82%A6%E5%85%B4%E4%B8%9A%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&page=1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            # 'x-requested-with': "XMLHttpRequest",
            # 'cache-control': "no-cache",
            # 'postman-token': "fd093e9b-9a1a-41dc-ade1-c60b7d231730"
        }

        res = requests.get(url.split('\n')[0], headers=headers)

        print res.content
        # from selenium import webdriver
        # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        #
        # # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # # dcap['phantomjs.page.settings.userAgent'] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36")
        #
        # url = "https://www.qixin.com/search?from=baidusem8&key=广东建邦兴业集团有限公司&page=1"
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # option.add_argument('no-sandbox')
        # option.add_argument('disable-dev-shm-usage')
        # browser = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=option)
        # # browser = webdriver.PhantomJS(desired_capabilities=dcap)
        # browser.get(url)
        # data = browser.page_source
        # browser.save_screenshot('1.png')
        # print data
        # browser.quit()








    def run(self):
        headers = [u'日期', u'公司', u'职位', u'职责详情', u'电话']
        # self.spider_company_url()
        company_data = self.spider_apllication_data()

        self.write_excel(u"公司信息.xlsx", headers, company_data)
        # self.get_company_number()
        # self.get_company_number()


if __name__ == "__main__":
    DataSpider().run()






