import scrapy
from scrapy.crawler import CrawlerProcess

from gumtree.spiders.listing_spider import ListingSpider
from helpers import get_urls, make_directory
from config import DATA_PATH

path = DATA_PATH
urls = get_urls(path)
path = make_directory(dirtype='listings', path=path)

process = CrawlerProcess({
    'BOT_NAME': 'gumtree',
    'SPIDER_MODULES': ['gumtree.spiders'],
    'NEWSPIDER_MODULE': 'gumtree.spiders',
    'ROBOTSTXT_OBEY': True,
    'DOWNLOAD_DELAY': 3,
    'FEED_URI': f'{path}/data.csv',
    'FEED_FORMAT': 'csv',
})

# url = ['https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/krakow/komfortowe-2-pokoje-%252B-balkon-ekspozycja-zachodnia/1007770548020912567790009']
# process.crawl(ListingSpider, urls=url, path=path)

process.crawl(ListingSpider, urls=urls, path=path)
process.start()     