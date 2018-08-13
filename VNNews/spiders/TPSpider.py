# -*- coding: utf-8 -*-
import scrapy

from VNNews.spiders.TemplateSpider import TemplateSpider


class TPSpider(TemplateSpider):
    name = "tienphong"
    allowed_domains = ["tienphong.vn"]
    filename = 'tienphong.txt'

    start_urls = [
        'http://www.tienphong.vn/xa-hoi/trang2',
        'http://www.tienphong.vn/kinh-te/trang2',
        'http://www.tienphong.vn/the-gioi/trang2',
        'http://www.tienphong.vn/gioi-tre/trang2',
        'http://www.tienphong.vn/phap-luat/trang2',
        'http://www.tienphong.vn/the-thao/trang2',
        'http://www.tienphong.vn/van-nghe/trang2',
        'http://www.tienphong.vn/giai-tri/trang2',
        'http://www.tienphong.vn/giao-duc/trang2'
    ]

    def parse(self, response):
        page = response.url

        # Retrieve article links
        links = response.xpath('//h2[@class = "title"]/a/@href').extract()
        for link in links:
            url = link
            yield scrapy.Request(url=url, callback=self.parse_content)
        # Navigate to next page
        current_index = int(page.split('/')[-1][5:])
        next_index = current_index + 1
        if next_index <= self.page_limit + 1:
            page_prefix = page[:-(len(str(current_index)))]
            next_page = page_prefix + str(next_index)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Get text content
        title = response.xpath('//h1[@class = "cms-title"]/text()').extract()
        intro = response.xpath('//div[@class = "summary cms-desc"]/text()').extract()
        for i in xrange(0, len(intro)):
            intro[i] = intro[i][6:]  # Remove intro header
        content = response.xpath('//div[@id = "article-body"]/p/span/text()').extract()
        content.extend(response.xpath('//div[@id = "article-body"]/p/text()').extract())

        # Save content
        yield self.get_item(title, intro, content, response)
