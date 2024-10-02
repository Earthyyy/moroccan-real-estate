import scrapy


class AnnouncementItem(scrapy.Item):
    pass


class AnnouncementsPageItem(scrapy.Item):
    announcements_selector = scrapy.Field()
    next_page_url = scrapy.Field()
    next_page_condition = scrapy.Field()


class AvitoAnnouncementItem(scrapy.Item):

    # required fields
    # from announcement
    url = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    time = scrapy.Field()
    user = scrapy.Field()
    n_bedrooms = scrapy.Field()
    # to extract from pipeline
    # type = scrapy.Field()
    # neighborhood = scrapy.Field()
    # floor = scrapy.Field()
    # living_area = scrapy.Field()

    # optional fields
    price = scrapy.Field()
    n_bathrooms = scrapy.Field()
    total_area = scrapy.Field()
    # to extract from pipeline
    # n_living_rooms = scrapy.Field()
    # age = scrapy.Field()
    # address = scrapy.Field()
    # syndicate_price = scrapy.Field()

    # helper fields: to be transformed in the pipeline
    attributes = scrapy.Field()
    equipements = scrapy.Field()


class YakeeyAnnouncementItem(scrapy.Item):

    # required fields
    url = scrapy.Field()
    type = scrapy.Field()
    price = scrapy.Field()
    neighborhood = scrapy.Field()
    city = scrapy.Field()
    title = scrapy.Field()
    reference = scrapy.Field()

    # optional fields

    # helper fields: to be transformed in the pipeline
    attributes = scrapy.Field()
    equipements = scrapy.Field()
