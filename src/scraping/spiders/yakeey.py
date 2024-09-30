from typing import ClassVar, List, Optional, Tuple

import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector.unified import Selector

from src.scraping.items import YakeeyAnnouncementItem


class YakeeySpider(scrapy.Spider):
    name = "yakeey"
    allowed_domains: ClassVar = ["yakeey.com"]
    start_urls: ClassVar = ["https://yakeey.com/fr-ma/achat/appartement/maroc"]

    def parse(self, response: HtmlResponse):
        # scrape each announcement
        announcements = YakeeySpider.get_announcements(response)
        for announcement in announcements:
            item = YakeeyAnnouncementItem()
            # TODO: fill the item with info from announcements listing
            yield response.follow(
                item["url"], callback=self.parse_announcement, cb_kwargs={"item": item}
            )

        # go to the next page
        # next_page_url = YakeeySpider.get_next_page_url(response)
        # if next_page_url:
        #     yield response.follow(next_page_url, callback=self.parse)

    def parse_announcement(self, response: HtmlResponse, **kwargs):
        pass

    @staticmethod
    def get_announcements(
        response: HtmlResponse
    ) -> List[Tuple[str, str, str, str, str, str, str, str]]:
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
            YakeeySpider.is_announcement_valid, response.css("div.mui-4oo2hv a")
        )
        for a in announcements_a:
            # TODO: fill the tuple with info from the announcement
            url = a.attrib["href"]
            n_rooms, n_bathrooms, total_area = YakeeySpider.get_info_from_announcement_a(
                a
            )
            announcements.append((url, n_rooms, n_bathrooms, total_area))
        return announcements

    @staticmethod
    def is_announcement_valid(a: Selector) -> bool:
        """
        Check if the announcement is valid.
        A valid announcement is one that doesn't point to a new real estate project.

        Args:
            a: the anchor tag of the announcement.

        Returns:
            True if the announcement is valid, False otherwise.
        """
        return a.css("a > div > div:nth-child(1) > span::text").get() != "Neuf"


    @staticmethod
    def get_info_from_announcement_a(a: Selector) -> Tuple[str, str, Optional[str]]:
        pass

    @staticmethod
    def get_next_page_url(response: HtmlResponse) -> Optional[str]:
        """
        Extract the next page url.

        Args:
            response: the response object of the page.

        Returns:
            The next page url, or None if we reached the last page.
        """
        nav = response.css("nav.mui-0 a")
        if nav[-1].attrib.get("aria-disabled", "false") == "false":
            return "https://yakeey.com" + nav[-1].attrib["href"]
        return None
