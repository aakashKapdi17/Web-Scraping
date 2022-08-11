import scrapy
from scrapy_splash import SplashRequest

class BeerSpider(scrapy.Spider):
    name='beer'
    
    def start_requests(self):
        url="https://www.beerwulf.com/en-gb/c/mixedbeercases"
        
        yield SplashRequest(url=url,callback=self.parse)
    
    def parse(self,response):
        products=response.xpath("//div[@id='product-items-container']")
        
        for item in products:
            yield{
                'name':item.xpath("//div[@class='product-title-container']/h4/text()").extract(),
                'price':item.xpath("//span[@class='price']/text()").extract()
            }