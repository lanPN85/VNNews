# -*- coding: utf-8 -*-
import scrapy

from VNNews.spiders.TemplateSpider import TemplateSpider


class PLSpider(TemplateSpider):
    name = "pl"
    allowed_domains = ["plo.vn"]
    filename = 'pl.txt'
    start_urls = [
        'http://plo.vn/thoi-su/?trang=2',
        'http://plo.vn/phap-luat/?trang=2',
        'http://plo.vn/quoc-te/?trang=2',
        'http://plo.vn/an-ninh-trat-tu/?trang=2',
        'http://plo.vn/xa-hoi/?trang=2',
        'http://plo.vn/kinh-te/?trang=2',
        'http://plo.vn/bat-dong-san/?trang=2',
        'http://plo.vn/van-hoa-giai-tri/?trang=2',
        'http://plo.vn/the-thao/?trang=2',
        'http://plo.vn/do-thi/?trang=2',
    ]

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//p[@class = "title"]/a/@href').extract()
        for link in links:
            url = link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-1].split('=')[-1])
        next_index = current_index + 1
        if next_index <= self.page_limit + 1:
            page_prefix = page[:-(len(str(current_index)))]
            next_page = page_prefix + str(next_index)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Scrape content
        title = response.xpath('//h1[@class = "main-title cms-title"]/text()').extract()
        intro = response.xpath('//div[@id = "chapeau"]/div/text()').extract()
        for i in xrange(0, len(intro)):
            intro[i] = intro[i][6:]  # Remove intro header
        content = response.xpath('//div[@id = "abody"]/*/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)
