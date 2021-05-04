# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import re
from audible.items import CategoryItem


class category_spider(Spider):
    name = 'category_spider'
    allowed_urls = ['https://www.audible.com']
    start_urls = ['https://www.audible.com/categories']
    audible_url = 'https://www.audible.com'
    custom_settings = {'WRITE_CATEGORY':True}
    
    def parse(self, response):

        # Get all Main Categories from the Super Category boxes at the starting url
        audible_url = 'https://www.audible.com'
        category_boxes = response.xpath(".//div[contains(@class, 'singleCategoryContainer')]")
        main_categories = []
        for box in category_boxes:
            category_urls = box.xpath("./h2/a/@href").extract()
            for cat_url in category_urls:
                main_categories.append(audible_url+cat_url)
                
        
        for main_cat in main_categories:
            yield Request(url = main_cat, callback = self.sub_category_parse)

            
    def sub_category_parse(self, response):
        audible_url = 'https://www.audible.com'
        
        #attempt to get patent category if avalible otherwise tag with Audible
        # as root. 
        try:
            parent_category = response.xpath(".//div[@id='center-0']//a[contains(@class,'parentCategoryUrl')]/text()").extract()[0]  
        except:
            parent_category = "Audible"
     
        #get category name
        cat_name = response.xpath(".//div[@id = 'center-0']//h1/text()").extract()[0]

        #get number of titles and clean input
        cat_number = response.xpath(".//div[@id = 'center-0']//span/text()").extract()[0]
        cat_number = re.sub("[^0-9]", "", cat_number)
        
        #get Best Sellers list URL
        title_list_link = audible_url + response.xpath(".//a[contains(@aria-label, 'View all in Best sellers')][1]/@href").extract()[0]
        
        #Create object and store information for CSV storage
        category_entry = CategoryItem() 
        category_entry['parent_category'] = parent_category
        category_entry['self_url'] = response.url
        category_entry['category_name'] = cat_name
        category_entry['category_numb_title'] = cat_number
        category_entry['title_list_url'] = title_list_link
        # should probably get category book values for estimates. 
        
        yield(category_entry)
        
        #Detects if any of the Sub-categories have a bold text, indicating no further sub-categories.
        sub_cat_bold = response.xpath(".//div[@id='center-0']//ul[contains(@class,'bc-list')]//span[contains(@class,'bc-text-bold')]")
        
        #Sub-category url list for current page
        sub_cat_list = response.xpath(".//div[@id='center-0']//ul[contains(@class,'bc-list')]//li[@class='bc-list-item']/a/@href").extract()
        
        #If there are no bold sub-categories, for each sub category 
        # request page and scrapy with sub_category_parse.
        if sub_cat_bold == []:
            for sub_cat in sub_cat_list:
                url = audible_url + sub_cat
                yield Request(url = url, callback = self.sub_category_parse)
        
