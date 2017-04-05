# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class TNSpider(TemplateSpider):
    name = "thanhnien"
    allowed_domains = ["thanhnien.vn"]
    filename = 'files/thanhnien.txt'

    url_prefix = 'http://thanhnien.vn'
    page_suffix = '.html'
    start_urls = [
        'http://thanhnien.vn/thoi-su/trang-2.html',
        'http://thanhnien.vn/the-gioi/trang-2.html',
        'http://thanhnien.vn/van-hoa/trang-2.html',
        'http://thanhnien.vn/doi-song/trang-2.html',
        'http://thanhnien.vn/kinh-doanh/trang-2.html',
        'http://thanhnien.vn/gioi-tre/trang-2.html',
        'http://thanhnien.vn/giao-duc/trang-2.html',
        'http://thanhnien.vn/cong-nghe/trang-2.html',
        'http://thanhnien.vn/suc-khoe/trang-2.html',
    ]

    def parse(self, response):
        page = response.url

        # Retrieve article links
        links = response.xpath('//a[@class = "title"]/@href').extract()
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
        # Get text content
        title = response.xpath('//h1[@class = "main-title cms-title"]/text()').extract()
        intro = response.xpath('//div[@id = "chapeau"]/text()').extract()
        content = response.xpath('//div[@id = "abody"]/div/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)
