# -*- coding: utf-8 -*-
import scrapy

class MngYan(scrapy.Spider):
    """
    用于爬取相关数据
    """

    # 蜘蛛名字
    name = "mingyan"

    def start_requests(self):

        # 爬取的连接
        urls = [
            'http://lab.scrapyd.cn/page/1/',
            'http://lab.scrapyd.cn/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = "mingyan-%s.html" % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("保存文件：%s" % filename)

