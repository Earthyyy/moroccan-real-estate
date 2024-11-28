import glob
import json
from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Tuple

import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector.unified import Selector

from src.scraping.items import YakeeyAnnouncementItem


class YakeeySpider(scrapy.Spider):
    name = "yakeey"
    allowed_domains: ClassVar[List[str]] = ["yakeey.com"]
    start_urls: ClassVar[List[str]] = [
        "https://yakeey.com/fr-ma/achat/appartement/maroc"
    ]
    page_counter: int = 0
    max_pages: int = 10
    references: List[str]

    def start_requests(self):
        glob_path = "./data/raw/yakeey/*.json"
        self.references = self.set_references(glob_path)
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
            item = YakeeyAnnouncementItem()
            (
                item["url"],
                item["type"],
                item["price"],
                item["neighborhood"],
                item["city"],
            ) = announcement
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
        item["title"], item["reference"] = self.get_header(response)
        item["attributes"] = self.get_attributes(response)
        item["equipments"] = self.get_equipments(response)
        yield item

    def get_announcements(
        self,
        response: HtmlResponse,
    ) -> List[Tuple[str, str, str, str, str]]:
        """Extract the url, number of rooms, bathrooms and total area from the
        announcements page.

        Args:
            self: the spider object.
            response: the response object of the page.

        Returns:
            A list of tuples containing the url and announcements info.
        """
        announcements = []
        announcements_a = filter(
            self.is_announcement_valid, response.css("div.mui-4oo2hv a")
        )
        for a in announcements_a:
            url = "https://yakeey.com" + a.attrib["href"]
            announcements.append((url, *self.get_info_from_announcement_a(a)))
        return announcements

    def is_announcement_valid(self, a: Selector) -> bool:
        """Check if the announcement is valid.
        A valid announcement is one that doesn't point to a new real estate project.

        Args:
            self: the spider object.
            a: the anchor tag of the announcement.

        Returns:
            True if the announcement is valid, False otherwise.
        """
        return a.css("a > div > div:nth-child(1) > span::text").get() != "Neuf"

    def get_info_from_announcement_a(
        self,
        a: Selector,
    ) -> Tuple[str, str, str, str]:
        """Extract the type, price, neighborhood and city.

        Args:
            self: the spider object.
            a: the anchor tag of the announcement.

        Returns:
            A dictionary of the announcement information.
        """
        property_type = a.css("a > div > div:nth-child(2) p")[0].css("::text").get()
        _, price = a.css("a > div > div:nth-child(2) p")[1].css("::text").getall()
        neighborhood, city = (
            a.css("a > div > div:nth-child(2) p")[2].css("::text").get().split(" - ")
        )
        return (property_type, price, neighborhood, city)

    def get_next_page_url(self, response: HtmlResponse) -> Optional[str]:
        """Extract the next page url.

        Args:
            self: the spider object.
            response: the response object of the page.

        Returns:
            The next page url, or None if we reached the last page.
        """
        nav = response.css("nav.mui-0 a")
        if nav[-1].attrib.get("aria-disabled", "false") == "false":
            return "https://yakeey.com" + nav[-1].attrib["href"]
        return None

    def get_header(self, response: HtmlResponse) -> Tuple[str, str]:
        """Extract the title and reference.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A tuple of 2 strings: title and reference.
        """
        title = response.css("div.mui-6k8xca > div:nth-child(2) h1::text").get()
        reference = response.url.split("-")[-1]
        return title, reference

    def get_attributes(self, response: HtmlResponse) -> Dict[str, str]:
        """Extract the attributes.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A dictionary of the attributes.
        """
        attributes = {}
        for section in response.css("div.mui-6k8xca > div"):
            if section.css("h2 ::text").get() == "Informations générales":
                for div in section.css("div.mui-1ov46kg > div"):
                    for child_div in div.xpath("./div[2]/div"):
                        attr = child_div.css("p::text").getall()
                        attributes[attr[0]] = attr[1]
        return attributes

    def get_equipments(self, response: HtmlResponse) -> List[str]:
        """Extract extra equipments.

        Args:
            self: the spider object.
            response: the response object of the announcement page.

        Returns:
            A list representing the equipments.
        """
        equipments = []
        for section in response.css("div.mui-6k8xca > div"):
            if section.css("h2 ::text").get() == "Caractéristiques du bien":
                equipments.extend(section.css("p::text").getall())
        return equipments

    def set_references(self, glob_path: str):
        """Get the list of existing references.

        Args:
            references (List[str]): The existing references list.
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
            # get the existing references list
            with open(recent_file, "r") as file:
                data = json.load(file)
                return [row["reference"] for row in data]
        # if no file is found we return an empty list
        except (ValueError, FileNotFoundError, json.JSONDecodeError):
            return []
