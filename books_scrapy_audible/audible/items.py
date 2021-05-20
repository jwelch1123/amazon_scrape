# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TitleItem(scrapy.Item):
	title_category  = scrapy.Field()    
	title_url       = scrapy.Field()
	title           = scrapy.Field()
	subtitle        = scrapy.Field()
	author          = scrapy.Field()
	narrator        = scrapy.Field()
	length          = scrapy.Field()
	release_date    = scrapy.Field()
	language        = scrapy.Field()
	star_rating     = scrapy.Field()
	count_rating    = scrapy.Field()
	price           = scrapy.Field()
	pod_flag        = scrapy.Field()

# not all books have subtitles
# not all books are rated (within ratingsLabel)
# Number of stars is written as off-screen text



class CategoryItem(scrapy.Item):
	parent_category     = scrapy.Field()
	parent_url          = scrapy.Field()
	self_url            = scrapy.Field()    
	category_name       = scrapy.Field()
	category_numb_title = scrapy.Field()    
	title_list_url      = scrapy.Field()
	leaf_flag           = scrapy.Field()

 
