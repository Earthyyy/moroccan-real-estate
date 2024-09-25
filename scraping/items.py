import scrapy

class AnnouncementItem(scrapy.Item):
    pass

class AnnouncementsPageItem(scrapy.Item):
    pass

class AvitoAnnouncementItem(scrapy.Item):

    # required fields
    url = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    time = scrapy.Field()
    user = scrapy.Field()
    n_bedrooms = scrapy.Field()
    type = scrapy.Field()
    neighborhood = scrapy.Field()
    living_area = scrapy.Field()
    floor = scrapy.Field()
    
    # optional fields
    price = scrapy.Field()
    n_bathrooms = scrapy.Field()
    total_area = scrapy.Field()
    n_living_rooms = scrapy.Field()
    age = scrapy.Field()
    address = scrapy.Field()
    syndicate_price = scrapy.Field()

    # helper fields: to be transformed in the pipeline
    attributes = scrapy.Field()
    equipements = scrapy.Field()
