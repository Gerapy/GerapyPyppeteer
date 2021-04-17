import scrapy

from gerapy_pyppeteer import PyppeteerRequest


class PretendTestSpider(scrapy.Spider):
    name = 'pretend_test'
    custom_settings = {
        # change your local chrome path
        'GERAPY_PYPPETEER_EXECUTABLE_PATH': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        'GERAPY_PYPPETEER_PRETEND': True
    }

    def start_requests(self):
        url = 'https://bot.sannysoft.com/'
        yield PyppeteerRequest(url=url, callback=self.parse_index, pretend=True, screenshot=False)

    def parse_index(self, response):
        import_test_name = response.xpath("//th[contains(text(), 'Test Name')]/../following-sibling::tr")
        import_test_result = f"\ntest_name\tresult_class\tresult\n"
        for i in import_test_name:
            test_name = i.xpath("string(./td[1])").get('')
            result_class = i.xpath("./td[2]/@class").re_first('passed|failed', '未知结果')
            result = i.xpath("./td[2]/text()").get('')
            import_test_result += f"{test_name}\t{result_class}\t{result}\n"
        self.logger.info(import_test_result)
