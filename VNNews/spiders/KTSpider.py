# -*- coding: utf-8 -*-
import scrapy

from VNNews.spiders.TemplateSpider import TemplateSpider


class KTSpider(TemplateSpider):
    name = "ktn"
    allowed_domains = ["kienthuc.net.vn"]
    filename = 'ktn.txt'
    start_urls = [
        'http://kienthuc.net.vn/xa-hoi/?page=2',
        'http://kienthuc.net.vn/the-gioi/?page=2',
        'http://kienthuc.net.vn/cong-dong-tre/?page=2',
        'http://kienthuc.net.vn/kinh-doanh/?page=2',
        'http://kienthuc.net.vn/quan-su/?page=2',
        'http://kienthuc.net.vn/kho-tri-thuc/?page=2',
        'http://kienthuc.net.vn/kham-pha/?page=2',
        'http://kienthuc.net.vn/cong-nghe/?page=2',
        'http://kienthuc.net.vn/lan-banh/?page=2',
        'http://kienthuc.net.vn/giai-tri/?page=2',
        'http://kienthuc.net.vn/khoe-dep/?page=2',
        'http://kienthuc.net.vn/thien/?page=2'

    ]
    url_prefix = 'http://kienthuc.net.vn'

    def parse(self, response):
        page = response.url

        # Navigate to content
        links = response.xpath('//article[@class = "story clearfix"]/h2[@class = "title"]/a/@href').extract()
        for link in links:
            url = self.url_prefix + link
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
        title = response.xpath('//h1[@class = "cms-title"]/text()').extract()
        intro = response.xpath('//h3[@class = "sapo cms-desc"]/div/text()').extract()
        content = response.xpath('//div[@id = "abody"]/div/text()').extract()

        yield self.get_item(title, intro, content, response)
