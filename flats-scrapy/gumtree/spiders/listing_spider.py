import re
import scrapy
from random import shuffle

class ListingSpider(scrapy.Spider):
    """
    Download listing information.
    """
    
    name = 'gumtree-listings'

    def __init__(self, urls, path, save_page, *args, **kwargs):
        super(ListingSpider, self).__init__(*args, **kwargs)
        self.urls = urls
        self.path = path
        self.save_page = save_page

    def start_requests(self):

        self.log(f'Fetching {len(self.urls)} listings.')

        shuffle(self.urls)

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """

        Extract information about property.

        Notes
        -----
        The website is in polish and needs
        to be translated to english. It will be
        translated as follows:

        Cena -> Price
        Lokalizacja -> Location
        Data dodania -> Date added
        Na sprzedaż przez -> Seller type
        Rodzaj nieruchomości -> Property type
        Liczba pokoi -> Number of rooms
        Liczba łazienek -> Number of bathrooms
        Wielkość (m2) -> Total area
        Parking -> Parking
        Tytuł -> Title
        Opis -> Description

        """

        url = response.url.split('/')[-2]
        filename = f'{self.path}/pages/{url}.html'
        if self.save_page:
            with open(filename, 'wb') as f:
                f.write(response.body)
                
        data = {'Cena': None,
                'Lokalizacja': None,
                'Data dodania': None,
                'Na sprzedaż przez': None,
                'Rodzaj nieruchomości': None,
                'Liczba pokoi': None,
                'Liczba łazienek': None,
                'Wielkość (m2)': None,
                'Parking': None,
                'Tytuł': None,
                'Opis': None,
                'Link': None}

        # Save link
        data['Link'] = response.url

        # Extract price
        price = response.xpath("//span[@class='amount']/text()").extract()
        if isinstance(price, list):
            if price:
                price = price[0]
                price = price.strip()
        else:
            price = None
        data['Cena'] = price

        # Extract listing title
        title = response.xpath("//span[@class='myAdTitle']/text()").extract()
        if isinstance(title, list):
            if title:
                title = title[0]
                title = re.sub(r'[^\w\s]', '', title)
                title = title.lower()
        else:
            title = None            
        data['Tytuł'] = title

        # Extract address
        address = response.xpath("//span[@class='address']/text()").extract()
        if isinstance(address, list):
            if address:
                address = address[0]
                address = address.strip()
        else:
            address = None
        data['Lokalizacja'] = address

        desc = response.xpath("//span[@class='pre']/text()").extract()
        if isinstance(desc, list):
            if desc:
                desc = desc[0]       
                desc = re.sub(r'[^\w\s]', ' ', desc)                
                desc = desc.replace('\n', ' ')
                desc = desc.replace('\r', ' ')
                desc = desc.replace('\xa', ' ')
                desc = desc.lower()

        data['Opis'] = desc

        # Extract other attributes
        divs = response.xpath("//div[@class='attribute']")
        if divs:
            for div in divs:
                if div:
                    name = div.xpath(".//span[@class='name']/text()")
                    value = div.xpath(".//span[@class='value']/text()")                
                    if name and value:
                        name = name[0]
                        value = value[0]
                        name = name.extract().strip()
                        value = value.extract().strip()                        
                        if name in data:
                            data[name] = value
                        else:
                            continue

        yield data