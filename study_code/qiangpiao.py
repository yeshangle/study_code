# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # 期望的条件
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from lxml import etree


class qiangpiao(object):

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path="/home/ubuntu/Download/chromedriver", chrome_options=self.options)
        self.initmy_url = 'https://www.damai.cn/'
        self.search_url = 'https://search.damai.cn/search.html?keyword=&spm=a2oeg.home.searchtxt.dsearchbtn2'
        self.login_url = 'https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F'

    def wait_input(self):
        self.name = input('演出名和地点（输入吴亦凡 重庆）：')
        # self.time = input('几号（如：18）：')
        self.changci = input('场次时间（输入2019-05-25 周六 19:00）：')
        self.price = input('票价（输入：看台1380元）：')
        # self.number = input('票数（如：1）：')
        self.people = input('购票者：（如有多个车次使用英文逗号分割）').split(',')

    def login(self):
        self.driver.get(self.login_url)  # 打开登录界面

        WebDriverWait(self.driver, 1000).until(EC.url_to_be(self.initmy_url))
        print('恭喜您，您已登录成功了！')

    def order_ticket(self):
        self.driver.get(self.search_url)
        inputtag = self.driver.find_element_by_class_name('input-search')
        inputtag.send_keys(self.name)

        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.CLASS_NAME, "input-search"), self.name))

        searchBotton = self.driver.find_element_by_class_name("btn-search")
        searchBotton.click()

        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, ".//img[@alt = '项目图片']")))
        second_url = self.driver.find_element_by_xpath(".//img[@alt = '项目图片']")
        second_url.click()

        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, ".//div[@class = 'cover']")))

        while True:
            judge = self.driver.find_elements_by_class_name("buybtn")[0]
            if "即将开抢" in judge.text:
                self.driver.refresh()
            else:
                break

        #场次选择
        time_list = self.driver.find_elements_by_xpath(
            ".//div[@class = 'select_right_list']/div[@class='select_right_list_item']/span | .//div[@class = 'select_right_list']/div[@class='select_right_list_item active']/span")
        for time in time_list:
            choice1 = time.text
            if choice1 in self.changci:
                time.click()

        price_list = self.driver.find_elements_by_xpath(
            ".//div[@class = 'select_right_list']/div[@class='select_right_list_item sku_item']/div | .//div[@class = 'select_right_list']/div[@class='select_right_list_item sku_item active']/div")
        for price in price_list:
            choice2 = price.text
            if choice2 in self.price:
                self.driver.execute_script("arguments[0].click();", price)

        #这一段是选择 票数
        # number_btn = self.driver.find_element_by_xpath(
        #     '//input[@class="cafe-c-input-number-input"]'
        # )
        # number_btn.clear()
        # number_btn.send_keys(self.number)


        self.driver.execute_script("arguments[0].click();", judge)


        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, ".//div[@class = 'ticket-buyer-select']")))
        consumers = self.driver.find_elements_by_xpath(
            ".//div[@class = 'next-col buyer-list-item']/label/span[@class='next-checkbox-label']")
        for consumer in consumers:
            consumer2 = consumer.text

            if consumer2 in self.people:
                consumer.click()   #单人
        #        self.driver.execute_script("arguments[0].click();", consumer) 多人

        paybtn = self.driver.find_element_by_xpath("//div[@class='submit-wrapper']/button")
        self.driver.execute_script("arguments[0].click();", paybtn)


    def run(self):
        self.wait_input()
        self.login()
        self.order_ticket()

if __name__ == '__main__':
    spider = qiangpiao()
    spider.run()
