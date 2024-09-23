import scrapy

class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["www.avito.ma"]
    start_urls = ["https://www.avito.ma/fr/maroc/appartements-à_vendre"]

    def parse(self, response):
        # get the url for each announcements
        announcements = response.css("a.sc-1jge648-0")
        for announcement in announcements:
            announcement_url = announcement.attrib["href"]
            yield response.follow(announcement_url, callback=self.parse_announcement)
        
        # get the url for the next page
        # nav = response.css("div.sc-2y0ggl-0 a")

        # if "activePage" not in nav[-1].attrib["class"]:
        #     next_page_url = nav[-1].attrib["href"]
        #     yield response.follow(next_page_url, callback=self.parse)
    
    def parse_announcement(self, response):
        title = response.css("div.sc-1g3sn3w-8 h1::text").get()
        price = response.css("div.sc-1g3sn3w-8 p::text").get()
        city, time = (response.css("div.sc-1g3sn3w-7 span")[i].css("::text").get() for i in range(2))
        poster = response.css("div.sc-1g3sn3w-2 p::text").get()
        attributes = dict()
        for li in response.css("div.sc-1g3sn3w-3 li"):
            key, value = (li.css("span::text")[i].get() for i in range(2))
            attributes[key] = value
        
        