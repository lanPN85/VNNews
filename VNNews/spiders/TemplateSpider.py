# -*- coding: utf-8 -*-
import scrapy

from VNNews import crawl_limit
from VNNews.items import Article


class TemplateSpider(scrapy.Spider):
    page_limit = 1
    crawl_count = 0
    filename = None
    testing = False
    allowed_domains = ['//no domain']
    directory = './'

    def __init__(self, name=None, **kwargs):
        super(TemplateSpider, self).__init__(name, **kwargs)
        self.page_limit = crawl_limit.limit.get(self.name, 1)

    def parse(self, response):
        raise NotImplementedError()

    def parse_content(self, response):
        raise NotImplementedError()

    def get_item(self, title, intro, content, response):
        title, intro, content = ' '.join(title).strip(), ' '.join(intro).strip(), ' '.join(content).strip()
        url = response.url
        referer = response.request.headers.get('Referer', None)
        self.crawl_count += 1
        article = Article(title=title.encode('utf-8'), intro=intro.encode('utf-8'), content=content.encode('utf-8'),
                          url=url, referer=referer, domain=self.allowed_domains[0], count=self.crawl_count)
        return article
