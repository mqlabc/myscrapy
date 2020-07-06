# -*- coding: utf-8 -*-
import scrapy
from ScrapyProj.items import MxItem


class MxinfoSpider(scrapy.Spider):
    name = 'general'
    allowed_domains = ['www.mingxing.com']
    start_urls = ['http://www.mingxing.com/ziliao/index.html']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'ScrapyProj.middlewares.RandomUserAgentMiddleware': 10,
        },
        'ITEM_PIPELINES': {
            # 'ScrapyProj.pipelines.MysqlPipeline': 300,
            # 自己写的pipeline（继承FilesPipeline），值必须为1
            # 下载经常失败，然后会不断重试，比较浪费时间
            'ScrapyProj.pipelines.MyFilesPipeline': 1,
        },
        # 在项目目录（有cfg文件的目录）创建images文件夹
        'FILES_STORE': './images',
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response):
        response.body.decode('utf-8')
        for href in response.xpath('//div[@class="page_starlist"]/ul/li/a/@href').getall():
            star_index = href
            yield scrapy.Request(response.urljoin(star_index), callback=self.parse_star)
        next_page_url = response.xpath('//a[@class="nt"][2]/@href')
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url.get()), self.parse)

    def parse_star(self, response):
        response.body.decode('utf-8')
        star_info = MxItem()
        star_info['name'] = response.xpath(
            '//span[@class="name"]/h3/text()').get()
        star_info['url'] = response.url
        star_info['portrait'] = response.xpath(
            '//span[@class="photo"]/img/@src').get()

        star_info['file_urls'] = response.xpath(
            '//ul[@class="list"]/li/a/span/img/@src').getall()
        star_info['news_names'] = response.xpath(
            '//ul[@class="list"]/li/span/a/h3/text()').getall()
        star_info['news_urls'] = response.xpath(
            '//ul[@class="list"]/li/span/a/@href').getall()
        print(star_info)
        yield star_info
