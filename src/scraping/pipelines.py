import re
from datetime import datetime, timedelta
from typing import ClassVar, List, Tuple

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class BaseFilterPipeline:
    required_fields: ClassVar[List[str]] = []
    required_attributes: ClassVar[List[str]] = []

    def process_item(self, item, spider):  # noqa: ARG002
        item_adapter = ItemAdapter(item)
        for field in self.required_fields:
            if not item_adapter.get(field):
                raise DropItem(f"Missing {field} in {item}")
        return item


class AvitoFilterPipeline(BaseFilterPipeline):
    required_fields: ClassVar[List[str]] = [
        "title",
        "city",
        "time",
        "user",
        "price",
        "n_bedrooms",
        "attributes",
    ]

    def process_item(self, item, spider):
        if spider.name != "avito":
            return item
        return super().process_item(item, spider)


class YakeeyFilterPipeline(BaseFilterPipeline):
    required_fields: ClassVar[List[str]] = [
        "type",
        "price",
        "neighborhood",
        "city",
        "title",
        "reference",
        "attributes",
    ]

    def process_item(self, item, spider):
        if spider.name != "yakeey":
            return item
        return super().process_item(item, spider)


class AvitoTimePipeline:
    time_re = re.compile(r"il y a (\d+) (minutes?|heures?|jours?|mois|ans?)")

    def process_item(self, item, spider):
        # only process items from AvitoSpider
        if spider.name != "avito":
            return item
        adapter = ItemAdapter(item)
        time = adapter.get("time")
        if time:
            adapter["date_time"], adapter["year"], adapter["month"] = (
                self.get_absolute_time(time)
            )
        return item

    @staticmethod
    def get_absolute_time(relative_time: str) -> Tuple[str, int, int]:
        """Transform the relative time to absolute date.

        Args:
            relative_time: the relative time.

        Returns:
            The absolute time.
        """
        # get the current date
        current_date = datetime.now()
        match = AvitoTimePipeline.time_re.match(relative_time)

        if not match:
            return "", 0, 0
        n, unit = match.groups()
        n = int(n)
        if "minute" in unit:
            delta = timedelta(minutes=n)
        elif "heure" in unit:
            delta = timedelta(hours=n)
        elif "jour" in unit:
            delta = timedelta(days=n)
        elif "mois" in unit:
            delta = timedelta(days=31 * n)
        elif "an" in unit:
            delta = timedelta(days=365 * n)
        date = current_date - delta
        return (
            date.strftime("%Y-%m-%d %H:%M"),
            date.year,
            date.month,
        )
