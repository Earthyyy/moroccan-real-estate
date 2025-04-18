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
    "info": ("Appartement", "2 100 000 DH", "Bourgogne (sidi belyout)", "Casablanca"),
    "header": ("Appartement à vendre de 126 m²", "CA002544"),
    "attributes": {
        "Nb. de chambres": "3",
        "Nb. de salles de bains": "2",
        "Nb. de salles d'eau": "1",
        "Étage du bien": "7",
        "Nb. d'étages dans l'immeuble": "7",
        "Surface totale": "126 m²",
        "Surface habitable": "126 m²",
        "Surface balcon": "4 m²",
        "Places de parking en sous-sol": "1",
    },
    "equipments": [
        "Ascenseur",
        "Interphone",
        "Balcon",
        "Terrasse",
        "Place de parking en sous-sol",
        "Climatisation centralisée",
        "Chauffage centralisé",
    ],
}
YAKEEY_ANNOUNCEMENT_2 = {
    "position": 5,
    "url": "https://yakeey.com//fr-ma/acheter-appartement-casablanca-maarif-extension-CA001118",
    "is_valid": True,
    "info": ("Appartement", "1 990 000 DH", "Maarif extension", "Casablanca"),
    "header": ("Appartement à vendre de 127 m² dont 109 m² habitables", "CA001118"),
    "attributes": {
        "Nb. de chambres": "2",
        "Nb. de salles de bains": "2",
        "Étage du bien": "1",
        "Nb. d'étages dans l'immeuble": "8",
        "Surface totale": "127 m²",
        "Surface habitable": "109 m²",
        "Surface terrasse": "10 m²",
        "Vue": "Vue dégagée",
        "Nb. de façades": "1",
        "Résidence fermée": "Oui",
    },
    "equipments": [
        "Ascenseur",
        "Résidence fermée",
        "Piscine commune",
        "Espaces verts",
        "Terrasse",
        "Place de parking en sous-sol",
        "Agent de sécurité",
        "Cuisine équipée",
    ],
}
YAKEEY_ANNOUNCEMENT_LOCKED_1 = {
    "position": 18,
    "is_valid": False,
}
YAKEEY_ANNOUNCEMENT_LOCKED_2 = {
    "position": 21,
    "is_valid": False,
}
YAKEEY_ANNOUNCEMENT_NEUF_1 = {
    "position": 23,
    "is_valid": False,
}
YAKEEY_ANNOUNCEMENT_NEUF_2 = {
    "position": 24,
    "is_valid": False,
}

YAKEEY_ANNOUNCEMENT_NO_ADDRESS = {
    "url": "https://yakeey.com/fr-ma/acheter-appartement-II063966",
    "header": ("Appartement à vendre de 64 m²", "II063966"),
    "attributes": {
        "Nb. de chambres": "2",
        "Nb. de salles de bains": "1",
        "Étage du bien": "3",
        "Nb. d'étages dans l'immeuble": "4",
        "Surface totale": "64 m²",
        "Surface habitable": "64 m²",
    },
    "equipments": [
        "Ascenseur",
        "Place de parking en sous-sol",
        "Agent de sécurité",
        "Climatisation centralisée",
        "Chauffage centralisé",
        "Cuisine équipée",
    ],
}

YAKEEY_ANNOUNCEMENTS = [
    YAKEEY_ANNOUNCEMENT_1,
    YAKEEY_ANNOUNCEMENT_2,
    YAKEEY_ANNOUNCEMENT_NO_ADDRESS,
]
