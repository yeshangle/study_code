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

        mm = [scrapy.FormRequest('http://www.job1001.com/SearchResult.php',
                            formdata={'search_region': '地区不限', 'jtzw': '一级建造师'},
                            callback=self.parse)]
        self.log("mm is %s" % mm)
        return mm


    def parse(self, response):
        filename = "yilan.html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("保存文件：%s" % filename)

