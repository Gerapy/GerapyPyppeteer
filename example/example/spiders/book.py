# -*- coding: utf-8 -*-
import scrapy
from

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['dynamic6.scrape.center']
    start_urls = ['http://dynamic6.scrape.center/']

    def parse(self, response):
        pass
