# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LaptopItem(scrapy.Item):
    name = scrapy.Field()
    cpu = scrapy.Field()
    gpu = scrapy.Field()
    storage = scrapy.Field()
    ram = scrapy.Field()
    display = scrapy.Field()
    price = scrapy.Field()

    pass