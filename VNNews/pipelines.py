# -*- coding: utf-8 -*-
import os

from VNNews.spiders.TemplateSpider import TemplateSpider


class CsvPipeline(object):
    def open_spider(self, spider):
        pass


class FastTextTrainPipeline(object):
    def open_spider(self, spider):
        self.path = './fastText/train.txt'
        self.fn = open(self.path, 'at')

    def process_item(self, item, spider):
        if item['content'] != '':
            self.fn.write('\n'.join([item['title'],
                                     item['intro'],
                                     item['content'],
                                     ''.encode('utf-8')]))
        spider.log('Saved to %s [%d]' % (self.path, item['count']))
        return item

    def close_spider(self, spider):
        self.fn.close()


class PlainContentPipeline(object):
    def open_spider(self, spider):
        self.path = os.path.join(TemplateSpider.directory, 'plain/vnnews.txt')
        self.fn = open(self.path, 'at', buffering=1)

    def process_item(self, item, spider):
        if item['content'] != '':
            self.fn.write(item['content'] + '\n')
        spider.log('Saved to %s [%d]' % (self.path, item['count']))
        return item

    def close_spider(self, spider):
        self.fn.close()


class TxtPipeline(object):
    def open_spider(self, spider):
        self.path = os.path.join(TemplateSpider.directory, 'text', spider.filename)
        self.fn = open(self.path, mode='wt', buffering=1)

    def process_item(self, item, spider):
        if item['content'] != '':
            self.fn.write('\n'.join([item['title'].decode('utf-8'),
                                     item['intro'].decode('utf-8'),
                                     item['content'].decode('utf-8'),
                                     '***\n']))
        spider.log('Saved to %s [%d]' % (self.path, item['count']))
        return item

    def close_spider(self, spider):
        self.fn.close()
