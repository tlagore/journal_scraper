# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
import json


class SpiderPipeline(object):
    def __init__(self, pgUser, pgPass, pgHost, pgDb, pgTable):
        self._connstr = "dbname='{}' user='{}' host='{}' password='{}'".format(pgDb, pgUser, pgHost, pgDb)
        self._table = pgTable
        print(self._connstr)
        self._conn = psycopg2.connect(self._connstr)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            pgUser = crawler.settings.get('PG_USER'),
            pgPass = crawler.settings.get('PG_PASS'),
            pgHost = crawler.settings.get('PG_HOST'),
            pgDb = crawler.settings.get('PG_DB'),
            pgTable = crawler.settings.get('PG_TABLE')
        )

    def process_item(self, item, spider):
        cursor = self._conn.cursor()

        extra_dets_json = json.dumps(item["extra_details"])
        keywords_arr = json.dumps(item["keywords"]).replace("[","{").replace("]","}")

        sql = """INSERT INTO journal (title,author,journal,doi,abstract,keywords,extradetails) VALUES 
                (%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (item["title"], item["author"], item["journal"], item["doi"], item["abstract"], keywords_arr, extra_dets_json))

        self._conn.commit()
        cursor.close()

        return item
