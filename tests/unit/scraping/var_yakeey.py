"""Variables to be used in test_yakeey.py"""

# Requests to the following URLs are cached in tests/scraping/cassettes
# if these caches are deleted, links might not work as the information
# is constantly changing.

YAKEEY_PAGES = {
    1: "https://yakeey.com/fr-ma/achat/appartement/maroc?page=1",
    2: "https://yakeey.com/fr-ma/achat/appartement/maroc?page=2",
    3: "https://yakeey.com/fr-ma/achat/appartement/maroc?page=3",
    15: "https://yakeey.com/fr-ma/achat/appartement/maroc?page=15",
    16: "https://yakeey.com/fr-ma/achat/appartement/maroc?page=16",
    33: "https://yakeey.com/fr-ma/achat/appartement/maroc?page=33",
    34: "https://yakeey.com/fr-ma/achat/appartement/maroc?page=34",
}

YAKEEY_ANNOUNCEMENT_1 = {
    "position": 0,
    "is_valid": True,
}
YAKEEY_ANNOUNCEMENT_2 = {
    "position": 5,
    "is_valid": True,
}
YAKEEY_ANNOUNCEMENT_LOCKED_1 = {
    "position": 18,
    "is_valid": True,
}
YAKEEY_ANNOUNCEMENT_LOCKED_2 = {
    "position": 21,
    "is_valid": True,
}
YAKEEY_ANNOUNCEMENT_NEUF_1 = {
    "position": 23,
    "is_valid": False,
}
YAKEEY_ANNOUNCEMENT_NEUF_2 = {
    "position": 24,
    "is_valid": False,
}

YAKEEY_ANNOUNCEMENTS = [
    YAKEEY_ANNOUNCEMENT_1,
    YAKEEY_ANNOUNCEMENT_2,
    YAKEEY_ANNOUNCEMENT_LOCKED_1,
    YAKEEY_ANNOUNCEMENT_LOCKED_2,
]
