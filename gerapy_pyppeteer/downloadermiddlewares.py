import sys
import asyncio
from scrapy.http import HtmlResponse
import twisted.internet
from twisted.internet.asyncioreactor import AsyncioSelectorReactor
from twisted.internet.defer import Deferred
from gerapy_pyppeteer.request import PyppeteerRequest
from pyppeteer import launch

from gerapy_pyppeteer.settings import *

reactor = AsyncioSelectorReactor(asyncio.get_event_loop())

# install AsyncioSelectorReactor
twisted.internet.reactor = reactor
sys.modules['twisted.internet.reactor'] = reactor


def as_deferred(f):
    """
    transform a Twisted Deffered to an Asyncio Future
    :param f: async function
    """
    return Deferred.fromFuture(asyncio.ensure_future(f))


logger = logging.getLogger('gerapy.pyppeteer')


class PyppeteerMiddleware(object):
    """
    Downloader middleware handling the requests with Puppeteer
    """
    
    @classmethod
    def from_crawler(cls, crawler):
        """
        init the middleware
        :param crawler:
        :return:
        """
        settings = crawler.settings
        logging_level = settings.get('GERAPY_PYPPETEER_LOGGING_LEVEL', GERAPY_PYPPETEER_LOGGING_LEVEL)
        logging.getLogger('websockets').setLevel(logging_level)
        logging.getLogger('pyppeteer').setLevel(logging_level)
        
        # init settings
        cls.window_width = settings.get('GERAPY_PYPPETEER_WINDOW_WIDTH', GERAPY_PYPPETEER_WINDOW_WIDTH)
        cls.window_height = settings.get('GERAPY_PYPPETEER_WINDOW_HEIGHT', GERAPY_PYPPETEER_WINDOW_HEIGHT)
        cls.headless = settings.get('GERAPY_PYPPETEER_HEADLESS', GERAPY_PYPPETEER_HEADLESS)
        cls.dumpio = settings.get('GERAPY_PYPPETEER_DUMPIO', GERAPY_PYPPETEER_DUMPIO)
        cls.devtools = settings.get('GERAPY_PYPPETEER_DEVTOOLS', GERAPY_PYPPETEER_DEVTOOLS)
        cls.executable_path = settings.get('GERAPY_PYPPETEER_EXECUTABLE_PATH', GERAPY_PYPPETEER_EXECUTABLE_PATH)
        cls.disable_extensions = settings.get('GERAPY_PYPPETEER_DISABLE_EXTENSIONS',
                                              GERAPY_PYPPETEER_DISABLE_EXTENSIONS)
        cls.hide_scrollbars = settings.get('GERAPY_PYPPETEER_HIDE_SCROLLBARS', GERAPY_PYPPETEER_HIDE_SCROLLBARS)
        cls.mute_audio = settings.get('GERAPY_PYPPETEER_MUTE_AUDIO', GERAPY_PYPPETEER_MUTE_AUDIO)
        cls.no_sandbox = settings.get('GERAPY_PYPPETEER_NO_SANDBOX', GERAPY_PYPPETEER_NO_SANDBOX)
        cls.disable_setuid_sandbox = settings.get('GERAPY_PYPPETEER_DISABLE_SETUID_SANDBOX',
                                                  GERAPY_PYPPETEER_DISABLE_SETUID_SANDBOX)
        cls.disable_gpu = settings.get('GERAPY_PYPPETEER_DISABLE_GPU', GERAPY_PYPPETEER_DISABLE_GPU)
        cls.download_timeout = settings.get('GERAPY_PYPPETEER_DOWNLOAD_TIMEOUT',
                                            settings.get('DOWNLOAD_TIMEOUT', GERAPY_PYPPETEER_DOWNLOAD_TIMEOUT))
        return cls()
    
    async def _process_request(self, request: PyppeteerRequest, spider):
        """
        use pyppeteer to process spider
        :param request:
        :param spider:
        :return:
        """
        options = {
            'headless': self.headless,
            'dumpio': self.dumpio,
            'devtools': self.devtools,
            'args': [
                f'--window-size={self.window_width},{self.window_height}',
            ]
        }
        if self.executable_path: options['executable_path'] = self.executable_path
        if self.disable_extensions: options['args'].append('--disable-extensions')
        if self.hide_scrollbars: options['args'].append('--hide-scrollbars')
        if self.mute_audio: options['args'].append('--mute-audio')
        if self.no_sandbox: options['args'].append('--no-sandbox')
        if self.disable_setuid_sandbox: options['args'].append('--disable-setuid-sandbox')
        if self.disable_gpu: options['args'].append('--disable-gpu')
        if request.proxy: options['args'].append(f'--proxy-server={request.proxy}')
        
        logger.debug('set options %s', options)
        
        browser = await launch(options)
        page = await browser.newPage()
        await page.setViewport({'width': self.window_width, 'height': self.window_height})
        
        # set cookies
        if isinstance(request.cookies, dict):
            await page.setCookie(*[
                {'name': k, 'value': v}
                for k, v in request.cookies.items()
            ])
        else:
            await page.setCookie(request.cookies)
        
        # the headers must be set using request interception
        await page.setRequestInterception(True)
        
        @page.on('request')
        async def _handle_headers(pu_request):
            overrides = {
                'headers': {
                    k.decode(): ','.join(map(lambda v: v.decode(), v))
                    for k, v in request.headers.items()
                }
            }
            await pu_request.continue_(overrides=overrides)
        
        timeout = self.download_timeout
        if request.timeout is not None:
            timeout = request.timeout
        
        logger.debug('crawling %s', request.url)
        response = await page.goto(
            request.url,
            options={
                'timeout': 1000 * timeout,
                'waitUntil': request.wait_until
            }
        )
        
        if request.wait_for:
            logger.debug('waiting for %s finished', request.url)
            await page.waitFor(request.wait_for)
            logger.debug('wait for %s finished', request.url)
        
        # evaluate script
        if request.script:
            logger.debug('evaluating %s', request.script)
            await page.evaluate(request.script)
        
        # sleep
        if request.sleep is not None:
            logger.debug('sleep for %ss', request.sleep)
            await asyncio.sleep(request.sleep)
        
        content = await page.content()
        body = str.encode(content)
        
        # close page and browser
        logger.debug('close pyppeteer')
        await page.close()
        await browser.close()
        
        # Necessary to bypass the compression middleware (?)
        response.headers.pop('content-encoding', None)
        response.headers.pop('Content-Encoding', None)
        
        return HtmlResponse(
            page.url,
            status=response.status,
            headers=response.headers,
            body=body,
            encoding='utf-8',
            request=request
        )
    
    def process_request(self, request, spider):
        """
        process request using pyppeteer
        :param request:
        :param spider:
        :return:
        """
        logger.debug('processing request %s', request)
        
        if not isinstance(request, PyppeteerRequest):
            logger.info('request is not PyppeteerRequest, just return')
            return None
        
        return as_deferred(self._process_request(request, spider))
    
    async def _spider_closed(self):
        pass
    
    def spider_closed(self):
        """
        callback when spider closed
        :return:
        """
        return as_deferred(self._spider_closed())
