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
        mm = "./test.html"
        self.log("mm is %s" % mm)
        return mm

    def parse(self, response):
        filename = "yilan.html"
        with open(filename, 'w') as f:
            f.write(response.body)
        self.log("保存文件：%s" % filename)

