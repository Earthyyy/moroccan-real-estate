import scrapy

class AvitoItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    city = scrapy.Field()
    time = scrapy.Field()
    user = scrapy.Field()
    attributes = scrapy.Field()
    equipements = scrapy.Field()