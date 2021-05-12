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
        #header = {
        #"Connection": "keep-alive",
        #"Upgrade-Insecure-Requests": "1",
        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #"Sec-Fetch-Site": "same-origin",
        #"Sec-Fetch-Mode": "navigate",
        #"Sec-Fetch-User": "?1",
        #"Sec-Fetch-Dest": "document",
        #"Referer": "https://www.google.com/",
        #"Accept-Encoding": "gzip, deflate, br",
        #"Accept-Language": "en-US,en;q=0.9"
    #}
        
        
        amazon_url = 'https://www.amazon.com'
        
        bot_check_tag = response.xpath(".//form[@action = '/errors/validateCaptcha']")
        
        if bot_check_tag:
            print("*"*100)
            print("*"*100)
            print("*"*100)
            print("THEY GOT ME")
            print("*"*100)
            print("*"*100)
            print("*"*100)
     
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
                yield Request(url = url, callback = self.parse, header = header)
        