import glob
import json
from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector.unified import Selector

from src.scraping.items import AvitoAnnouncementItem


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains: ClassVar[List[str]] = ["www.avito.ma"]
    start_urls: ClassVar[List[str]] = [
        "https://www.avito.ma/fr/maroc/appartements-à_vendre"
    ]
    page_counter: int = 0
    max_pages: int = 10
    recent_date: datetime

    def start_requests(self):
        glob_path = "./data/raw/avito/*.json"
        self.recent_date = self.set_recent_date(glob_path)
        return super().start_requests()

    def parse(self, response: HtmlResponse):
        # increment the page counter
        self.page_counter += 1
        if self.page_counter > self.max_pages:
            self.logger.info("Reached the maximum number of pages.")
            self.crawler.engine.close_spider(
                self, "Reached the maximum number of pages."
            )
        # get the announcements from list and parse them
        announcements = self.get_announcements(response)
        for announcement in announcements:
            item = AvitoAnnouncementItem()
            item["url"], item["n_bedrooms"], item["n_bathrooms"], item["total_area"] = (
                announcement
            )
            yield response.follow(
                item["url"], callback=self.parse_announcement, cb_kwargs={"item": item}
            )
        # go to the next page
        next_page_url = self.get_next_page_url(response)
        if (
            next_page_url
            and self.page_counter < self.max_pages
        ):
            yield response.follow(next_page_url, callback=self.parse)

    def parse_announcement(self, response: HtmlResponse, **kwargs):
        item = kwargs["item"]
        item["title"], item["price"], item["city"], item["time"], item["user"] = (
            self.get_header(response)
        )
        item["attributes"] = self.get_attributes(response)
        item["equipments"] = self.get_equipments(response)
        yield item

    def get_announcements(
        self,
        response: HtmlResponse,
    ) -> List[Tuple[str, str, Optional[str], Optional[str]]]:
        """Extract the url, number of rooms, bathrooms and total area from the
        announcements page.

        Args:
            self: the spider object.
            response: the response object of the page.

        Returns:
            A list of tuples
            (url, n_rooms, n_bathrooms (optional), total_area (optional)).
        """
        announcements = []
        announcements_a = filter(
            self.is_announcement_valid, response.css("div.sc-1nre5ec-1 a")
        )
        for a in announcements_a:
            url = a.attrib["href"]
            announcements.append((url, *self.get_info_from_announcement_a(a)))
        return announcements

    def is_announcement_valid(self, a: Selector) -> bool:
        """Check if the announcement is valid.
        A valid announcement is one that doesn't redirect to any external domain.

        Args:
            self: the spider object.
            a: the anchor tag of the announcement.

        Returns:
            True if the announcement is valid, False otherwise.
        """
        url = a.attrib["href"]
        domain = urlparse(url).netloc
        return domain in self.allowed_domains

    def get_info_from_announcement_a(
        self,
        a: Selector,
    ) -> Tuple[str, Optional[str], Optional[str]]:
        """Extract the number of rooms, bathrooms and total area from the announcement.

        Args:
            self: the spider object.
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

    def get_next_page_url(self, response: HtmlResponse) -> Optional[str]:
        """Extract the next page url.

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

    def get_header(self, response: HtmlResponse) -> Tuple[str, str, str, str, str]:
        """Extract the title, price, city, time and user.

        Args:
            self: the spider object.
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

    def get_attributes(self, response: HtmlResponse) -> Dict[str, str]:
        """Extract the attributes.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A dictionary of the attributes.
        """
        attributes = {}
        for li in response.css("div.sc-1g3sn3w-3 li"):
            key, value = li.css("span::text").getall()
            attributes[key] = value
        return attributes

    def get_equipments(self, response: HtmlResponse) -> List[str]:
        """Extract extra equipments.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A list representing the equipments.
        """
        return response.css(
            "div.sc-1g3sn3w-15 > div > div:nth-child(1) ::text"
        ).getall()

    def set_recent_date(self, glob_path: str) -> datetime:
        """Get the date of the most recent scraped announcement.

        Returns:
            datetime: The date of the most recent announcement.
        """
        try:
            # get the most recent json file
            files = glob.glob(glob_path)
            recent_file = max(
                files,
                key=lambda file: datetime.strptime(
                    file.split("/")[-1].split("_")[-1].split(".")[0], "%Y-%m-%d"
                ),
            )
            # get the most recent date from the file
            with open(recent_file, "r") as file:
                data = json.load(file)
                return max(
                    [
                        datetime.strptime(row["date_time"], "%Y-%m-%d %H:%M")
                        for row in data
                    ]
                )
        # return the base date if no file is found
        except (ValueError, FileNotFoundError, json.JSONDecodeError):
            return datetime(
                2024, 1, 1
            )  # we are going to ignore announcements older than this date
