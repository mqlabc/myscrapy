# -*- coding: utf-8 -*-
import re
import time
import scrapy
from ScrapyProj.items import GeneralItem
# The previously bundled scrapy.xlib.pydispatch library was deprecated and replaced by pydispatcher.
from pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver


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
        options = webdriver.ChromeOptions()

        # 减小被识别的概率
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

        # sougou微信平台可以识别headless模式，必要时不使用headless改用virtualdisplay
        # options.add_argument('--headless')
        display = Display(visible=0, size=(1366, 768))
        display.start()

        # 指定chrome目录:加载插件；保持登录
        chrome_options.add_argument(
            r"user-data-dir=C:\Users\mql\AppData\Local\Google\Chrome\User Data")

        self.driver = webdriver.Chrome(options=options)
        super(GeneralSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭浏览器
        print("Spider closed.")
        self.browser.quit()

    def parse(self, response):
        level2_pages = response.xpath(
            '//span[@class="articlename"]/a/@href').getall()
        for page in level2_pages:
            yield scrapy.Request('https://mooc1-1.chaoxing.com' + page, callback=self.parse_level2)
        pass

    def parse_level2(self, response):
        # 有必要try
        try:
            frames = response.headers['results'].decode()
            results = ['http://d0.ananas.chaoxing.com/download/' +
                       i for i in re.findall('objectid="(.*?)"', frames)]
            item = GeneralItem()
            # 注意key的名称
            item['url'] = results
            yield item
        except KeyError:
            pass
