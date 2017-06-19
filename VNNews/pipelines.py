# -*- coding: utf-8 -*-
from spiders.TemplateSpider import TemplateSpider


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
