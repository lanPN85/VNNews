# -*- coding: utf-8 -*-
try:
    import mysql.connector as connector
except ImportError:
    pass

from spiders.TemplateSpider import TemplateSpider


class MySQLPipeline(object):
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
            spider.log('Committed to MySQL [%d]' % item['count'])
        except connector.Error as err:
            self.conn.rollback()
            spider.log(err)
        return item

    def close_spider(self, spider):
        self.conn.close()


class TxtPipeline(object):

    def open_spider(self, spider):
        self.path = TemplateSpider.directory + spider.filename
        self.fn = file(self.path, mode='wt',
                       buffering=1)

    def process_item(self, item, spider):
        if item['content'] != '':
            self.fn.write('\n'.encode('utf-8').join([item['title'], item['intro'], item['content'], '***\n'.encode('utf-8')]))
        spider.log('Saved to %s [%d]' % (self.path, item['count']))
        return item

    def close_spider(self, spider):
        self.fn.close()
