# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class DVSpider(TemplateSpider):
    name = "danviet"
    allowed_domains = ["danviet.vn"]
    filename = 'files/danviet.txt'
    url_prefix = 'http://danviet.vn'
    start_urls = [
        'http://danviet.vn/ajax/box_bai_viet_trang_chuyen_muc/index/1007/1/8/1/0/1/0',  # The-gioi
        'http://danviet.vn/ajax/box_bai_viet_trang_chuyen_muc/index/1001/1/8/1/0/1/0',  # General
        'http://danviet.vn/ajax/box_bai_viet_trang_chuyen_muc/index/1035/1/8/1/0/1/0',  # The-thao
        'http://danviet.vn/ajax/box_bai_viet_trang_chuyen_muc/index/1008/1/8/1/0/1/0',  # Phap-luat
        'http://danviet.vn/ajax/box_bai_viet_trang_chuyen_muc/index/1004/1/8/1/0/1/0',  # Kinh-te
        'http://danviet.vn/ajax/box_bai_viet_trang_chuyen_muc/index/1006/1/8/1/0/1/0',  # Van-hoa
        'http://danviet.vn/ajax/box_bai_viet_trang_chuyen_muc/index/1025/1/8/1/0/1/0',  # Giai-tri
        'http://danviet.vn/ajax/box_bai_viet_trang_chuyen_muc/index/1097/1/8/1/0/1/0',  # Du-lich
    ]

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//a[@class = "news-title18"]/@href').extract()
        for link in links:
            url = self.url_prefix + link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-6])
        next_index = current_index + 1
        if next_index <= self.page_limit:
            suffix_len = 0
            frags = page.split('/')
            for i in xrange(1, 6):
                suffix_len += 1 + len(frags[-i])
            page_suffix = page[-suffix_len:]
            page_prefix = page[:-(len(str(current_index)) + len(page_suffix))]
            next_page = page_prefix + str(next_index) + page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Article page

        # Scrape content
        title = response.xpath('//span[@class = "Bigtieudebaiviet"]/text()').extract()
        intro = response.xpath('//div[@class = "sapobaiviet"]/h3/text()').extract()
        content = response.xpath('//div[@class = "contentbaiviet"]/p/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)