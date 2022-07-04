from gc import callbacks
import scrapy
from whiskeyShop.items import WhiskeyshopItem
from scrapy.loader import ItemLoader

class WhiskeySpider(scrapy.Spider):
    name='whiskey'
    start_urls=['https://www.whiskyshop.com/single-malt-scotch-whisky']


    def parse(self,response):

        

        for product in  response.css('div.product-item-info'):

            l=ItemLoader(item=WhiskeyshopItem(),selector=product)
            l.add_css('name','a.product-item-link')
            l.add_css('price','span.price')
            l.add_css('link','a.product.photo.product-item-photo::attr(href)')

        
                
            yield l.load_item()
    
            next_page=response.css('a.action.next').attrib['href']
            if next_page is not None:
                yield response.follow(next_page,callback=self.parse)