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
    'gerapy_pyppeteer.downloadermiddlewares.py.PyppeteerMiddleware': 543,
}
```

Others optional settings:

```python
# pyppeteer logging level
GERAPY_PYPPETEER_LOGGING_LEVEL = logging.WARNING

# pyppeteer timeout
GERAPY_PYPPETEER_DOWNLOAD_TIMEOUT = 30

# pyppeteer browser window
GERAPY_PYPPETEER_WINDOW_WIDTH = 1400
GERAPY_PYPPETEER_WINDOW_HEIGHT = 700

# pyppeteer settings
GERAPY_PYPPETEER_HEADLESS = True
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

## Example

For more detail, please see [example](./example).