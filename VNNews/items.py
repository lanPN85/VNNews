# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    url = scrapy.Field()
    count = scrapy.Field()
    referer = scrapy.Field()
    title = scrapy.Field()
    intro = scrapy.Field()
    content = scrapy.Field()
    domain = scrapy.Field()

    def __repr__(self):
        return ''
