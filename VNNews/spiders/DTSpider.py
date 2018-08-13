# -*- coding: utf-8 -*-
import scrapy

from VNNews.spiders.TemplateSpider import TemplateSpider


class DTSpider(TemplateSpider):
    name = "dantri"
    allowed_domains = ["dantri.com.vn"]
    filename = 'dantri.txt'
    start_urls = [
        'http://dantri.com.vn/su-kien/trang-2.htm',
        'http://dantri.com.vn/xa-hoi/trang-2.htm',
        'http://dantri.com.vn/the-gioi/trang-2.htm',
        'http://dantri.com.vn/the-thao/trang-2.htm',
        'http://dantri.com.vn/giao-duc-khuyen-hoc/trang-2.htm',
        'http://dantri.com.vn/tam-long-nhan-ai/trang-2.htm',
        'http://dantri.com.vn/kinh-doanh/trang-2.htm',
        'http://dantri.com.vn/van-hoa/trang-2.htm',
        'http://dantri.com.vn/giai-tri/trang-2.htm',
        'http://dantri.com.vn/phap-luat/trang-2.htm',
        'http://dantri.com.vn/nhip-song-tre/trang-2.htm',
        'http://dantri.com.vn/suc-khoe/trang-2.htm',
        'http://dantri.com.vn/suc-manh-so/trang-2.htm',
        'http://dantri.com.vn/o-to-xe-may/trang-2.htm',
        'http://dantri.com.vn/tinh-yeu-gioi-tinh/trang-2.htm',
        'http://dantri.com.vn/chuyen-la/trang-2.htm'
    ]
    page_suffix = '.htm'
    url_prefix = 'http://dantri.com.vn'

    def parse(self, response):
        page = response.url

        # Retrieve article links
        list_div = response.xpath('//div[@id = "listcheckepl"]').xpath('.//div[@class = "mr1"]')
        links = list_div.xpath('.//a/@href').extract()
        for link in links:
            url = self.url_prefix + link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        current_index = int(page.split('/')[-1].split('.')[0].split('-')[1])
        next_index = current_index + 1
        if next_index <= self.page_limit + 1:
            page_prefix = page[:-(len(str(current_index)) + len(self.page_suffix))]
            next_page = page_prefix + str(next_index) + self.page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):

        # Get text content
        title = response.css('title::text').extract()
        content = response.xpath('//div[@id = "divNewsContent"]').xpath('.//p/text()').extract()
        intro = []

        # Save content
        yield self.get_item(title, intro, content, response)

