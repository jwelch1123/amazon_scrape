# amazon_scrape

This a half-built project that I partially built out while building an Audible scraping project, [found here](https://github.com/jwelch1123/finding_the_tree_in_the_forest.git).


Requirements:
- Install **requirements.txt**
- [ScraperAPI](https://www.scraperapi.com/) key

The project consists of two spiders:
- amazon_cat_spider.py
- amazon_title_spider.py

### Amazon Category Spider

In order to examine the category structure of amazon books, [starting here](https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155&dc&fs=true&qid=1620260821&ref=sr_ex_n_1). 

After about 500 requests, Amazon will display a CAPTCHA. After considering multiple solutions, I went with ScraperAPI which allows easy access to proxies. The current usage of this is pretty wasteful since it calls the proxy for every single URL but I think they allow you to use the same proxy multiple times which would be better.

I used all 5000 free proxy calls and was not able to completely map the category structure of Amazon, there are likely ~7000 distinct categories based on how many top-level categories were scraped. 

The spider works in the following way:
1. Start at the [top level](https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155&dc&fs=true&qid=1620260821&ref=sr_ex_n_1) page.
2. Get the current category, bolded text.
3. Create a list of the super (above) categories, has arrow.
4. Get urls for subcategories, has a link & indent tag.
5. For each subcategory, pass it to the main parsing method, repeating steps 2-5 until no categories remain.


### Amazon Title Spider

This spider takes the category urls parsed by the Category Spider from a csv and iterates across them and passes all the title urls which have the text "Hardcover" or "Paperback" to the title_info_collection method. Once the bottom of the page is reach, the url of the next page is passed recursively to the same method. The title_info_collection method collects the information such as authors, prices, and book metrics. 

This spider does not yet implement the ScraperAPI solution will likely result in CAPTCHA pages after 500 unique page vists. 

