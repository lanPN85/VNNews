# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class BTTSpider(TemplateSpider):
    name = "btt"
    allowed_domains = ["baotintuc.vn"]
    filename = 'files/btt.txt'
    start_urls = [
        'http://baotintuc.vn/thoi-su-472ct0/trang-2.htm',
        'http://baotintuc.vn/the-gioi-130ct0/trang-2.htm',
        'http://baotintuc.vn/kinh-te-128ct0/trang-2.htm',
        'http://baotintuc.vn/xa-hoi-129ct0/trang-2.htm',
        'http://baotintuc.vn/phap-luat-475ct0/trang-2.htm',
        'http://baotintuc.vn/giao-duc-135ct0/trang-2.htm',
        'http://baotintuc.vn/ho-so-133ct0/trang-2.htm',
        'http://baotintuc.vn/quan-su-514ct0/trang-2.htm',
        'http://baotintuc.vn/the-thao-273ct0/trang-2.htm',
        'http://baotintuc.vn/van-hoa-158ct0/trang-2.htm',
        'http://baotintuc.vn/khoa-hoc-cong-nghe-131ct0/trang-2.htm',
        'http://baotintuc.vn/dan-toc-151ct0/trang-2.htm',
        'http://baotintuc.vn/suc-khoe-564ct0/trang-2.htm',
    ]
    url_prefix = 'http://baotintuc.vn'
    page_suffix = '.htm'

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//div[@class = "listspecial"]/ul/li/h3/a/@href').extract()
        for link in links:
            url = self.url_prefix + link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-1].split('.')[0].split('-')[-1])
        next_index = current_index + 1
        if next_index <= self.page_limit + 1:
            page_prefix = page[:-(len(str(current_index)) + len(self.page_suffix))]
            next_page = page_prefix + str(next_index) + self.page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Scrape content
        title = response.xpath('//h1[@class = "title"]/text()').extract()
        intro = response.xpath('//h2[@id = "plhMain_NewsDetail1_divSapoLive"]/text()').extract()
        content = response.xpath('//div[@id = "plhMain_NewsDetail1_divContentLive"]/p/text()').extract()

        yield self.get_item(title, intro, content, response)
