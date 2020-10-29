# Gerapy Pyppeteer Changelog

## 0.0.12 (2020-10-30)

### Bug Fixes

* Fix bug about executablePath arg name

## 0.0.12 (2020-10-24)

### Bug Fixes

* Fix bug about crawling with Pyppeteer of normal Request

## 0.0.11 (2020-08-05)

### Bug Fixes

* Fix bug about `asyncio` in Python 3.8 on Windows [https://github.com/Gerapy/GerapyPyppeteer/issues/5](https://github.com/Gerapy/GerapyPyppeteer/issues/5)
* Fix bug of setting cookies [https://github.com/Gerapy/GerapyPyppeteer/issues/11](https://github.com/Gerapy/GerapyPyppeteer/issues/11)

### Features

* Add settings of `GERAPY_ENABLE_REQUEST_INTERCEPTION` [https://github.com/Gerapy/GerapyPyppeteer/issues/6](https://github.com/Gerapy/GerapyPyppeteer/issues/6)

## 0.0.10 (2020-08-01)

### Features

* Add `pretend` attribute for `PyppeteerRequest`, which can override `GERAPY_PYPPETEER_PRETEND`
* Add support for `dict` format of `wait_for` attribute of `PyppeteerRequest`

### Bug Fixes

* Change the priority of `request.meta.get('proxy')` and `pyppeteer_meta.get('proxy')`

## 0.0.9 (2020-07-31)

### Features

* Add support for screenshot

### Bug Fixes

* Fix bug of name `GERAPY_PYPPETEER_IGNORE_RESOURCE_TYPES`

## 0.0.8 (2020-07-26)

### Features

* Add support for pretending as real Browser instead of WebDriver

### Bug Fixes

* Fix bug of ValueError when `wait_until` is None
* Fix error position of log message about `wait_for`

## 0.0.7 (2020-07-25)

### Features

* Add meta info from PyppeteerRequest attributes

### Bug Fixes

* Skip validation of PyppeteerRequest

## 0.0.5 (2020-07-20)

### Features

* Add support for `ignoreHTTPSErrors`, `slowMo`, `ignoreDefaultArgs`,
`handleSIGINT`, `handleSIGTERM`, `handleSIGHUP`, `autoClose` args.

## 0.0.4 (2020-07-15)

### Bug Fixes

* Fix Bug of un-closing Pyppeteer when loaded failed

### Features

* Add support for `GERAPY_IGNORE_RESOURCE_TYPES`
* Add support for retrying