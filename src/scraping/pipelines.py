import re
from datetime import datetime, timedelta
from typing import Tuple

from itemadapter import ItemAdapter


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
        """
        Transform the relative time to absolute date.

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
