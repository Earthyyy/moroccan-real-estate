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
    "info": (
        "Appartement",
        "2 100 000 DH",
        "Bourgogne (sidi belyout)",
        "Casablanca",
        "126 m²",
        "3 Chambre(s)",
        "2 Sdb",
    ),
    "header": {
        "title": "Appartement à vendre de 126 m²",
        "reference": "CA002544"
    },
    "attributes": {
        "Nb. de chambres": "3",
        "Nb. de salles de bains": "2",
        "Nb. de salles d'eau": "1",
        "Étage du bien": "7",
        "Nb. d'étages dans l'immeuble": "7",
        "Surface totale": "126 m²",
        "Surface habitable": "126 m²",
        "Surface balcon": "4 m²",
        "Places de parking en sous-sol": "1"
    },
    "equipments": [
        "Ascenseur",
        "Interphone",
        "Balcon",
        "Terrasse",
        "Place de parking en sous-sol",
        "Climatisation centralisée",
        "Chauffage centralisé"
    ]
}
YAKEEY_ANNOUNCEMENT_2 = {
    "position": 5,
    "url": "https://yakeey.com//fr-ma/acheter-appartement-casablanca-maarif-extension-CA001118",
    "is_valid": True,
    "info": (
        "Appartement",
        "1 990 000 DH",
        "Maarif extension",
        "Casablanca",
        "109 m²",
        "2 Chambre(s)",
        "2 Sdb",
    ),
    "header": {
        "title": "Appartement à vendre de 127 m² dont 109 m² habitables",
        "reference": "CA001118"
    },
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
        "Résidence fermée": "Oui"
    },
    "equipments": [
        "Ascenseur",
        "Résidence fermée",
        "Piscine commune",
        "Espaces verts",
        "Terrasse",
        "Place de parking en sous-sol",
        "Agent de sécurité",
        "Cuisine équipée"
    ]
}
YAKEEY_ANNOUNCEMENT_LOCKED_1 = {
    "position": 18,
    "url": "https://yakeey.com//fr-ma/acheter-appartement-casablanca-la-gironde-CI061379",
    "is_valid": True,
    "info": (
        "Appartement",
        "1 600 000 DH",
        "La gironde",
        "Casablanca",
        "173 m²",
        "3 Chambre(s)",
        "2 Sdb",
    ),
    "header": {
        "title": "Appartement à vendre de 199 m² dont 173 m² habitables",
        "reference": "CI061379"
    },
    "attributes": {
        "Nb. de chambres": "3",
        "Nb. de salles de bains": "2",
        "Étage du bien": "1",
        "Nb. d'étages dans l'immeuble": "5",
        "Surface totale": "199 m²",
        "Surface habitable": "173 m²"
    },
    "equipments": []
}
YAKEEY_ANNOUNCEMENT_LOCKED_2 = {
    "position": 21,
    "url": "https://yakeey.com//fr-ma/acheter-appartement-casablanca-derb-omar-FA061603",
    "is_valid": True,
    "info": (
        "Appartement",
        "990 000 DH",
        "Derb omar",
        "Casablanca",
        "97 m²",
        "2 Chambre(s)",
        "2 Sdb",
    ),
    "header": {
        "title": "Appartement à vendre de 131 m² dont 97 m² habitables",
        "reference": "FA061603"
    },
    "attributes": {
        "Nb. de chambres": "2",
        "Nb. de salles de bains": "2",
        "Étage du bien": "4",
        "Nb. d'étages dans l'immeuble": "4",
        "Surface totale": "131 m²",
        "Surface habitable": "97 m²"
    },
    "equipments": []
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
