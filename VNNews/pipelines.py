# -*- coding: utf-8 -*-
import mysql.connector as connector


class DBPipeline(object):
    def __init__(self):
        self.username = 'lanpn'
        self.password = 'serenity'
        self.host = 'localhost'
        self.db = 'news_store'
        self.conn = None

    def open_spider(self, spider):
        self.conn = connector.connect(host=self.host, user=self.username,
                                      password=self.password, database=self.db)

    def process_item(self, item, spider):
        if item['content'] == '' or spider.testing:
            return item

        query = "INSERT INTO `articles`(`url`, `referer`, `title`, `intro`, `content`, `domain`)" \
                "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
                (item['url'][:255], item['referer'][:255], item['title'], item['intro'], item['content'], item['domain'])
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            spider.crawl_count += 1
            spider.log('Committed to MySQL [%d]' % spider.crawl_count)
        except connector.Error as err:
            self.conn.rollback()
            spider.log(err)
        return item

    def close_spider(self, spider):
        self.conn.close()


class TxtPipeline(object):
    fn = None

    def open_spider(self, spider):
        self.fn = file(spider.filename, mode='wt',
                       buffering=1)

    def process_item(self, item, spider):
        if item['content'] != '':
            self.fn.write('\n'.encode('utf-8').join([item['title'], item['intro'], item['content'], '***\n'.encode('utf-8')]))
        return item

    def close_spider(self, spider):
        self.fn.close()
