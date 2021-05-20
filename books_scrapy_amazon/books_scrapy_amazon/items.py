# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CategoryAmazonItem(scrapy.Item):
    current_cat    = scrapy.Field()
    current_url    = scrapy.Field()
    superior_cats  = scrapy.Field()
    sub_cats       = scrapy.Field()
    

class BooksScrapyAmazonItem(scrapy.Item):
    title_category = scrapy.Field()    
    title_url      = scrapy.Field()
    title          = scrapy.Field()
    subtitle       = scrapy.Field()
    author         = scrapy.Field()
    author_role    = scrapy.Field()
    audible_flag   = scrapy.Field()
    print_length   = scrapy.Field()
    book_volume    = scrapy.Field() 
    release_date   = scrapy.Field()
    language       = scrapy.Field()
    star_rating    = scrapy.Field()
    count_rating   = scrapy.Field()
    paper_price    = scrapy.Field()
    hard_price     = scrapy.Field()
    book_rank      = scrapy.Field()
    type_tag       = scrapy.Field()