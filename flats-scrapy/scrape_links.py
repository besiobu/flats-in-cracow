import scrapy
from scrapy.crawler import CrawlerProcess

from config import DATA_PATH
from gumtree.spiders.link_spider import LinkSpider
from helpers import make_directory

path = DATA_PATH

path = make_directory(dirtype='urls', path=path)

process = CrawlerProcess({
    'BOT_NAME': 'gumtree',
    'SPIDER_MODULES': ['gumtree.spiders'],
    'NEWSPIDER_MODULE': 'gumtree.spiders',
    'ROBOTSTXT_OBEY': True,
    'DOWNLOAD_DELAY': 3
})

process.crawl(LinkSpider, n_pages=50, path=path)
process.start() 