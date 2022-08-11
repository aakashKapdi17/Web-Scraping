#packages
import json
from requests import head
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
from datetime import date

import urllib3

# OnTheMarket scraper class
class CommercialSale(scrapy.Spider):
    # spider name
    name='onthemarket'
    
    #base URL
    base_url='https://www.onthemarket.com/for-sale/commercial/property/'
    
    # search query parameters
    params={
        'page':'0',
        'radius':'3.0'
        
    }
    
    # headers
    headers={
       'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    
    #custom download settings
    custom_settings = {
        #uncomment to set accordingly
        #'CONCURRENT_REQUESTS_PER_DOMAIN':1,
        #'DOWNLOAD_TIMEOUT':0.25  #250 ms of delay
    }
    
    #current page
    current_page = 1
    
    #postcodes list
    postcodes = []
    
    #constuctor init
    def __init__(self):
        
        # Reading postcodes file
        with open('onthemarket\postcode-outcodes.csv','r') as fh:
            data=fh.readlines()
            
        # populating the postcodes list    
        for line in data:
            temp=line.split(",")
            if temp[0].isnumeric():
                self.postcodes.append(temp[1].lower())
                
    # general crawler 
    def start_requests(self):
        
        #define filename
        filename='./onthemarket/Output/Commercial_sale'+date.today().strftime("%Y/%m/%Y %H:%M:%S")+'.json'
        
        #postcodes count
        count=1
        
        # loop over postcodes
        for postcode in self.postcodes:
            self.current_page=0
            next_postcode=self.base_url+postcode+'/?'+ urllib.parse.urlencode(self.params)
            yield scrapy.Request(url=next_postcode,headers=self.headers,meta={'postcode':postcode,'filename':filename,'count':count},callback=self.parse_links)
            count+=1
            break
        
    # Parse Property Links
    def parse_links(self,response):
        # extract forwarded data
        postcode=response.meta.get('postcode')
        filename=response.meta.get('filename')
        count=response.meta.get('count')
        print(postcode,filename,count)
        
        # print verbose debug info
        print('\n\nPostcode %s:%s out of %s postcodes'%(postcode,count,len(self.postcodes)))
          
        # loop over property cards
        cards=response.xpath("//li[@class='otm-PropertyCard']")
        for card in cards:
            listing=card.xpath("div/div[@class='otm-PropertyCardMedia']//a/@href").get()
            yield response.follow(url=listing,headers=self.headers,meta={'postcode':postcode,'filename':filename,'count':count},callback=self.parse_listing)
            break
        
    # Parse property listings
    def parse_listing(self,response):
        # extract forwarded data
        postcode=response.meta.get('postcode')
        filename=response.meta.get('filename')
        
        #extracting features
        features={
            'id':'',
            'postcode':postcode,
            'title':response.xpath("//h1/text()").get(),
            'Address':response.xpath("//h1/following-sibling::div[1]/text()").get(),
            'price': response.xpath("//section[@class='main-col']//div[@class='otm-Price']/*/text()").extract()[-1].split("|")[0],
            'feature_list':response.xpath("//section[@class='otm-FeaturesList mb-12']//li/text()").extract(),
            'photo_links':response.xpath("//li/picture/img/@src").extract()
     #       'description':response.xpath("//div[@class='description-truncate']/div/*[descendant::text()]/text()").extract()
        }
        
        print(json.dumps(features,indent=2))
        
                
# main driver

if __name__=='__main__':
    #run scraper
    process=CrawlerProcess()
    process.crawl(CommercialSale)
    process.start()        