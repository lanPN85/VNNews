# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class BTTSpider(TemplateSpider):
    name = "ttvh"
    allowed_domains = ["thethaovanhoa.vn"]
    filename = 'ttvh.txt'
    start_urls = [
        'http://thethaovanhoa.vn/bong-da-trong-nuoc-128ct0/trang-2.htm',
        'http://thethaovanhoa.vn/tay-ban-nha-151ct0/trang-2.htm',
        'http://thethaovanhoa.vn/bong-da-anh-149ct0/trang-2.htm',
        'http://thethaovanhoa.vn/duc-152ct0/trang-2.htm',
        'http://thethaovanhoa.vn/italia-150ct0/trang-2.htm',
        'http://thethaovanhoa.vn/champions-league-155ct0/trang-2.htm',
        'http://thethaovanhoa.vn/the-thao-158ct0/trang-2.htm',
        'http://thethaovanhoa.vn/van-hoa-giai-tri-133ct0/trang-2.htm',
        'http://thethaovanhoa.vn/xa-hoi-132ct0/trang-2.htm',
        'http://thethaovanhoa.vn/the-gioi-131ct0/trang-2.htm',
    ]
    url_prefix = 'http://thethaovanhoa.vn'
    page_suffix = '.htm'

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//div[@class = "ovh lst"]/ul/li/h3/a/@href').extract()
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
        title = response.xpath('//div[@class = "divContent"]/h1/text()').extract()
        content = response.xpath('//div[@id = "divcontentwrap"]/div/p/span/span/text()').extract()[1:]
        intro = []

        # Save content
        yield self.get_item(title, intro, content, response)
