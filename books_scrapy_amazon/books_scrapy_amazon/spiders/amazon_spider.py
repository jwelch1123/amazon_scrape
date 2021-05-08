# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from books_scrapy_amazon.items import BooksScrapyAmazonItem
import re

class AmazonSpider(Spider):
    name = 'amazon_spider'
    allowed_urls = ['https://www.amazon.com']
    start_urls = ['https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155&dc&fs=true&qid=1620260821&ref=sr_ex_n_1']

    def parse(self, response):
        '''
        Documentation
        
        '''
        amazon_url = 'https://www.amazon.com'
        avalible_categories_elements = response.xpath(".//div[@id = 'departments']//li[contains(@class,'s-navigation-indent')]")
        avalible_cat_urls = avalible_categories_elements.xpath(".//@href").extract()
        
        current_category = avalible_categories_elements.xpath(".//span[contains(@class, 'a-text-bold')]/text()").extract()[0]
        
        yield Request(url = response.url, callback = self.title_url_collection)
        
        #if avalible_cat_urls != []:
        #    # for object, if it has a url? how do i get parent 
        #    for cat_url in avalible_cat_urls:
        #        url = amazon_url + cat_url
        #        yield Request(url = url, callback = self.parse)
        
        
        
    def title_url_collection(self, response):
        '''Scrape all...
        
        Each url is passed to the title_info_collection method.
        '''
    
        amazon_url = 'https://www.amazon.com'
        
        book_url_elements = response.xpath(".//div[contains(@class,'s-main-slot')]/div[contains(@data-component-type,'s-search-result')]//div[contains(@class,'a-section a-spacing-none')]//a")
            
        for page_link in book_url_elements:
            url_text = page_link.xpath("./text()").extract_first()
            url_link  = page_link.xpath("./@href").extract_first()
            
            if url_text in ["Hardcover","Paperback"]:
                url = amazon_url + url_link
                yield Request(url = url, callback = self.title_info_collection, meta= {'type':url_text})
            
        next_button = response.xpath(".//li[contains(@class,'a-last')]//@href").extract()
        
        if next_button != []:
            url = amazon_url + next_button[0]
            yield Request(url=url, callback = self.title_url_collection)

        
        
    def title_info_collection(self, response):
        '''Collect information from each title
        ###
        '''
        amazon_url = 'https://www.amazon.com'
        
        
        try:
            title_category = response.xpath(".//div[@id = 'wayfinding-breadcrumbs_feature_div']/ul/li/span/a/text()").extract()
            title_category = [cat.strip() for cat in title_category]
        except:
            title_category = ""

        title_url = response.url

        title_subtitle = response.xpath(".//span[@id= 'productTitle']/text()").extract()[0].strip().split(": ", 1)
        title          = title_subtitle[0]
        try:
            subtitle  = title_subtitle[1]
        except:
            subtitle  = ""

        # using author[0] to throw an error with an empty list.
        # I need the list to capture multiple authors.
        author_list_element = response.xpath(".//div[@id='bylineInfo']/span[contains(@class, 'author')]")
        author = []
        for author_element in author_list_element:
            try:
                author_text = author_element.xpath("./a/text()").extract_first()
                author_text[0]
                author.append(author_text)
            except:
                pass
            try:
                author_text = author_element.xpath("./span/a[contains(@class,'contributorNameID')]/text()").extract_first()
                author_text[0]
                author.append(author_text)
            except:
                pass
            
                    
        try:
            author_role = response.xpath(".//div[@id='bylineInfo']//span[@class = 'contribution']/span/text()").extract()
            #"(Author)"
            #"(Author, Ilustration)"
            #"(Author), "
            #author_role = [role.replace(", ","").replace("(","").replace(")","") for role in author_role]
            author_role = [role.replace("), ",")") for role in author_role]
        except:
            author_role = ""


        if author == [] and (author_role == [] or author_role == ""):
            try:
                author = response.xpath(".//div[contains(@class,'authorNameColumn')]/a/text()").extract()
                author = [s.strip() for s in author]
                if isinstance(author,list):
                    author_role = ["Author"] * len(author)
                else:
                    author_role = "Author"
            except:
                author = []
                author_role = []
            

        info_element     = response.xpath(".//div[@id='detailBulletsWrapper_feature_div']/div[@id='detailBullets_feature_div']/ul/li")
        try:
            print_length = info_element.xpath(".//span[contains(text(),'pages')]/text()").extract_first()
            print_length = re.sub("[^0-9]", "", print_length)
        except:
            print_length = ""

        try:
            book_volume = info_element.xpath(".//span[contains(text(),'inches')]/text()").extract_first()
            book_volume = book_volume.replace(" inches","")
        except:
            book_volume = ""

        try:
            release_date = info_element.xpath(".//span[contains(text(),'Publisher')]/../span[2]/text()").extract_first()
            release_date = release_date.rsplit("(",1)[1].replace(")","")
        except:
            try:
                release_date = response.xpath(".//span[@id = 'productSubtitle']/text()").extract_first()
                release_date = release_date.split("– ")[1]
            except:
                release_date = ""

        try:
            language = info_element.xpath(".//span[contains(text(),'Language')]/../span[2]/text()").extract()[0]
            language = language.strip()
        except:
            language = ""

        try:
            star_rating = response.xpath(".//div[@id ='averageCustomerReviews']//a/i/span/text()").extract()[0]
            star_rating = star_rating.replace(" out of 5 stars","")

            count_rating = response.xpath(".//div[@id ='averageCustomerReviews_feature_div']//span[@id = 'acrCustomerReviewText']/text()").extract()[0]
            count_rating = re.sub("[^0-9]", "", count_rating)

        except:
            star_rating = ""
            count_rating = ""


        table_element = response.xpath(".//div[@id='twister']/div[contains(@class,'top-level')]")

        #Setting Defaults for these values
        audible_flag = ""
        hard_price   = ""
        paper_price  = ""

        for row in table_element:

            media_type   = row.xpath(".//td[@class = 'dp-title-col']//span/text()").extract()
            media_type   = " ".join(media_type)

            try:
                media_price  = row.xpath(".//td[contains(@class,'dp-price-col')]//span[contains(@class, 'a-color-price')]/text()").extract()
            except:
                try:
                    media_price = row.xpath(".//td[contains(@class,'dp-price-col')]//text()").extract()
                except:
                    media_price = ""

            if media_price is None:
                try:
                    media_price = row.xpath(".//td[contains(@class,'dp-price-col')]//text()").extract()
                except:
                    media_price = ""

            media_price  = " ".join(media_price).strip().replace("$","")


            if "Audible" in media_type:
                audible_flag = True
            if "Hardcover" in media_type:
                hard_price   = media_price 
            if "Paperback" in media_type:
                paper_price  = media_price 

            # quick data cleaning
        if audible_flag == "":
            audible_flag = False

        try:
            book_rank = response.xpath(".//div[@id='detailBulletsWrapper_feature_div']/ul//span[contains(text(),'Best Sellers Rank:')]/../text()").extract()
            book_rank = re.sub("[^0-9]","","".join(book_rank))
        except:
            book_rank = ""

        title_entry = BooksScrapyAmazonItem()
        title_entry["title_category"] = title_category 
        title_entry["title_url"]      = title_url
        title_entry["title"]          = title
        title_entry["subtitle"]       = subtitle
        title_entry["author"]         = author 
        title_entry["author_role"]    = author_role
        #title_entry["author_url"]    = author_url # not collected
        title_entry["audible_flag"]   = audible_flag
        title_entry["print_length"]   = print_length
        title_entry["book_volume"]    = book_volume
        title_entry["release_date"]   = release_date
        title_entry["language"]       = language
        title_entry["star_rating"]    = star_rating
        title_entry["count_rating"]   = count_rating
        title_entry["paper_price"]    = paper_price 
        title_entry["hard_price"]     = hard_price 
        title_entry["book_rank"]      = book_rank
        title_entry["type_tag"]       = response.meta['type']
        yield(title_entry)
            

            