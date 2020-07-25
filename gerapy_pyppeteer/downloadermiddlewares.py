import sys
import asyncio
from pyppeteer.errors import PageError, TimeoutError
from scrapy.http import HtmlResponse
import twisted.internet
from scrapy.utils.python import global_object_name
from twisted.internet.asyncioreactor import AsyncioSelectorReactor
from twisted.internet.defer import Deferred
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
    
    def _retry(self, request, reason, spider):
        """
        get retry request
        :param request:
        :param reason:
        :param spider:
        :return:
        """
        if not self.retry_enabled:
            return
        
        retries = request.meta.get('retry_times', 0) + 1
        retry_times = self.max_retry_times
        
        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']
        
        stats = spider.crawler.stats
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            
            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)
            
            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            logger.error("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
    
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
        cls.ignore_https_errors = settings.get('GERAPY_PYPPETEER_IGNORE_HTTPS_ERRORS',
                                               GERAPY_PYPPETEER_IGNORE_HTTPS_ERRORS)
        cls.slow_mo = settings.get('GERAPY_PYPPETEER_SLOW_MO', GERAPY_PYPPETEER_SLOW_MO)
        cls.ignore_default_args = settings.get('GERAPY_PYPPETEER_IGNORE_DEFAULT_ARGS',
                                               GERAPY_PYPPETEER_IGNORE_DEFAULT_ARGS)
        cls.handle_sigint = settings.get('GERAPY_PYPPETEER_HANDLE_SIGINT', GERAPY_PYPPETEER_HANDLE_SIGINT)
        cls.handle_sigterm = settings.get('GERAPY_PYPPETEER_HANDLE_SIGTERM', GERAPY_PYPPETEER_HANDLE_SIGTERM)
        cls.handle_sighup = settings.get('GERAPY_PYPPETEER_HANDLE_SIGHUP', GERAPY_PYPPETEER_HANDLE_SIGHUP)
        cls.auto_close = settings.get('GERAPY_PYPPETEER_AUTO_CLOSE', GERAPY_PYPPETEER_AUTO_CLOSE)
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
        cls.ignore_resource_types = settings.get('GERAPY_IGNORE_RESOURCE_TYPES', GERAPY_IGNORE_RESOURCE_TYPES)
        
        cls.retry_enabled = settings.getbool('RETRY_ENABLED')
        cls.max_retry_times = settings.getint('RETRY_TIMES')
        cls.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        cls.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        
        return cls()
    
    async def _process_request(self, request, spider):
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
        if self.executable_path:
            options['executable_path'] = self.executable_path
        if self.ignore_https_errors:
            options['ignoreHTTPSErrors'] = self.ignore_https_errors
        if self.slow_mo:
            options['slowMo'] = self.slow_mo
        if self.ignore_default_args:
            options['ignoreDefaultArgs'] = self.ignore_default_args
        if self.handle_sigint:
            options['handleSIGINT'] = self.handle_sigint
        if self.handle_sigterm:
            options['handleSIGTERM'] = self.handle_sigterm
        if self.handle_sighup:
            options['handleSIGHUP'] = self.handle_sighup
        if self.auto_close:
            options['autoClose'] = self.auto_close
        if self.disable_extensions:
            options['args'].append('--disable-extensions')
        if self.hide_scrollbars:
            options['args'].append('--hide-scrollbars')
        if self.mute_audio:
            options['args'].append('--mute-audio')
        if self.no_sandbox:
            options['args'].append('--no-sandbox')
        if self.disable_setuid_sandbox:
            options['args'].append('--disable-setuid-sandbox')
        if self.disable_gpu:
            options['args'].append('--disable-gpu')
        
        # get pyppeteer meta
        pyppeteer_meta = request.meta.get('pyppeteer')
        logger.debug('pyppeteer_meta %s', pyppeteer_meta)
        
        # set proxy
        proxy = pyppeteer_meta.get('proxy')
        if not proxy:
            proxy = request.meta.get('proxy')
        if proxy: options['args'].append(f'--proxy-server={proxy}')
        
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
        async def _handle_interception(pu_request):
            # handle headers
            overrides = {
                'headers': {
                    k.decode(): ','.join(map(lambda v: v.decode(), v))
                    for k, v in request.headers.items()
                }
            }
            # handle resource types
            _ignore_resource_types = self.ignore_resource_types
            if request.meta.get('pyppeteer', {}).get('ignore_resource_types') is not None:
                _ignore_resource_types = request.meta.get('pyppeteer', {}).get('ignore_resource_types')
            if pu_request.resourceType in _ignore_resource_types:
                await pu_request.abort()
            else:
                await pu_request.continue_(overrides)
        
        _timeout = self.download_timeout
        if pyppeteer_meta.get('timeout') is not None:
            _timeout = pyppeteer_meta.get('timeout')
        
        logger.debug('crawling %s', request.url)
        
        response = None
        try:
            options = {
                'timeout': 1000 * _timeout,
                'waitUntil': pyppeteer_meta.get('wait_until')
            }
            logger.debug('request %s with options %s', request.url, options)
            response = await page.goto(
                request.url,
                options=options
            )
        except (PageError, TimeoutError):
            logger.error('error rendering url %s using pyppeteer', request.url)
            await page.close()
            await browser.close()
            return self._retry(request, 504, spider)
        
        if pyppeteer_meta.get('wait_for'):
            _wait_for = pyppeteer_meta.get('wait_for')
            try:
                logger.debug('waiting for %s finished', _wait_for)
                await page.waitFor(_wait_for)
            except TimeoutError:
                logger.error('error waiting for %s of %s', _wait_for, request.url)
                await page.close()
                await browser.close()
                return self._retry(request, 504, spider)
        
        # evaluate script
        if pyppeteer_meta.get('script'):
            _script = pyppeteer_meta.get('script')
            logger.debug('evaluating %s', _script)
            await page.evaluate(_script)
        
        # sleep
        if pyppeteer_meta.get('sleep') is not None:
            _sleep = pyppeteer_meta.get('sleep')
            logger.debug('sleep for %ss', _sleep)
            await asyncio.sleep(_sleep)
        
        content = await page.content()
        body = str.encode(content)
        
        # close page and browser
        logger.debug('close pyppeteer')
        await page.close()
        await browser.close()
        
        if not response:
            logger.error('get null response by pyppeteer of url %s', request.url)
        
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
        return as_deferred(self._process_request(request, spider))
    
    async def _spider_closed(self):
        pass
    
    def spider_closed(self):
        """
        callback when spider closed
        :return:
        """
        return as_deferred(self._spider_closed())
