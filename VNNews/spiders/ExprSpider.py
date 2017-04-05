# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class ExprSpider(TemplateSpider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    page_suffix = '.html'
    filename = 'files/vnexpress.txt'
    start_urls = [
        'http://vnexpress.net/tin-tuc/the-gioi/page/1.html',
        'http://kinhdoanh.vnexpress.net/page/1.html',
        'http://giaitri.vnexpress.net/page/1.html',
        'http://vnexpress.net/tin-tuc/phap-luat/page/1.html',
        'http://vnexpress.net/tin-tuc/giao-duc/page/1.html',
        'http://suckhoe.vnexpress.net/page/1.html',
        'http://vnexpress.net/tin-tuc/khoa-hoc/page/1.html',
        'http://sohoa.vnexpress.net/page/1.html',
        'http://vnexpress.net/tin-tuc/oto-xe-may/page/1.html',
    ]

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//a[@class = "txt_link"]/@href').extract()
        for link in links:
            url = link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        page_index = int(page.split("/")[-1].split('.')[0])
        next_index = page_index + 1
        if next_index <= self.page_limit:
            page_prefix = page[:-(len(str(page_index)) + len(self.page_suffix))]
            next_page = page_prefix + str(next_index) + self.page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Scrape content
        title = response.xpath('//div[@class = "title_news"]/h1/text()').extract()
        intro = response.xpath('//h3[@class = "short_intro txt_666"]/text()').extract()
        content = response.xpath('//p[@class = "Normal"]/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)
