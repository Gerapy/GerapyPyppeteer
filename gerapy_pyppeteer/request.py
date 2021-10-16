from scrapy import Request
import copy


class PyppeteerRequest(Request):
    """
    Scrapy ``Request`` subclass providing additional arguments
    """

    def __init__(self, url, callback=None, wait_until=None, wait_for=None, script=None, actions=None, proxy=None,
                 proxy_credential=None, sleep=None, timeout=None, ignore_resource_types=None, pretend=None, screenshot=None, meta=None,
                 *args, **kwargs):
        """
        :param url: request url
        :param callback: callback
        :param one of "load", "domcontentloaded", "networkidle0", "networkidle2".
                see https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.goto, default is `domcontentloaded`
        :param wait_for: wait for some element to load, also supports dict
        :param script: script to execute
        :param actions: actions defined for execution of Page object
        :param proxy: use proxy for this time, like `http://x.x.x.x:x`
        :param proxy_credential: the proxy credential, like `{'username': 'xxxx', 'password': 'xxxx'}`
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
        pyppeteer_meta = meta.get('pyppeteer') or {}

        self.wait_until = pyppeteer_meta.get('wait_until') if pyppeteer_meta.get(
            'wait_until') is not None else (wait_until or 'domcontentloaded')
        self.wait_for = pyppeteer_meta.get('wait_for') if pyppeteer_meta.get(
            'wait_for') is not None else wait_for
        self.script = pyppeteer_meta.get('script') if pyppeteer_meta.get(
            'script') is not None else script
        self.actions = pyppeteer_meta.get('actions') if pyppeteer_meta.get(
            'actions') is not None else actions
        self.sleep = pyppeteer_meta.get('sleep') if pyppeteer_meta.get(
            'sleep') is not None else sleep
        self.proxy = pyppeteer_meta.get('proxy') if pyppeteer_meta.get(
            'proxy') is not None else proxy
        self.proxy_credential = pyppeteer_meta.get('proxy_credential') if pyppeteer_meta.get(
            'proxy_credential') is not None else proxy_credential
        self.pretend = pyppeteer_meta.get('pretend') if pyppeteer_meta.get(
            'pretend') is not None else pretend
        self.timeout = pyppeteer_meta.get('timeout') if pyppeteer_meta.get(
            'timeout') is not None else timeout
        self.ignore_resource_types = pyppeteer_meta.get('ignore_resource_types') if pyppeteer_meta.get(
            'ignore_resource_types') is not None else ignore_resource_types
        self.screenshot = pyppeteer_meta.get('screenshot') if pyppeteer_meta.get(
            'screenshot') is not None else screenshot

        pyppeteer_meta = meta.setdefault('pyppeteer', {})
        pyppeteer_meta['wait_until'] = self.wait_until
        pyppeteer_meta['wait_for'] = self.wait_for
        pyppeteer_meta['script'] = self.script
        pyppeteer_meta['actions'] = self.actions
        pyppeteer_meta['sleep'] = self.sleep
        pyppeteer_meta['proxy'] = self.proxy
        pyppeteer_meta['proxy_credential'] = self.proxy_credential
        pyppeteer_meta['pretend'] = self.pretend
        pyppeteer_meta['timeout'] = self.timeout
        pyppeteer_meta['screenshot'] = self.screenshot
        pyppeteer_meta['ignore_resource_types'] = self.ignore_resource_types

        super().__init__(url, callback, meta=meta, *args, **kwargs)
