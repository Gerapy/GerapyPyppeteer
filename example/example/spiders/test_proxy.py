# -*- coding: utf-8 -*-
import scrapy
from gerapy_pyppeteer import PyppeteerRequest
from scrapy import Request, signals
from example.items import MovieItem
import logging

logger = logging.getLogger(__name__)


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['www.httpbin.org']
    base_url = 'https://www.httpbin.org/get'
    max_page = 10
    custom_settings = {
        'GERAPY_PYPPETEER_PROXY': 'http://tps254.kdlapi.com:15818',
        'GERAPY_PYPPETEER_PROXY_CREDENTIAL': {
            'username': '',
            'password': ''
        }
    }

    def start_requests(self):
        """
        first page
        :return:
        """
        yield PyppeteerRequest(self.base_url,
                               callback=self.parse_index,
                               priority=10,
                               proxy='http://tps254.kdlapi.com:15818',
                               proxy_credential={
                                   'username': '',
                                   'password': ''
                               })

    def parse_index(self, response):
        """
        extract movies
        :param response:
        :return:
        """
        print(response.text)
