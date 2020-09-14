import scrapy
from scrapy.crawler import CrawlerProcess

from config import DATA_PATH, SAVE_PAGE
from gumtree.spiders.listing_spider import ListingSpider
from helpers import get_urls, make_directory

path = DATA_PATH
urls = get_urls(path)
path = make_directory(dirtype='listings', path=path)

process = CrawlerProcess({
    'BOT_NAME': 'gumtree',
    'SPIDER_MODULES': ['gumtree.spiders'],
    'NEWSPIDER_MODULE': 'gumtree.spiders',
    'ROBOTSTXT_OBEY': True,
    'DOWNLOAD_DELAY': 5,
    'FEED_URI': f'{path}/data.csv',
    'FEED_FORMAT': 'csv',
})

process.crawl(ListingSpider, urls=urls, path=path, save_page=SAVE_PAGE)
process.start()     
