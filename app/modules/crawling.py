from app import *
from urllib.request import urlopen
from bs4 import BeautifulSoup


logger=setup_logger(name="crawling")


def crawlLoggingTest():
    logger.info(f"crawl logging test success")
     
