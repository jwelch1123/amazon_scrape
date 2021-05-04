# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import NotConfigured

#class ValidateItemPipeline(object):
#
#    def process_item(self, item, spider):
#        if not all(item.values()):
#            raise DropItem("Missing values!")
#        else:
#            return item


class WriteCategoryPipeline(object):

     
    def __init__(self):
        self.filename = 'category_hierarchy_n_urls.csv'
    
    @classmethod
    def from_crawler(cls,crawler):
        if not crawler.settings.getbool('WRITE_CATEGORY'):
            raise NotConfigured
        return cls()
     
    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()
    
     
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()

     
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class WriteTitlePipeline(object):

     
    def __init__(self):
        self.filename = 'title_information.csv'

    @classmethod
    def from_crawler(cls,crawler):
        if not crawler.settings.getbool('WRITE_TITLE'):
            raise NotConfigured
        return cls()
    
    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()

         
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()

         
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
