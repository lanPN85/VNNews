# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class VnPlusSpider(TemplateSpider):
    name = "vnplus"
    allowed_domains = ["www.vietnamplus.vn"]
    filename = 'files/vnplus.txt'
    url_prefix = 'http://www.vietnamplus.vn/'
    page_suffix = '.vnp'
    start_urls = [
        'http://www.vietnamplus.vn/kinhte/trang2.vnp',
        'http://www.vietnamplus.vn/chinhtri/trang2.vnp',
        'http://www.vietnamplus.vn/xahoi/trang2.vnp',
        'http://www.vietnamplus.vn/thegioi/trang2.vnp',
        'http://www.vietnamplus.vn/doisong/trang2.vnp',
        'http://www.vietnamplus.vn/vanhoa/trang2.vnp',
        'http://www.vietnamplus.vn/thethao/trang2.vnp',
        'http://www.vietnamplus.vn/khaohoc/trang2.vnp',
        'http://www.vietnamplus.vn/congnghe/trang2.vnp',
        'http://www.vietnamplus.vn/chuyenla/trang2.vnp',
    ]

    def parse(self, response):
        page = response.url

        # Retrieve article links
        links = response.xpath(
            '//div[@class = "story-listing slist-03"]/article[@class = "story "]/a/@href').extract()
        for link in links:
            url = self.url_prefix + link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-1].split('.')[0][5:])
        next_index = current_index + 1
        if next_index <= self.page_limit + 1:
            page_prefix = page[:-(len(str(current_index)) + len(self.page_suffix))]
            next_page = page_prefix + str(next_index) + self.page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Get text content
        title = response.xpath('//header[@class = "article-header"]/h1/text()').extract()
        content = response.xpath('//div[@class = "article-body cms-body AdAsia"]/text()').extract()
        intro = []

        # Save content
        yield self.get_item(title, intro, content, response)
