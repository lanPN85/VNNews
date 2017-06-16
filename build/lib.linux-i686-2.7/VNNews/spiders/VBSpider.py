# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class VBSpider(TemplateSpider):
    name = "vietbao"
    filename = 'vietbao.txt'
    page_suffix = '/'
    allowed_domains = ["vietbao.vn"]
    start_urls = [
        'http://vietbao.vn/Chinh-Tri/p/2/',
        'http://vietbao.vn/The-gioi/p/2/',
        'http://vietbao.vn/Xa-hoi/p/2/',
        'http://vietbao.vn/Kinh-te/p/2/',
        'http://vietbao.vn/An-ninh-Phap-luat/p/2/',
        'http://vietbao.vn/Bong-da/p/2/',
        'http://vietbao.vn/The-gioi-giai-tri/p/2/',
        'http://vietbao.vn/The-gioi-tre/p/2/',
        'http://vietbao.vn/Doi-song-Gia-dinh/p/2/',
        'http://vietbao.vn/Suc-khoe/p/2/',
    ]

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//a[@class = "title-lg"]/@href').extract()
        for link in links:
            url = link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-2])
        next_index = current_index + 1
        if next_index <= self.page_limit + 1:
            page_prefix = page[:-(len(str(current_index)) + len(self.page_suffix))]
            next_page = page_prefix + str(next_index) + self.page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Scrape content
        title = response.xpath('//div[@class = "mod-title"]/h1/text()').extract()
        intro = response.xpath('//div[@id = "vb-content-detailbox"]/b/text()').extract()
        content = response.xpath('//div[@id = "vb-content-detailbox"]/p/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)
