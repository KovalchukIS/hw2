# -*- coding: utf-8 -*-

#import scrapy
#from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkExtractor

#from scrapy.loader.processors import TakeFirst, Identity
#from scrapy.loader import ItemLoader
#from scrapy.selector import HtmlXPathSelector, Selector

from notes.items import NotesItem

import scrapy

from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import datetime

class NotesSpider2(CrawlSpider):
    name = 'notebooks2'
    allowed_domains = ['notik.ru']
    start_urls = ["https://www.notik.ru/index/notebooks.htm?srch=true&full="]
    
    rules = (
           Rule(LinkExtractor(allow=(r'&page=\d+',)), callback='parse_item'),)

    def parse_item(self, response):
        for card in response.xpath("//tr[@class='goods-list-table']"):
            _selector  = card.xpath(".//td[@class='glt-cell w4']//text()[normalize-space()]")
            Item = NotesItem()
            Item['cpu'] = int(re.findall(r'\d+',_selector[3].get())[0])/1000
            Item['ram'] = int(re.findall(r'\d+',_selector[4].get())[0])
            Item['disk'] = _selector[6].get()
            Item['disk_vol'] = int(re.findall(r'\d+',_selector[7].get())[0])
            price_selector = card.xpath(".//td[@class='glt-cell gltc-cart']")
            Item['visited_at'] = datetime.datetime.now()
            Item['ecname'] = price_selector.xpath(".//a").attrib.get("ecname")
            Item['price_rub'] = int(price_selector.xpath(".//a").attrib.get("ecprice"))
            Item['url'] = 'http://notik.ru'+card.xpath(".//td[@class='glt-cell gltc-title show-mob hide-desktop']//a").attrib.get('href')
            Item['rank']= Item['cpu']*10+Item['ram']*10+Item['price_rub']*-0.0001
            yield Item
            
