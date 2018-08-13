# -*- coding: utf-8 -*-
import scrapy

from VNNews.spiders.TemplateSpider import TemplateSpider


class VNNSpider(TemplateSpider):
    name = "vietnamnet"
    allowed_domains = ["vietnamnet.vn"]
    page_suffix = '/index.html'
    url_prefix = 'http://vietnamnet.vn'
    filename = 'vnn.txt'
    start_urls = [
        'http://vietnamnet.vn/vn/thoi-su/trang1/index.html',
        'http://vietnamnet.vn/vn/kinh-doanh/trang1/index.html',
        'http://vietnamnet.vn/vn/giai-tri/trang1/index.html',
        'http://vietnamnet.vn/vn/the-gioi/trang1/index.html',
        'http://vietnamnet.vn/vn/giao-duc/trang1/index.html',
        'http://vietnamnet.vn/vn/doi-song/trang1/index.html',
        'http://vietnamnet.vn/vn/phap-luat/trang1/index.html',
        'http://vietnamnet.vn/vn/the-thao/trang1/index.html',
        'http://vietnamnet.vn/vn/cong-nghe/trang1/index.html',
        'http://vietnamnet.vn/vn/suc-khoe/trang1/index.html',
    ]

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//li[@class = "item clearfix dotter"]/h3/a/@href').extract()
        for link in links:
            url = self.url_prefix + link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        page_index = int(page.split("/")[-2][5:])
        next_index = page_index + 1
        if next_index <= self.page_limit:
            page_prefix = page[:-(len(str(page_index)) + len(self.page_suffix))]
            next_page = page_prefix + str(next_index) + self.page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Scrape content
        title = response.xpath('//h1[@class = "title"]/text()').extract()
        intro = response.xpath('//div[@id = "ArticleContent"]/p/strong/text()').extract()
        content = response.xpath('//div[@id = "ArticleContent"]/p/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)
