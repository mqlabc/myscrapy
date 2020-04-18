# -*- coding: utf-8 -*-
import scrapy
import time
from ScrapyProj.items import GeneralItem
# The previously bundled scrapy.xlib.pydispatch library was deprecated and replaced by pydispatcher.
from pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re


class GeneralSpider(scrapy.Spider):
    name = 'general_with_browser'
    allowed_domains = ['mooc1-1.chaoxing.com']
    start_urls = [
        'https://mooc1-1.chaoxing.com/mycourse/studentcourse?courseId=207139123&clazzid=14311244&vc=1&cpi=102334520'
        '&enc=434ff33357b75fc268e18214a3ad212d']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'ScrapyProj.middlewares.DynamicPageMiddleware': 3,
            'ScrapyProj.middlewares.RandomUserAgentMiddleware': 1,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        chrome_options = Options()
        # 指定chrome目录
        # 加载插件；保持登录
        chrome_options.add_argument(r"user-data-dir=C:\Users\mql\AppData\Local\Google\Chrome\User Data")
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('window-size=1366,768')
        self.browser = webdriver.Chrome(options=chrome_options)
        # self.browser = webdriver.Chrome()
        super(GeneralSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭浏览器
        print("Spider closed.")
        self.browser.quit()

    def parse(self, response):
        level2_pages = response.xpath('//span[@class="articlename"]/a/@href').getall()
        for page in level2_pages:
            yield scrapy.Request('https://mooc1-1.chaoxing.com' + page, callback=self.parse_level2)
        pass

    def parse_level2(self, response):
        # 有必要try
        try:
            frames = response.headers['results'].decode()
            results = ['http://d0.ananas.chaoxing.com/download/' + i for i in re.findall('objectid="(.*?)"', frames)]
            item = GeneralItem()
            # 注意key的名称
            item['url'] = results
            yield item
        except KeyError:
            pass
