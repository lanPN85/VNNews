# -*- coding: utf-8 -*-

from spiders.TemplateSpider import TemplateSpider


class CsvPipeline(object):
    def open_spider(self, spider):
        pass


class FastTextTrainPipeline(object):
    def open_spider(self, spider):
        self.path = './fastText/train.txt'
        self.fn = file(self.path, mode='at',
                       buffering=1)

    def process_item(self, item, spider):
        if item['content'] != '':
            self.fn.write('\n'.encode('utf-8').join([item['title'],
                                                     item['intro'],
                                                     item['content'],
                                                     ''.encode('utf-8')]))
        spider.log('Saved to %s [%d]' % (self.path, item['count']))
        return item

    def close_spider(self, spider):
        self.fn.close()


class TxtPipeline(object):
    def open_spider(self, spider):
        self.path = TemplateSpider.directory + spider.filename
        self.fn = file(self.path, mode='wt',
                       buffering=1)

    def process_item(self, item, spider):
        if item['content'] != '':
            self.fn.write('\n'.encode('utf-8').join([item['title'],
                                                     item['intro'],
                                                     item['content'],
                                                     '***\n'.encode('utf-8')]))
        spider.log('Saved to %s [%d]' % (self.path, item['count']))
        return item

    def close_spider(self, spider):
        self.fn.close()
