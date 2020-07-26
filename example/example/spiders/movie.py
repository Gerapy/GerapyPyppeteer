# -*- coding: utf-8 -*-
import scrapy
from gerapy_pyppeteer import PyppeteerRequest
from scrapy import Request, signals
from example.items import MovieItem
import logging

logger = logging.getLogger(__name__)


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['antispider1.scrape.center']
    base_url = 'https://antispider1.scrape.center'
    max_page = 10
    
    def start_requests(self):
        """
        first page
        :return:
        """
        for page in range(1, self.max_page + 1):
            url = f'{self.base_url}/page/{page}'
            logger.debug('start url %s', url)
            yield PyppeteerRequest(url, callback=self.parse_index, priority=10, wait_for='.item')
    
    def parse_index(self, response):
        """
        extract movies
        :param response:
        :return:
        """
        items = response.css('.item')
        for item in items:
            href = item.css('.name::attr(href)').extract_first()
            detail_url = response.urljoin(href)
            logger.info('detail url %s', detail_url)
            yield PyppeteerRequest(detail_url, callback=self.parse_detail, wait_for='.item')
    
    def parse_detail(self, response):
        """
        process detail info of book
        :param response:
        :return:
        """
        name = response.css('h2::text').extract_first()
        categories = response.css('.categories button span::text').extract()
        score = response.css('.score::text').extract_first()
        categories = [category.strip() for category in categories] if categories else []
        score = score.strip() if score else None
        yield MovieItem(name=name, categories=categories, score=score)
