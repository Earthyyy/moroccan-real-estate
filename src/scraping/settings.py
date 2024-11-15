import datetime

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

BOT_NAME = "moroccan-real-estate"

SPIDER_MODULES = ["src.scraping.spiders"]
NEWSPIDER_MODULE = "src.scraping.spiders"

# obey robots.txt rules
ROBOTSTXT_OBEY = True

# configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0.5

# Enable AutoThrottle
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 1
# AUTOTHROTTLE_MAX_DELAY = 2
# AUTOTHROTTLE_TARGET_CONCURRENCY = 8

# configure item pipelines
ITEM_PIPELINES = {
    "src.scraping.pipelines.AvitoTimePipeline": 400,
    "src.scraping.pipelines.AvitoFilterPipeline": 300,
    "src.scraping.pipelines.YakeeyFilterPipeline": 200,
}

# configure logging
LOG_ENABLED = True
LOG_LEVEL = "DEBUG"
LOG_FILE_APPEND = False
LOG_FILE = None

# FEEDS setting
FEEDS = {
    f"./data/raw/avito/avito_{current_date}.json": {
        "format": "json",
        "overwrite": True,
        "encoding": "utf8",
        "store_empty": False,
        "fields": None,
        "indent": 4,
        "item_classes": ["src.scraping.items.AvitoAnnouncementItem"],
    },
    f"./data/raw/yakeey/yakeey_{current_date}.json": {
        "format": "json",
        "overwrite": True,
        "encoding": "utf8",
        "store_empty": False,
        "fields": None,
        "indent": 4,
        "item_classes": ["src.scraping.items.YakeeyAnnouncementItem"],
    },
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
