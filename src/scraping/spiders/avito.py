from typing import ClassVar, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector.unified import Selector

from src.scraping.items import AvitoAnnouncementItem


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains: ClassVar = ["www.avito.ma"]
    start_urls: ClassVar = ["https://www.avito.ma/fr/maroc/appartements-à_vendre"]

    def parse(self, response: HtmlResponse):
        # scrape each announcement
        announcements = AvitoSpider.get_announcements(response)
        for announcement in announcements:
            item = AvitoAnnouncementItem()
            item["url"], item["n_bedrooms"], item["n_bathrooms"], item["total_area"] = (
                announcement
            )
            yield response.follow(
                item["url"], callback=self.parse_announcement, cb_kwargs={"item": item}
            )

        # go to the next page
        next_page_url = AvitoSpider.get_next_page_url(response)
        if (
            next_page_url
            and next_page_url
            != "https://www.avito.ma/fr/maroc/appartements-à_vendre?page=2"
        ):
            yield response.follow(next_page_url, callback=self.parse)

    def parse_announcement(self, response: HtmlResponse, **kwargs):
        item = kwargs["item"]
        item["title"], item["price"], item["city"], item["time"], item["user"] = (
            self.get_header(response)
        )
        item["attributes"] = self.get_attributes(response)
        item["equipements"] = self.get_equipments(response)
        yield item

    @staticmethod
    def get_announcements(
        response: HtmlResponse,
    ) -> List[Tuple[str, str, Optional[str], Optional[str]]]:
        """
        Extract the url, number of rooms, bathrooms and total area from the
        announcements page.

        Args:
            response: the response object of the page.

        Returns:
            A list of tuples
            (url, n_rooms, n_bathrooms (optional), total_area (optional)).
        """
        announcements = []
        announcements_a = filter(
            AvitoSpider.is_announcement_valid, response.css("div.sc-1nre5ec-1 a")
        )
        for a in announcements_a:
            url = a.attrib["href"]
            announcements.append((url, *AvitoSpider.get_info_from_announcement_a(a)))
        return announcements

    @staticmethod
    def is_announcement_valid(a: Selector) -> bool:
        """
        Check if the announcement is valid.
        A valid announcement is one that doesn't redirect to any external domain.

        Args:
            a: the anchor tag of the announcement.

        Returns:
            True if the announcement is valid, False otherwise.
        """
        url = a.attrib["href"]
        domain = urlparse(url).netloc
        return domain in AvitoSpider.allowed_domains

    @staticmethod
    def get_info_from_announcement_a(
        a: Selector,
    ) -> Tuple[str, Optional[str], Optional[str]]:
        """
        Extract the number of rooms, bathrooms and total area from the announcement.

        Args:
            a: the anchor tag of the announcement.

        Returns:
            A tuple of 3 strings: n_rooms, n_bathrooms (optional),
            total_area (optional).
        """
        n_rooms, n_bathrooms, total_area = "", None, None
        spans_text = [
            "".join(elem.css("::text").getall()).strip()
            for elem in a.xpath('./div[3]//span[contains(@class, "sc-1s278lr-0")]')
        ]
        if spans_text:
            n_rooms = spans_text[0]
            if len(spans_text) == 2:
                if "m²" not in spans_text[1]:
                    n_bathrooms = spans_text[1]
                else:
                    total_area = spans_text[1]
            elif len(spans_text) == 3:
                n_bathrooms, total_area = spans_text[1:]
        return n_rooms, n_bathrooms, total_area

    @staticmethod
    def get_next_page_url(response: HtmlResponse) -> Optional[str]:
        """
        Extract the next page url.

        Args:
            response: the response object of the page.

        Returns:
            The next page url, or None if we reached the last page.
        """
        nav = response.css("div.sc-2y0ggl-0 a")
        if "activePage" not in nav[-1].attrib["class"]:
            return nav[-1].attrib["href"]
        return None

    @staticmethod
    def get_header(response: HtmlResponse) -> Tuple[str, str, str, str, str]:
        """
        Extract the title, price, city, time and user.

        Args:
            response: the response object of the announcement page.

        Returns:
            A tuple of 5 strings: title, price, city, time, user.
        """
        header1 = response.css("div.sc-1g3sn3w-8")
        title = header1.css("h1::text").get()
        price = header1.css("p::text").get()
        city = header1.css("div.sc-1g3sn3w-8 > div:nth-child(2) span::text").get()
        time = header1.css("time::text").get()
        header2 = response.css("div.sc-1g3sn3w-2")
        user = header2.css("p::text").get()
        return title, price, city, time, user

    @staticmethod
    def get_attributes(response: HtmlResponse) -> Dict[str, str]:
        """
        Extract the attributes.

        Args:
            response: the response object of the announcement page.

        Returns:
            A dictionary of the attributes.
        """
        attributes = {}
        for li in response.css("div.sc-1g3sn3w-3 li"):
            key, value = li.css("span::text").getall()
            attributes[key] = value
        return attributes

    @staticmethod
    def get_equipments(response: HtmlResponse) -> List[str]:
        """
        Extract extra equipements.

        Args:
            response: the response object of the announcement page.

        Returns:
            A list representing the equipments.
        """
        return response.css("div.sc-1g3sn3w-15 span::text").getall()
