# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from books_scrapy_amazon.items import CategoryAmazonItem
import re
from scraper_api import ScraperAPIClient

client = ScraperAPIClient("6a2b42189b564d94c1df3037d1050188")


class amazon_cat_spider(Spider):
    name            = 'amazon_cat_spider'
    allowed_urls    = ['https://www.amazon.com']
    start_urls      = ['https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155&dc&fs=true&qid=1620260821&ref=sr_ex_n_1']
    custom_settings = {'WRITE_CATEGORY':True}
    session_ID = 1

    def parse(self, response):
        '''Get list of sub_category URLs and recursively pass 
        them to this method. At each level, create an item showing
        superior and sub categories.
        '''     
        amazon_url = 'https://www.amazon.com'
        
        bot_check_tag = response.xpath(".//form[@action = '/errors/validateCaptcha']")
        
        if bot_check_tag:
            print("*"*100)
            print("*"*100)
            print("*"*100)
            self.session_ID = self.session_ID+1
            yield Request(client.scrapyGet(url=response.url, session_number= self.session_ID), callback=self.parse)
            
     
        # Get list of categories for manipulation
        try:
            avalible_categories_elements = response.xpath(".//div[@id = 'departments']/ul")
        except:
            avalible_categories_elements = ""
            
        # get information and clean
        try:
            current_cat   = avalible_categories_elements.xpath(".//span[contains(@class,'a-text-bold')]/text()").extract()[0]
        except:
            current_cat   = ""
        
        
        try:
            superior_cats = avalible_categories_elements.xpath(".//span[contains(@class,'s-back-arrow')]/../span/text()").extract()
            if superior_cats == []:
                superior_cats = "Amazon"
        except:
            superior_cats = ""
            
        # List of categories below current level
        try:
            sub_cats      = avalible_categories_elements.xpath("./li[contains(@class,'s-navigation-indent')]//a/span/text()").extract()
        except:
            sub_cats      = ""
            
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
                yield Request(client.scrapyGet(url=url, 
                                     session_number = self.session_ID),
                                     callback=self.parse)
        