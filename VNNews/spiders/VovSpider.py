# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class VovSpider(TemplateSpider):
    name = "vov"
    allowed_domains = ["vov.vn"]
    filename = 'files/vov.txt'
    url_prefix = 'http://vov.vn'
    start_urls = [
        'http://vov.vn/chinh-tri/trang1',
        'http://vov.vn/doi-song/trang1',
        'http://vov.vn/thegioi/trang1',
        'http://vov.vn/kinh-te/trang1',
        'http://vov.vn/xa-hoi/trang1',
        'http://vov.vn/phap-luat/trang1',
        'http://vov.vn/the-thao/trang1',
        'http://vov.vn/van-hoa-giai-tri/trang1',
        'http://vov.vn/nguoi-viet/trang1',
        'http://vov.vn/suc-khoe/trang1',
        'http://vov.vn/oto-xe-may/trang1',
    ]

    def parse(self, response):
        page = response.url

        # Retrieve article links
        links = response.xpath('//h4[@class = "title"]/a/@href').extract()[1:-5]
        for link in links:
            url = self.url_prefix + link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-1][5:])
        next_index = current_index + 1
        if next_index <= self.page_limit:
            page_prefix = page[:-(len(str(current_index)))]
            next_page = page_prefix + str(next_index)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Get text content
        title = response.xpath('//h1[@class ="cms-title"]/text()').extract()
        intro = response.xpath('//p[@class = "sapo cms-desc"]/text()').extract()
        for i in xrange(0, len(intro)):
            intro[i] = intro[i][8:]  # Remove intro header
        content = response.xpath('//div[@id = "article-body"]/p/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)
