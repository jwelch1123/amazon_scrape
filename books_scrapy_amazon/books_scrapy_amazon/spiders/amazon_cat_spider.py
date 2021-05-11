# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from books_scrapy_amazon.items import CategoryAmazonItem
import re

class amazon_cat_spider(Spider):
    name            = 'amazon_cat_spider'
    allowed_urls    = ['https://www.amazon.com']
    start_urls      = ['https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155&dc&fs=true&qid=1620260821&ref=sr_ex_n_1']
    custom_settings = {'WRITE_CATEGORY':True}

    def parse(self, response):
        '''Get list of sub_category URLs and recursively pass 
        them to this method. At each level, create an item showing
        superior and sub categories.
        '''
        amazon_url = 'https://www.amazon.com'
     
        # Get list of categories for manipulation
        avalible_categories_elements = response.xpath(".//div[@id = 'departments']/ul")
        
        # get information and clean
        current_cat   = avalible_categories_elements.xpath(".//span[contains(@class,'a-text-bold')]/text()").extract()[0]
        superior_cats = avalible_categories_elements.xpath(".//span[contains(@class,'s-back-arrow')]/../span/text()").extract()
        if superior_cats == []:
            superior_cats = "Amazon"
        sub_cats      = avalible_categories_elements.xpath("./li[contains(@class,'s-navigation-indent')]//a/span/text()").extract()
        
        # Create ITEM
        categoryItem = CategoryAmazonItem()
        categoryItem["current_cat"]    = current_cat
        categoryItem["current_url"]    = response.url
        categoryItem["superior_cats"]  = superior_cats
        categoryItem["sub_cats"]       = sub_cats
        yield(categoryItem)
        
        
        # Get avalible subcategories
        avalible_cat_urls = avalible_categories_elements.xpath("./li[contains(@class,'s-navigation-indent')]//@href").extract()
        
        # If there are sub_categories, send them to this method.
        if avalible_cat_urls != []: 
            for cat_url in avalible_cat_urls:
                url = amazon_url + cat_url
                yield Request(url = url, callback = self.parse)
        