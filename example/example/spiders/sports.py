import scrapy
from gerapy_pyppeteer import PyppeteerRequest


class SportsSpider(scrapy.Spider):
    name = 'sports'
    allowed_domains = ['sports.qq.com']
    start_urls = ['http://sports.qq.com/']
    
    def start_requests(self):
        for url in self.start_urls:
            yield PyppeteerRequest(url, callback=self.parse_index, pretend=False)
    
    def parse_index(self, response):
        pass
