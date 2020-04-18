# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名称不可随意，需与spider相同
    name = scrapy.Field()
    url = scrapy.Field()
    portrait = scrapy.Field()

    file_urls = scrapy.Field()
    news_urls = scrapy.Field()
    news_names = scrapy.Field()


class GeneralItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名称不可随意，需与spider相同
    url = scrapy.Field()
