# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class NDHSpider(TemplateSpider):
    testing = True
    name = "ndh"
    allowed_domains = ["ndh.vn"]
    filename = 'ndh.txt'
    start_urls = [
        'http://ndh.vn/Handler/Moredata.aspx?pageIndex=1&Cat_ID=4',  # Dau-tu
        'http://ndh.vn/Handler/Moredata.aspx?pageIndex=1&Cat_ID=6',  # Tieu-dung
    ]

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//li/div/h2/a/@href').extract()
        for link in links:
            url = link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-1].split('&')[0].split('=')[-1])
        next_index = current_index + 1
        if next_index <= self.page_limit:
            page_suffix = page[-9:]
            page_prefix = page[:-(len(str(current_index) + page_suffix))]
            next_page = page_prefix + str(next_index) + page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Scrape content
        title = response.xpath('//div[@class = "title-detail "]/h1/text()').extract()
        intro = response.xpath('//div[@class = "shapo-detail"]/text()').extract()
        for i in range(len(intro)):
            intro[i] = intro[i][7:]  # Remove intro header
        content = response.xpath('//div[@class = "main-detail"]/p/text()').extract()

        yield self.get_item(title, intro, content, response)
