import scrapy

class LinkSpider(scrapy.Spider):
    """
    Download search results from 
    Gumtree, store pages and extract links.
    """

    name = 'gumtree-links'

    def __init__(self, n_pages, path, *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.n_pages = n_pages
        self.path = path

    def start_requests(self):

        urls = []                    
        for i in range(1, self.n_pages + 1):
            url = f'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/krakow/page-{i}/v1c9073l3200208p{i}'
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        url = response.url.split('/')[-2]
        page_path = f'{self.path}/pages/{url}.html'
        links_path = f'{self.path}/{url}.txt'

        # Save page
        self.log(f'Saving page to {page_path}.')
        with open(page_path, 'wb') as f:
            f.write(response.body)
        
        # Extract links to listings
        listings = response.xpath("//div[@class='title']/a/@href").extract()        

        # Save links
        self.log(f'Saving links to {links_path}.')
        with open(links_path, 'w') as f:
            for link in listings:
                full_link = 'https://www.gumtree.pl' + link        
                f.write(full_link)
                f.write('\n')