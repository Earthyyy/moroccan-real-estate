"""Variables to be used in test_avito.py"""

# Requests to the following URLs are cached in tests/scraping/cassettes
# if these caches are deleted, links might not work as the information
# is constantly changing.
# for example, the last page of the announcements is 1359,
# but it might change in the future, as well as announcements within the pages,
# or information in an announcement.

AVITO_PAGES = {
    1: "https://www.avito.ma/fr/maroc/appartements-à_vendre",
    2: "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=2",
    3: "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=3",
    500: "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=500",
    501: "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=501",
    1000: "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=1000",
    1001: "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=1001",
    1359: "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=1359",
    1360: "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=1360",
}

AVITO_ANNOUNCEMENT = {
    "position": 0,
    "url": "https://www.avito.ma/fr/autre_secteur/appartements/شقة_بواجهتين_بالقرب_من_ديكاتلون_فمنزل_R2__55576138.htm",
    "is_valid": True,
    "info": ("3", "3", "140 m²"),
    "header": (
        "شقة بواجهتين بالقرب من ديكاتلون فمنزل R2 ",
        "880 000 DH",  # noqa: RUF001
        "Meknès",
        "il y a 9 heures",
        "BAMEKNA IMMOBILIER",
    ),
    "attributes": {
        "Type": "Appartements, à vendre",
        "Secteur": "Autre secteur",
        "Salons": "2",
        "Surface habitable": "140",
        "Âge du bien": "Neuf",
        "Étage": "2",
    },
    "equipments": [
        "Balcon",
        "Chauffage",
        "Climatisation",
        "Concierge",
        "Cuisine équipée",
        "Duplex",
        "Meublé",
        "Sécurité",
        "Terrasse",
    ],
}
AVITO_ANNOUNCEMENT_STAR = {
    "position": 27,
    "url": "https://www.avito.ma/fr/skikina/appartements/Appartement_à_vendre_105_m²_à_Temara_55562047.htm",
    "is_valid": True,
    "info": ("3", "2", "105 m²"),
    "header": (
        "Appartement à vendre 105 m² à Temara",
        "750 000 DH",  # noqa: RUF001
        "Temara",
        "il y a 9 heures",
        "Karim ",
    ),
    "attributes": {
        "Type": "Appartements, à vendre",
        "Secteur": "Skikina",
        "Frais de syndic / mois": "150",
        "Salons": "1",
        "Surface habitable": "105",
        "Âge du bien": "11-20 ans",
        "Étage": "3",
    },
    "equipments": ["Ascenseur", "Balcon", "Parking", "Sécurité"],
}
AVITO_ANNOUNCEMENT_VERIFIED = {
    "position": 23,
    "url": "https://www.avito.ma/fr/2_mars/appartements/Appartement_Spacieux_à_vendre_147_m²_à_Casablanca__55393976.htm",
    "is_valid": True,
    "info": ("3", "2", "147 m²"),
    "header": (
        "Appartement Spacieux à vendre 147 m² à Casablanca ",
        "1 950 000 DH",  # noqa: RUF001
        "Casablanca",
        "il y a 9 heures",
        "Keysafe Immobilier",
    ),
    "attributes": {
        "Type": "Appartements, à vendre",
        "Secteur": "2 Mars",
        "Frais de syndic / mois": "500",
        "Salons": "2",
        "Surface habitable": "147",
        "Étage": "Rez de chaussée",
    },
    "equipments": [
        "Ascenseur",
        "Balcon",
        "Chauffage",
        "Climatisation",
        "Concierge",
        "Cuisine équipée",
        "Parking",
        "Sécurité",
        "Terrasse",
    ],
}
AVITO_ANNOUNCEMENT_REQUIRED_ONLY = {
    "position": 11,
    "url": "https://www.avito.ma/fr/khemisset/appartements/Appartement_à_vendre_1_m²_à_Khemisset_55576049.htm",
    "is_valid": True,
    "info": ("1", None, None),
    "header": (
        "Appartement à vendre 1 m² à Khemisset",
        "Prix non spécifié",
        "Khemisset",
        "il y a 9 heures",
        "wassim jaouya",
    ),
    "attributes": {
        "Type": "Appartements, à vendre",
        "Secteur": "Toute la ville",
        "Surface habitable": "1",
        "Étage": "1",
    },
    "equipments": [],
}
AVITO_ANNOUNCEMENT_OPTIONAL_ALL = {
    "position": 21,
    "url": "https://www.avito.ma/fr/saidia/appartements/Apparemment__saidia_ap2_al_waha_55208892.htm",
    "is_valid": True,
    "info": ("2", "2", "117 m²"),
    "header": (
        "Apparemment saidia ap2 al waha",
        "980 000 DH",  # noqa: RUF001
        "Saidia",
        "il y a 9 heures",
        "Ad Ch",
    ),
    "attributes": {
        "Type": "Appartements, à vendre",
        "Secteur": "Toute la ville",
        "Frais de syndic / mois": "265",
        "Salons": "1",
        "Surface habitable": "117",
        "Âge du bien": "6-10 ans",
        "Étage": "1",
    },
    "equipments": [
        "Balcon",
        "Climatisation",
        "Concierge",
        "Cuisine équipée",
        "Meublé",
        "Parking",
        "Sécurité",
        "Terrasse",
    ],
}
AVITO_ANNOUNCEMENT_NO_PRICE = {
    "position": 5,
    "url": "https://www.avito.ma/fr/sakar/appartements/appartement_avec_jardin__55576063.htm",
    "is_valid": True,
    "info": ("3", "2", "281 m²"),
    "header": (
        "appartement avec jardin ",
        "Prix non spécifié",
        "Marrakech",
        "il y a 9 heures",
        "Summer House",
    ),
    "attributes": {
        "Type": "Appartements, à vendre",
        "Secteur": "Sakar",
        "Salons": "2",
        "Surface habitable": "140",
        "Âge du bien": "11-20 ans",
        "Étage": "Rez de chaussée",
    },
    "equipments": ["Chauffage", "Climatisation", "Cuisine équipée", "Terrasse"],
}
AVITO_ANNOUNCEMENT_NO_EQUIPMENTS = {
    "position": 2,
    "url": "https://www.avito.ma/fr/oulfa/appartements/appartement_sourour_farah_salam__55440383.htm",
    "is_valid": True,
    "info": ("2", "1", "50 m²"),
    "header": (
        "appartement sourour farah salam ",
        "280 000 DH",  # noqa: RUF001
        "Casablanca",
        "il y a 9 heures",
        "Agence immobilière la confiance ",
    ),
    "attributes": {
        "Type": "Appartements, à vendre",
        "Secteur": "Oulfa",
        "Frais de syndic / mois": "30",
        "Salons": "1",
        "Surface habitable": "50",
        "Âge du bien": "1-5 ans",
        "Étage": "3",
    },
    "equipments": [],
}
AVITO_ANNOUNCEMENT_HIDDEN_EQUIPMENT = {
    "url": "https://www.avito.ma/fr/gu%C3%A9liz/appartements/Studio_Appartement_Haut_Standing_Gueliz_55203172.htm",
    "is_valid": True,
    "info": ("2", "2", "51 m²"),
    "header": (
        "Studio-Appartement-Haut-Standing-Gueliz",
        "19 000 DH",  # noqa: RUF001
        "Marrakech",
        "il y a 3 heures",
        "CHEZ NIZAR",
    ),
    "attributes": {
        "Type": "Appartements, à vendre",
        "Secteur": "Guéliz",
        "Salons": "1",
        "Surface habitable": "51",
        "Âge du bien": "Neuf",
        "Étage": "5",
    },
    "equipments": [
        "Ascenseur",
        "Balcon",
        "Chauffage",
        "Climatisation",
        "Concierge",
        "Cuisine équipée",
        "Duplex",
        "Meublé",
        "Parking",
        "Sécurité",
        "Terrasse",
    ],
}

AVITO_ANNOUNCEMENT_IMMONEUF = {
    "position": 4,
    "url": "https://immoneuf.avito.ma/fr/unite/jfU?utm_source=avito_integration&utm_medium=listing_integration",
    "is_valid": False,
    "info": None,
    "header": None,
    "attributes": None,
    "equipments": None,
}

AVITO_ANNOUNCEMENTS = [
    AVITO_ANNOUNCEMENT,
    AVITO_ANNOUNCEMENT_STAR,
    AVITO_ANNOUNCEMENT_VERIFIED,
    AVITO_ANNOUNCEMENT_REQUIRED_ONLY,
    AVITO_ANNOUNCEMENT_OPTIONAL_ALL,
    AVITO_ANNOUNCEMENT_NO_PRICE,
    AVITO_ANNOUNCEMENT_NO_EQUIPMENTS,
    AVITO_ANNOUNCEMENT_HIDDEN_EQUIPMENT,
]
