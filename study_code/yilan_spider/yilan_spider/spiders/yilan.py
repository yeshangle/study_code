# -*- coding: utf-8 -*-
import scrapy

class MngYan(scrapy.Spider):
    """
    用于爬取相关数据
    """

    # 蜘蛛名字
    name = "yilan"

    def start_requests(self):

        # 爬取的连接
        urls = [
            'http: // www.job1001.com / SearchResult.php?page = 0 & sums = & & parentName = & key = & region_1 = & region_2 = & region_3 = & keytypes = & jtzw = % D2 % BB % BC % B6 % BD % A8 % D4 % EC % CA % A6 & data = & dqdh_gzdd = & jobtypes = & edus = & titleAction = & provinceName = & sexs = & postidstr = & postname = & searchzwtrade = & gznum = & rctypes = & salary = & showtype = list & sorttype = score'
        # main_search
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        filename = "yilan.html"
        with open(filename, 'w') as f:
            f.write(response.body)
        self.log("保存文件：%s" % filename)

