from scrapy import Request


class PyppeteerRequest(Request):
    """
    Scrapy ``Request`` subclass providing additional arguments
    """
    
    def __init__(self, url, callback=None, wait_until=None, wait_for=None, script=None, sleep=None, timeout=None,
                 proxy=None, ignore_resource_types=None, *args,
                 **kwargs):
        """
        :param url: request url
        :param callback: callback
        :param wait_until: one of "load", "domcontentloaded", "networkidle0", "networkidle2".
                see https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.goto
        :param wait_for: wait for some element to load
        :param script: script to execute
        :param sleep: time to sleep after loaded
        :param args:
        :param kwargs:
        """
        self.wait_until = wait_until or 'domcontentloaded'
        self.wait_for = wait_for
        self.script = script
        self.sleep = sleep
        self.proxy = proxy
        self.timeout = timeout
        self.ignore_resource_types = ignore_resource_types
        
        super().__init__(url, callback, *args, **kwargs)
