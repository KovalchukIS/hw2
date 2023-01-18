# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class NotesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    visited_at = Field()
    ecname = Field()
    cpu = Field()
    ram = Field()
    disk = Field()
    disk_vol = Field()
    price_rub = Field()
    rank = Field()
