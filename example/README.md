# Gerapy Pyppeteer Example

## Run

There are two ways to run this example:

### Run with Python

```shell script
pip3 install -r requierments.txt
pyppeteer-install
python3 run.py
```

### Run with Docker

```shell script
docker run germey/gerapy-pyppeteer-example
```

If you want to build your own docker image, please remember to set:

```python
GERAPY_PYPPETEER_HEADLESS = True
GERAPY_PYPPETEER_NO_SANDBOX = True (default is True)
```

In your settings.py file.

Otherwise, it won't works well.
