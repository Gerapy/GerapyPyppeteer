from scrapy import Request
import copy


class PyppeteerRequest(Request):
    """
    Scrapy ``Request`` subclass providing additional arguments
    """
    
    def __init__(self, url, callback=None, wait_until=None, wait_for=None, script=None, proxy=None,
                 sleep=None, timeout=None, ignore_resource_types=None, pretend=None, screenshot=None, meta=None, *args,
                 **kwargs):
        """
        :param url: request url
        :param callback: callback
        :param one of "load", "domcontentloaded", "networkidle0", "networkidle2".
                see https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.goto, default is `domcontentloaded`
        :param wait_for: wait for some element to load, also supports dict
        :param script: script to execute
        :param proxy: use proxy for this time, like `http://x.x.x.x:x`
        :param sleep: time to sleep after loaded, override `GERAPY_PYPPETEER_SLEEP`
        :param timeout: load timeout, override `GERAPY_PYPPETEER_DOWNLOAD_TIMEOUT`
        :param ignore_resource_types: ignored resource types, override `GERAPY_PYPPETEER_IGNORE_RESOURCE_TYPES`
        :param pretend: pretend as normal browser, override `GERAPY_PYPPETEER_PRETEND`
        :param screenshot: ignored resource types, see
                https://miyakogi.github.io/pyppeteer/_modules/pyppeteer/page.html#Page.screenshot,
                override `GERAPY_PYPPETEER_SCREENSHOT`
        :param args:
        :param kwargs:
        """
        # use meta info to save args
        meta = copy.deepcopy(meta) or {}
        pyppeteer_mata = meta.get('pyppeteer') or {}
        
        self.wait_until = pyppeteer_mata.get('wait_until') if pyppeteer_mata.get(
            'wait_until') is not None else (wait_until or 'domcontentloaded')
        self.wait_for = pyppeteer_mata.get('wait_for') if pyppeteer_mata.get('wait_for') is not None else wait_for
        self.script = pyppeteer_mata.get('script') if pyppeteer_mata.get('script') is not None else script
        self.sleep = pyppeteer_mata.get('sleep') if pyppeteer_mata.get('sleep') is not None else sleep
        self.proxy = pyppeteer_mata.get('proxy') if pyppeteer_mata.get('proxy') is not None else proxy
        self.pretend = pyppeteer_mata.get('pretend') if pyppeteer_mata.get('pretend') is not None else pretend
        self.timeout = pyppeteer_mata.get('timeout') if pyppeteer_mata.get('timeout') is not None else timeout
        self.ignore_resource_types = pyppeteer_mata.get('ignore_resource_types') if pyppeteer_mata.get(
            'ignore_resource_types') is not None else ignore_resource_types
        self.screenshot = pyppeteer_mata.get('screenshot') if pyppeteer_mata.get(
            'screenshot') is not None else screenshot
        
        pyppeteer_mata = meta.setdefault('pyppeteer', {})
        pyppeteer_mata['wait_until'] = self.wait_until
        pyppeteer_mata['wait_for'] = self.wait_for
        pyppeteer_mata['script'] = self.script
        pyppeteer_mata['sleep'] = self.sleep
        pyppeteer_mata['proxy'] = self.proxy
        pyppeteer_mata['pretend'] = self.pretend
        pyppeteer_mata['timeout'] = self.timeout
        pyppeteer_mata['screenshot'] = self.screenshot
        pyppeteer_mata['ignore_resource_types'] = self.ignore_resource_types
        
        super().__init__(url, callback, meta=meta, *args, **kwargs)
