# -*- coding: utf-8 -*-
import scrapy

from VNNews.spiders.TemplateSpider import TemplateSpider


class K14Spider(TemplateSpider):
    name = "kenh14"
    allowed_domains = ["kenh14.vn"]
    url_prefix = 'http://kenh14.vn'
    page_prefix = 'http://kenh14.vn/timeline/laytinmoitronglist-'
    filename = 'k14.txt'
    start_urls = [
        'http://kenh14.vn/timeline/laytinmoitronglist-1-2-1-1-1-1-4-0-3-1.chn',  # Doi-song
        'http://kenh14.vn/timeline/laytinmoitronglist-1-2-1-1-1-1-118-0-3-1.chn',  # The-thao
        'http://kenh14.vn/timeline/laytinmoitronglist-1-2-1-1-1-1-3-0-3-1.chn',  # Music
        'http://kenh14.vn/timeline/laytinmoitronglist-1-2-1-1-1-1-142-0-3-1.chn',  # Xa-hoi
        'http://kenh14.vn/timeline/laytinmoitronglist-1-2-1-1-1-1-149-0-3-1.chn',  # The-gioi
    ]

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//h3[@class = "knswli-title"]/a/@href').extract()
        for link in links:
            url = self.url_prefix + link
            yield scrapy.Request(url=url, callback=self.parse_content)

        # Navigate to next page
        page_index = int(page.split('/')[-1].split('-')[1])
        next_index = page_index + 1
        page_suffix = page[-(len(page) - (len(self.page_prefix) + len(str(page_index)))):]
        if next_index <= self.page_limit:
            next_page = self.page_prefix + str(next_index) + page_suffix
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        # Scrape content
        title = response.xpath('//h1[@class = "kbwc-title"]/text()').extract()
        content = response.xpath('//div[@class = "knc-content"]/p/text()').extract()
        intro = []

        # Save content
        yield self.get_item(title, intro, content, response)
