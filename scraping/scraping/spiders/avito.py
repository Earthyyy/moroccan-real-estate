import scrapy
from scraping.items import AvitoItem

class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["www.avito.ma"]
    start_urls = ["https://www.avito.ma/fr/maroc/appartements-à_vendre"]

    def parse(self, response):
        # scrape each announcement
        announcement_urls = self.get_announcement_urls(response)
        for announcement_url in announcement_urls:
            yield response.follow(announcement_url, callback=self.parse_announcement)
        
        # go to the next page
        # next_page_url = self.get_next_page_url(response)
        # if next_page_url:
        #     yield response.follow(next_page_url, callback=self.parse)
    
    def parse_announcement(self, response):
        item = AvitoItem()
        item["title"], item["price"], item["city"], item["time"], item["user"] = self.get_header(response)
        item["attributes"] = self.get_attributes(response)
        item["equipements"] = self.get_equipments(response)
        yield item

    def get_announcement_urls(self, response):
        """
        Extract the announcement urls.
        
        Args:
            self: the spider object.
            response: the response object of the page.

        Returns:
            A list of announcement urls.
        """
        return response.css("div.sc-1nre5ec-1 a::attr(href)").getall()

    def get_next_page_url(self, response):
        """
        Extract the next page url.
        
        Args:
            self: the spider object.
            response: the response object of the page.
            
        Returns:
            The next page url, or None if we reached the last page.
        """
        nav = response.css("div.sc-2y0ggl-0 a")
        if "activePage" not in nav[-1].attrib["class"]:
            return nav[-1].attrib["href"]
        return None

    def get_header(self, response):
        """
        Extract the title, price, city, time and user.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A tuple of 5 strings: title, price, city, time, user.
        """
        title, price, city, time = response.css("div.sc-1g3sn3w-8 ::text").getall()
        user = response.css("div.sc-1g3sn3w-0.sc-1g3sn3w-2 p::text").get()
        return title, price, city, time, user
    
    def get_attributes(self, response):
        """
        Extract the attributes.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A dictionary of the attributes.
        """
        attributes = dict()
        # 1st part of the attributes
        n_rooms, n_bathrooms, total_area = self.get_attributes_first(response)
        attributes["Chambres"] = n_rooms
        attributes["Salles de bain"] = n_bathrooms
        attributes["Surface totale"] = total_area

        # 2nd part of the attributes
        attributes.update(self.get_attributes_second(response))

        return attributes

    def get_attributes_first(self, response):
        """
        Extract the first part of the attributes.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A tuple of 3 strings: n_rooms, n_bathrooms, total_area.
        """
        n_bedrooms, n_bathrooms, total_area = None, None, None
        n_bedrooms, *optional = response.css("div.sc-1g3sn3w-3 div.sc-6p5md9-0 ::text").getall()
        if len(optional) == 1:
            if 0 < int(optional[0]) <= 8:
                n_bathrooms = optional[0]
            else:
                total_area = optional[0]
        elif len(optional) == 2:
            n_bathrooms, total_area = optional
        return n_bedrooms, n_bathrooms, total_area
    
    def get_attributes_second(self, response):
        """
        Extract the second part of the attributes.

        Args:
            self: the spider object
            response: the response object of the announcement page.

        Returns:
            A dictionary of the attributes.
        """
        attributes = dict()
        for li in response.css("div.sc-1g3sn3w-3 li"):
            key, value = li.css("span::text").getall()
            attributes[key] = value
        return attributes

    def get_equipments(self, response):
        """
        Extract extra equipements.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A list representing the equipments.
        """
        return response.css("div.sc-1g3sn3w-15 span::text").getall()
