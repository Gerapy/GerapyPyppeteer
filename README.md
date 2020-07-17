# Gerapy Pyppeteer

This is a package for supporting pyppeteer in Scrapy, also this
package is a module in [Gerapy](https://github.com/Gerapy/Gerapy).

## Installation

```shell script
pip3 install gerapy-pyppeteer
```

## Usage

You can use `PyppeteerRequest` to specify a request which uses pyppeteer to render.

For example:

```python
yield PyppeteerRequest(detail_url, callback=self.parse_detail)
```

And you also need to enable `PyppeteerMiddleware` in `DOWNLOADER_MIDDLEWARES`:

```python
DOWNLOADER_MIDDLEWARES = {
    'gerapy_pyppeteer.downloadermiddlewares.PyppeteerMiddleware': 543,
}
```

Congratulate, you've finished the all of the required configuration.

If you run the Spider again, Pyppeteer will be started to render every
web page which you configured the request as PyppeteerRequest.

## Settings

GerapyPyppeteer provides some optional settings.

### Concurrency 

You can directly use Scrapy's setting to set Concurrency of Pyppeteer,
for example:

```python
CONCURRENT_REQUESTS = 3
```

### Logging Level

By default, Pyppeteer will log all the debug messages, so GerapyPyppeteer
configured the logging level of Pyppeteer to WARNING.

If you want to see more logs from Pyppeteer, you can change the this setting: 

```python
import logging
GERAPY_PYPPETEER_LOGGING_LEVEL = logging.DEBUG
```

### Download Timeout

Pyppeteer may take some time to render the required web page, you can also change this setting, default is `30s`:

```python
# pyppeteer timeout
GERAPY_PYPPETEER_DOWNLOAD_TIMEOUT = 30
```

### Headless

By default, Pyppeteer is running in `Headless` mode, you can also 
change it to `False` as you need, default is `True`:

```python
GERAPY_PYPPETEER_HEADLESS = False 
```

### Window Size

You can also set the width and height of Pyppeteer window:

```python
GERAPY_PYPPETEER_WINDOW_WIDTH = 1400
GERAPY_PYPPETEER_WINDOW_HEIGHT = 700
```

Default is 1400, 700.

### Pyppeteer Args

You can also change the args of Pyppeteer, such as `dumpio`, `devtools`, etc.

Optional settings and their default values:

```python
GERAPY_PYPPETEER_DUMPIO = False
GERAPY_PYPPETEER_DEVTOOLS = False
GERAPY_PYPPETEER_EXECUTABLE_PATH = None
GERAPY_PYPPETEER_DISABLE_EXTENSIONS = True
GERAPY_PYPPETEER_HIDE_SCROLLBARS = True
GERAPY_PYPPETEER_MUTE_AUDIO = True
GERAPY_PYPPETEER_NO_SANDBOX = True
GERAPY_PYPPETEER_DISABLE_SETUID_SANDBOX = True
GERAPY_PYPPETEER_DISABLE_GPU = True
```

### Disable loading of specific resource type

You can disable the loading of specific resource type to
decrease the loading time of web page. You can configure
the disabled resource types using `GERAPY_IGNORE_RESOURCE_TYPES`:

```python
GERAPY_IGNORE_RESOURCE_TYPES = []
```

For example, if you want to disable the loading of css and javascript,
you can set as below:

```python
GERAPY_IGNORE_RESOURCE_TYPES = ['stylesheet', 'script']
```

All of the optional resource type list:

* document: the Original HTML document
* stylesheet: CSS files
* script: JavaScript files
* image: Images
* media: Media files such as audios or videos
* font: Fonts files
* texttrack: Text Track files
* xhr: Ajax Requests
* fetch: Fetch Requests
* eventsource: Event Source
* websocket: Websocket
* manifest: Manifest files
* other: Other files

### Settings for each Pyppeteer Request

`PyppeteerRequest` provide args which can override global settings above.

* wait_until: one of "load", "domcontentloaded", "networkidle0", "networkidle2".
                see https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.goto, default is `domcontentloaded`
* wait_for: wait for some element to load
* script: script to execute after page loaded
* sleep: time to sleep after page loaded
* ignore_resource_types: ignored resource types

For example, you can configure PyppeteerRequest as:

```python
from gerapy_pyppeteer import PyppeteerRequest

def parse(self, response):
    yield PyppeteerRequest(url, 
        callback=self.parse_detail,
        wait_until='domcontentloaded',
        wait_for='title',
        script='() => { console.log(document) }',
        sleep=2)
```

Then Pyppeteer will:
* wait for document to load
* wait for title to load
* execute `console.log(document)` script
* sleep for 2s
* return the rendered web page content

## Example

For more detail, please see [example](./example).

Also you can directly run with Docker:

```
docker run germey/gerapy-pyppeteer-example
```

Outputs:

```shell script
2020-07-13 01:49:13 [scrapy.utils.log] INFO: Scrapy 2.2.0 started (bot: example)
2020-07-13 01:49:13 [scrapy.utils.log] INFO: Versions: lxml 4.3.3.0, libxml2 2.9.9, cssselect 1.1.0, parsel 1.6.0, w3lib 1.22.0, Twisted 20.3.0, Python 3.7.7 (default, May  6 2020, 04:59:01) - [Clang 4.0.1 (tags/RELEASE_401/final)], pyOpenSSL 19.1.0 (OpenSSL 1.1.1d  10 Sep 2019), cryptography 2.8, Platform Darwin-19.4.0-x86_64-i386-64bit
2020-07-13 01:49:13 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.asyncioreactor.AsyncioSelectorReactor
2020-07-13 01:49:13 [scrapy.crawler] INFO: Overridden settings:
{'BOT_NAME': 'example',
 'CONCURRENT_REQUESTS': 3,
 'NEWSPIDER_MODULE': 'example.spiders',
 'RETRY_HTTP_CODES': [403, 500, 502, 503, 504],
 'SPIDER_MODULES': ['example.spiders']}
2020-07-13 01:49:13 [scrapy.extensions.telnet] INFO: Telnet Password: 83c276fb41754bd0
2020-07-13 01:49:13 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.memusage.MemoryUsage',
 'scrapy.extensions.logstats.LogStats']
2020-07-13 01:49:13 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'gerapy_pyppeteer.downloadermiddlewares.PyppeteerMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2020-07-13 01:49:13 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2020-07-13 01:49:13 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2020-07-13 01:49:13 [scrapy.core.engine] INFO: Spider opened
2020-07-13 01:49:13 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2020-07-13 01:49:13 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2020-07-13 01:49:13 [example.spiders.book] INFO: crawling https://dynamic5.scrape.center/page/1
2020-07-13 01:49:13 [gerapy.pyppeteer] DEBUG: processing request <GET https://dynamic5.scrape.center/page/1>
2020-07-13 01:49:13 [gerapy.pyppeteer] DEBUG: set options {'headless': True, 'dumpio': False, 'devtools': False, 'args': ['--window-size=1400,700', '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']}
2020-07-13 01:49:14 [gerapy.pyppeteer] DEBUG: crawling https://dynamic5.scrape.center/page/1
2020-07-13 01:49:19 [gerapy.pyppeteer] DEBUG: waiting for .item .name finished
2020-07-13 01:49:20 [gerapy.pyppeteer] DEBUG: wait for .item .name finished
2020-07-13 01:49:20 [gerapy.pyppeteer] DEBUG: close pyppeteer
2020-07-13 01:49:20 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://dynamic5.scrape.center/page/1> (referer: None)
2020-07-13 01:49:20 [gerapy.pyppeteer] DEBUG: processing request <GET https://dynamic5.scrape.center/detail/26898909>
2020-07-13 01:49:20 [gerapy.pyppeteer] DEBUG: processing request <GET https://dynamic5.scrape.center/detail/26861389>
2020-07-13 01:49:20 [gerapy.pyppeteer] DEBUG: processing request <GET https://dynamic5.scrape.center/detail/26855315>
2020-07-13 01:49:20 [gerapy.pyppeteer] DEBUG: set options {'headless': True, 'dumpio': False, 'devtools': False, 'args': ['--window-size=1400,700', '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']}
2020-07-13 01:49:20 [gerapy.pyppeteer] DEBUG: set options {'headless': True, 'dumpio': False, 'devtools': False, 'args': ['--window-size=1400,700', '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']}
2020-07-13 01:49:21 [gerapy.pyppeteer] DEBUG: set options {'headless': True, 'dumpio': False, 'devtools': False, 'args': ['--window-size=1400,700', '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']}
2020-07-13 01:49:21 [gerapy.pyppeteer] DEBUG: crawling https://dynamic5.scrape.center/detail/26855315
2020-07-13 01:49:21 [gerapy.pyppeteer] DEBUG: crawling https://dynamic5.scrape.center/detail/26861389
2020-07-13 01:49:21 [gerapy.pyppeteer] DEBUG: crawling https://dynamic5.scrape.center/detail/26898909
2020-07-13 01:49:24 [gerapy.pyppeteer] DEBUG: waiting for .item .name finished
2020-07-13 01:49:24 [gerapy.pyppeteer] DEBUG: wait for .item .name finished
2020-07-13 01:49:24 [gerapy.pyppeteer] DEBUG: close pyppeteer
2020-07-13 01:49:24 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://dynamic5.scrape.center/detail/26861389> (referer: https://dynamic5.scrape.center/page/1)
2020-07-13 01:49:24 [gerapy.pyppeteer] DEBUG: processing request <GET https://dynamic5.scrape.center/page/2>
2020-07-13 01:49:24 [gerapy.pyppeteer] DEBUG: set options {'headless': True, 'dumpio': False, 'devtools': False, 'args': ['--window-size=1400,700', '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']}
2020-07-13 01:49:25 [scrapy.core.scraper] DEBUG: Scraped from <200 https://dynamic5.scrape.center/detail/26861389>
{'name': '壁穴ヘブンホール',
 'score': '5.6',
 'tags': ['BL漫画', '小基漫', 'BL', '『又腐又基』', 'BLコミック']}
2020-07-13 01:49:25 [gerapy.pyppeteer] DEBUG: waiting for .item .name finished
2020-07-13 01:49:25 [gerapy.pyppeteer] DEBUG: crawling https://dynamic5.scrape.center/page/2
2020-07-13 01:49:26 [gerapy.pyppeteer] DEBUG: wait for .item .name finished
2020-07-13 01:49:26 [gerapy.pyppeteer] DEBUG: close pyppeteer
2020-07-13 01:49:26 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://dynamic5.scrape.center/detail/26855315> (referer: https://dynamic5.scrape.center/page/1)
2020-07-13 01:49:26 [gerapy.pyppeteer] DEBUG: processing request <GET https://dynamic5.scrape.center/detail/27047626>
2020-07-13 01:49:26 [gerapy.pyppeteer] DEBUG: set options {'headless': True, 'dumpio': False, 'devtools': False, 'args': ['--window-size=1400,700', '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']}
2020-07-13 01:49:26 [scrapy.core.scraper] DEBUG: Scraped from <200 https://dynamic5.scrape.center/detail/26855315>
{'name': '冒险小虎队', 'score': '9.4', 'tags': ['冒险小虎队', '童年', '冒险', '推理', '小时候读的']}
2020-07-13 01:49:26 [gerapy.pyppeteer] DEBUG: waiting for .item .name finished
2020-07-13 01:49:26 [gerapy.pyppeteer] DEBUG: crawling https://dynamic5.scrape.center/detail/27047626
2020-07-13 01:49:27 [gerapy.pyppeteer] DEBUG: wait for .item .name finished
2020-07-13 01:49:27 [gerapy.pyppeteer] DEBUG: close pyppeteer
...
```
