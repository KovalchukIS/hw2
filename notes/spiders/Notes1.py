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

class NotesSpider(CrawlSpider):
    name = "notebooks"
    allowed_domains = ['citilink.ru']
    start_urls = ["https://www.citilink.ru/catalog/noutbuki/?view_type=list"]

    rules = (
           Rule(LinkExtractor(allow=(r'p=\d+',)), callback='scrap_notes'),)

    def scrap_notes(self, response):
        for card in response.xpath('//div[@class="product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist"]'):
            try:
                names,vols = [],[]
                for i in card.xpath('.//span[@class="ProductCardHorizontal__properties_name"]//text()[normalize-space()]'):
                    names.append(i.get().replace(':','').lower().strip())
                for j in card.xpath('.//span[@class="ProductCardHorizontal__properties_value"]//text()[normalize-space()]'):
                    vols.append(j.get().replace(';','').lower().strip())
                _dict = dict(zip(names,vols))
                
                Item = NotesItem()
                
                Item['cpu'] = float(_dict["процессор"].split("ггц")[0].strip(" ").split(" ")[-1])
                Item['ram'] = int(_dict["оперативная память"].split("гб")[0].strip(" "))
                Item['disk'] = (re.findall(r'[a-z]+',_dict['диск'])[0])
                Item['disk_vol'] = int(re.findall(r'\d+',_dict['диск'])[0])
                
                Item['visited_at'] = datetime.datetime.now()
                Item['ecname'] = card.xpath(".//a[@class='ProductCardHorizontal__title  Link js--Link Link_type_default']").attrib.get('title')
                Item['price_rub'] = int(card.attrib.get('data-price'))
                Item['url'] = 'http://citilink.ru'+card.xpath(".//a").attrib.get('href')
                Item['rank']= Item['cpu']*10+Item['ram']*10+Item['price_rub']*-0.0001
                yield Item
            except:
                print('Не получилось вытащить характеристики')
            
