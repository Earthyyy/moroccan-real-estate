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
    "url": "https://yakeey.com//fr-ma/acheter-appartement-casablanca-bourgogne-(sidi-belyout)-CA002544",
    "is_valid": True,
    "info": ("Appartement", "2 100 000 DH", "Bourgogne (sidi belyout)", "Casablanca",
             "126 m²", "3 Chambre(s)", "2 Sdb")
}
YAKEEY_ANNOUNCEMENT_2 = {
    "position": 5,
    "url": "https://yakeey.com//fr-ma/acheter-appartement-casablanca-maarif-extension-CA001118",
    "is_valid": True,
    "info": ("Appartement", "1 990 000 DH", "Maarif extension", "Casablanca",
             "109 m²", "2 Chambre(s)", "2 Sdb")
}
YAKEEY_ANNOUNCEMENT_LOCKED_1 = {
    "position": 18,
    "url": "https://yakeey.com//fr-ma/acheter-appartement-casablanca-la-gironde-CI061379",
    "is_valid": True,
    "info": ("Appartement", "1 600 000 DH", "La gironde", "Casablanca",
             "173 m²", "3 Chambre(s)", "2 Sdb")
}
YAKEEY_ANNOUNCEMENT_LOCKED_2 = {
    "position": 21,
    "url": "https://yakeey.com//fr-ma/acheter-appartement-casablanca-derb-omar-FA061603",
    "is_valid": True,
    "info": ("Appartement", "990 000 DH", "Derb omar", "Casablanca",
             "97 m²", "2 Chambre(s)", "2 Sdb")
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
