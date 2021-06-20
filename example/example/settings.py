BOT_NAME = 'example'

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'gerapy_pyppeteer.downloadermiddlewares.PyppeteerMiddleware': 543,
}

RETRY_HTTP_CODES = [403, 500, 502, 503, 504]

GERAPY_PYPPETEER_HEADLESS = True

LOG_LEVEL = 'DEBUG'

GERAPY_PYPPETEER_PRETEND = False

GERAPY_PYPPETEER_SCREENSHOT = {
    'type': 'png',
    'fullPage': True
}

GERAPY_PYPPETEER_DOWNLOAD_TIMEOUT = 10
