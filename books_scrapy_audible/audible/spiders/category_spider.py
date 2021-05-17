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
        '''This method collects all the top level
        Audible Categories from the Audible/Categories page.
        There are 23 root categories with 2-10 sub categories.
        The main category urls are passed to sub_category_parse.
        '''
        # Get all Main Categories from the Super Category boxes at the starting url
        audible_url = 'https://www.audible.com'
        
        main_category_element = response.xpath(".//div[contains(@class, 'singleCategoryContainer')]/h2/a")

        for main_cat in main_category_element:
            url = audible_url + main_cat.xpath("./@href").extract_first()
            cat_path = main_cat.xpath("./text()").extract()
            url_path_ = [url]
            yield Request(url = url, 
                          callback = self.sub_category_parse)
            
    def sub_category_parse(self, response):
        '''Each sub category page is parsed to yield the 
        parent category, the current category and 
        the url and number of titles at this level. 
        Then, if none of the sub-categories are in bold
        (indicating end of path), each sub-category is scraped and
        passed recursively to this function.
        '''
    
        audible_url = 'https://www.audible.com'
        
        #attempt to get patent category if avalible otherwise tag with Audible
        # as root. 
        try:
            parent_category = response.xpath(".//div[@id='center-0']//a[contains(@class,'parentCategoryUrl')]/text()").extract()[0]
            parent_url      = audible_url + response.xpath(".//div[@id='center-0']//a[contains(@class,'parentCategoryUrl')]/@href").extract()[0]
        except:
            parent_category = "Audible"
            parent_url      = "https://www.audible.com/categories"
            
     
        #get category name
        cat_name = response.xpath(".//div[@id = 'center-0']//h1/text()").extract()[0]

        #get number of titles and clean input
        cat_number = response.xpath(".//div[@id = 'center-0']//span/text()").extract()[0]
        cat_number = re.sub("[^0-9]", "", cat_number)
        
        #get Best Sellers list URL or "See all in __" URL as alternative.
        try:
            title_list_link = audible_url + response.xpath(".//a[contains(@aria-label, 'View all in Best sellers')][1]/@href").extract()[0]
        except:
            title_list_link = response.xpath(".//a[contains(@class,'allInCategoryPageLink')]/@href").extract()[0]
            title_list_link = audible_url + title_list_link
        
            
        #Create object and store information for CSV storage
        category_entry = CategoryItem() 
        category_entry['parent_category']     = parent_category
        category_entry['parent_url']          = parent_url
        category_entry['self_url']            = response.url
        category_entry['category_name']       = cat_name
        category_entry['category_numb_title'] = cat_number
        category_entry['title_list_url']      = title_list_link
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
                yield Request(url = url, 
                              callback = self.sub_category_parse)
        
