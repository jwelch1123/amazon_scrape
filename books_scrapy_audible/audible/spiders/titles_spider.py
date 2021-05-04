# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from audible.items import TitleItem
import re
import pandas as pd

class TitleSpider(Spider):
    name = 'title_spider'
    allowed_urls = ['https://www.audible.com']
    start_urls = ['https://www.audible.com/categories']
    custom_settings = {'WRITE_TITLE':True}


    def parse(self, response):
        category_csv = pd.read_csv("category_hierarchy_n_urls.csv")        

        url_list = category_csv.title_list_url
        
        
        for url in url_list[0:2]:
            print("*"*60)
            print(url)
            print("*"*60)
            yield Request(url=url, callback=self.title_list_parse)
            
    def title_list_parse(self, response):
        audible_url = 'https://www.audible.com'
        
        
        title_cards = response.xpath(".//li[contains(@class,'productListItem')]")
        
        title_category = response.xpath(".//div[@id='top-3']//h1[contains(@class,'bc-heading')]/text()").extract()[0]
        title_category = title_category.replace("\n","").replace("Showing titles in ","")
        
        for title_card in title_cards:
            
            # Title and Title page URL, some data loss in title name due to translation
            title_url          = title_card.xpath(".//li/h3/a/@href").extract()[0]
            title_url          = audible_url + title_url
            title_title        = title_card.xpath(".//li/h3/a/text()").extract()[0]
            
            # Attempt to get subtitle if avalible, data loss due to translation
            try:
                title_subtitle     = title_card.xpath(".//li[contains(@class,'subtitle')]/span/text()").extract()[0]
            except:
                title_subtitle     = ""
                
            # Returns a list to capture all names, data loss due to translation
            title_author       = title_card.xpath(".//li[contains(@class,'authorLabel')]//a/text()").extract()
            
            # Returns a list to capture all names, data loss due to translation
            title_narrator     = title_card.xpath(".//li[contains(@class,'narratorLabel')]//a/text()").extract()
            
            
            # Get title length and remove the leading string
            title_length       = title_card.xpath(".//li[contains(@class,'runtimeLabel')]/span/text()").extract()[0]
            title_length       = title_length.replace("Length: ","")
            
            # Modifying the format, converting the text into minutes.
            # Common formats
            #   "4 hrs and 20 mins"
            #   "40 mins"
            #   "Less than 1 minute"
            # Regex will match any numbers and either "h" or "min" 
            # If statement excludes "Less than 1 minute" string.
            if "Less than" in title_length:
                title_length   = 1

            else:
                try:
                    hours = re.sub("[^0-9]", "", re.findall(r"\d+ h",title_length)[0])
                except:
                    hours = 0
                try:
                    minutes = re.sub("[^0-9]", "", re.findall(r"\d+ min",title_length)[0])
                except:
                    minutes = 0

                hours = pd.to_numeric(hours) * 60
                minutes = pd.to_numeric(minutes)

                title_length = hours +  minutes
            
            # Get the Release date, includes future dates.
            title_release_date = title_card.xpath(".//li[contains(@class,'releaseDateLabel')]/span/text()").extract()[0]
            title_release_date = title_release_date.replace("Release date:","").replace("\n","").replace(",","").strip()
            
            # Get the Language of the book, might be character loss due to translation
            title_language     = title_card.xpath(".//li[contains(@class,'languageLabel')]/span/text()").extract()[0]
            title_language     = title_language.replace("Language:","").replace("\n","").strip()
            
            #Star and number of Ratings combined to take advantage of star xpath throwing error
            try:
                title_star_rating  = title_card.xpath(".//li[contains(@class,'ratingsLabel')]/span[contains(@class,'bc-pub-offscreen')]/text()").extract()[0]
                title_star_rating  = title_star_rating.replace(" out of 5 stars","")
                
                title_count_rating = title_card.xpath(".//li[contains(@class,'ratingsLabel')]/span[contains(@class,'bc-size-small')]/text()").extract()[0]
                title_count_rating = re.sub("[^0-9]", "", title_count_rating)
                
            except:
                title_star_rating  = ""
                title_count_rating = ""            
            
            # Get Price and formate to numbers with decimal.
            title_price        = title_card.xpath(".//p[contains(@class,'buybox-regular-price')]/span[2]/text()").extract()[0]
            title_price        = title_price.strip().replace("$","")
            
            
            # Write and yield object
            title_entry = TitleItem()
            title_entry["title_category"] = title_category
            title_entry["title_url"] = title_url
            title_entry["title"] = title_title
            title_entry["subtitle"] = title_subtitle
            title_entry["author"] = title_author
            title_entry["narrator"] = title_narrator
            title_entry["length"] = title_length
            title_entry["release_date"] = title_release_date
            title_entry["language"] = title_language
            title_entry["star_rating" ] = title_star_rating
            title_entry["count_rating"] = title_count_rating
            title_entry["price"] = title_price
            
            yield(title_entry)
            print("*"*60)
            print("YIELD ITEM")
            print("*"*60)
            
        # Get the Next Page button element and check if it has a disabled tag
        next_button_element = response.xpath(".//ul[contains(@class,'pagingElements')]//span[contains(@class,'nextButton')]")
        disabled_next_button = next_button_element.xpath("./a[@aria-disabled='true']")
        
        # If the button is not disabled, create the next page url and run a recursive call with this function. 
        if disabled_next_button == []:
            next_button_url = next_button_element.xpath(".//a/@href").extract()[0]
            next_button_url = audible_url + next_button_url
            yield Request(url = next_button_url, callback = self.title_list_parse)
        