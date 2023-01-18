# -*- coding: utf-8 -*-
# 
# # Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Float, DateTime
from sqlalchemy.orm import Session
import os
from notes.items import NotesItem
from scrapy.exceptions import DropItem



Base = declarative_base()

class NotesTable(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    visited_at = Column(DateTime)
    ecname = Column(String)
    cpu = Column(Float)
    ram = Column(Integer)
    disk = Column(String)
    disk_vol = Column(Integer)
    price_rub = Column(Integer)
    rank = Column(Float)
    
    
    def __init__(self, url, visited_at, ecname, cpu, ram, disk, disk_vol, price_rub, rank):
        self.url = url
        self.visited_at = visited_at
        self.ecname = ecname
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.disk_vol = disk_vol
        self.price_rub = price_rub
        self.rank = rank

    def __repr__(self):
        return "<Data %s, %s, %s, %s, %s, %s, %s, %s, %s>" % \
            (self.url, self.visited_at, self.ecname, self.cpu, self.ram, self.disk, self.disk_vol, self.price_rub, self.rank)


class NotesPipeline(object):
    def __init__(self):
        basename = 'notes.sqlite'
        self.engine = create_engine("sqlite:///./%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)
        

    def process_item(self, item, spider):
        dt = NotesTable(item['url'],item['visited_at'], item['ecname'], item['cpu'], item['ram'], item['disk'], item['disk_vol'], item['price_rub'], item['rank'])
        self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)



