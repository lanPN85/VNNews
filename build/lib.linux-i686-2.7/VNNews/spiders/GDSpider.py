# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class GDSpider(TemplateSpider):
    name = "gdn"
    allowed_domains = ["giadinh.net.vn"]
    filename = 'files/gdn.txt'
    start_urls = [
        'http://giadinh.net.vn/xa-hoi/trang-2.htm',
        'http://giadinh.net.vn/gia-dinh/trang-2.htm',
        'http://giadinh.net.vn/song-khoe/trang-2.htm',
        'http://giadinh.net.vn/giai-tri/trang-2.htm',
        'http://giadinh.net.vn/phap-luat/trang-2.htm',
        'http://giadinh.net.vn/an/trang-2.htm',
        'http://giadinh.net.vn/vong-tay-nhan-ai/trang-2.htm',
        'http://giadinh.net.vn/thi-truong/trang-2.htm',
        'http://giadinh.net.vn/bon-phuong/trang-2.htm',
    ]
    url_prefix = 'http://giadinh.net.vn'
    page_suffix = '.htm'

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//div[@class = "showlist"]/ul/li/h4/a/@href').extract()
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
        title = response.xpath('//div[@class = "title-detail"]/h1/text()').extract()
        intro = response.xpath('//h2[@class = "detail-sp"]/text()').extract()
        content = response.xpath('//div[@class = "content-new clear"]/p/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)
