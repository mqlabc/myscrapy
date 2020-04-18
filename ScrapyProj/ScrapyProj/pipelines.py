# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy


class MxPipeline(object):
    def process_item(self, item, spider):
        return item


# from mysql
#
#
# class MysqlPipeline(object):
#     """将数据存入MySql"""
#
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host='localhost',
#             user='mql',
#             passwd='mql12345',
#             database="mx_db",
#             # buffered=True
#         )
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql1 = """
#         insert into show_star(star_name,star_url,star_portrait) values(%s,%s,%s);
#         """
#         self.cursor.execute(insert_sql1, (item['name'], item['url'], item['portrait']))
#         self.conn.commit()
#
#         # select_sql='select id from show_star where star_name="'+item['name']+'";'
#         # self.cursor.execute(select_sql)
#         # id=self.cursor.fetchone()[0]
#
#         insert_sql2 = """
#         insert into show_news(news_name,news_url,news_photo,star_name) values(%s,%s,%s,%s);
#         """
#         for news_name, news_url in zip(item['news_names'], item['news_urls']):
#             self.cursor.execute(insert_sql2, (news_name, news_url, news_name[:10] + '.jpg', item['name']))
#         self.conn.commit()
#
#     def close_spider(self, spider):
#         self.conn.close()


from scrapy.pipelines.files import FilesPipeline


class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        mx_name = request.meta.get('mx_name')
        file_name = request.meta.get('file_name')
        # 不用加后缀？
        return mx_name + '/' + file_name

    def get_media_requests(self, item, info):
        for file_url, news_name in zip(item['file_urls'], item['news_names']):
            # 通过meta传递给下面方法file_path
            yield scrapy.Request(file_url, meta={'mx_name': item['name'], 'file_name': news_name[:10] + '.jpg'})


class MysqlTwistedPipeline(object):
    pass

# from ?.models.es_types import StarBaikeType
# class ElasticSearchPipeline(object):
#     """将数据写入ES中"""
#     def process_item(self, item, spider):
#         star_baike_info = StarBaikeType()
#         star_baike_info.star_url = item['star_url']
#         star_baike_info.star_name = item['star_name']
#         star_baike_info.star_portrait = item['star_portrait']
#         # star_baike_info.baike_shot_loc = item['baike_shot_loc']
#         star_baike_info.star_hotness = item['star_hotness']
#         star_baike_info.star_summary = item['star_summary']

#         star_baike_info.save()
#         return item


# class EasyElasticSearchPipeline(object):
#     """将数据写入ES中"""
#     def process_item(self, item, spider):
#         item.save_to_es()
#         return item
