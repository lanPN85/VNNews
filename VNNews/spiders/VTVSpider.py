# -*- coding: utf-8 -*-
import scrapy

from TemplateSpider import TemplateSpider


class VTVSpider(TemplateSpider):
    name = "vtv"
    allowed_domains = ["vtv.vn"]
    filename = 'files/vtv.txt'
    page_suffix = '.htm'
    url_prefix = 'http://vtv.vn'
    start_urls = [
        'http://vtv.vn/timeline/121/trang-1.htm',  # Trong-nuoc
        'http://vtv.vn/timeline/122/trang-1.htm',  # Quoc-te
        'http://vtv.vn/timeline/87/trang-1.htm',  # Giai-tri
        'http://vtv.vn/timeline/90/trang-1.htm',  # Kinh te
        'http://vtv.vn/timeline/132/trang-1.htm',  # Doi-song
        'http://vtv.vn/timeline/166/trang-1.htm',  # Giao duc
        'http://vtv.vn/timeline/109/trang-1.htm',  # Cong-nghe
    ]

    def parse(self, response):
        page = response.url

        # Retrieve article links
        links = response.xpath('//h4/a/@href').extract()
        for link in links:
            url = self.url_prefix + link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-1].split('.')[0].split('-')[1])
        next_index = current_index + 1
        if next_index <= self.page_limit:
            page_prefix = page[:-(len(self.page_suffix) + len(str(current_index)))]
            next_page = page_prefix + str(next_index) + self.page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Get text content
        title = response.xpath('//h1[@class = "title_detail"]/text()').extract()
        intro = response.xpath('//h2[@class = "sapo"]/text()').extract()
        for i in xrange(0, len(intro)):
            intro[i] = intro[i][9:]  # Remove intro header
        content = response.xpath('//div[@class = "ta-justify"]/p/text()').extract()

        # Save content
        yield self.get_item(title, intro, content, response)
