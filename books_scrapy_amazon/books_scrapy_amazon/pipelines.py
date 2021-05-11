# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import NotConfigured
    
    
class CatScrapyAmazonPipeline(object):
     
    def __init__(self):
        self.filename = 'amazon_category.csv'
    
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


class TitleScrapyAmazonPipeline(object):

    def __init__(self):
        self.filename = 'amazon_titles.csv'

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