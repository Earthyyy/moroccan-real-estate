from scrapy import Field, Item


class AvitoAnnouncementItem(Item):
    url = Field()
    attributes = Field()
    equipments = Field()

    # required fields
    # from announcement
    title = Field()
    city = Field()
    time = Field()
    user = Field()
    price = Field()
    n_bedrooms = Field()
    # to extract from pipeline
    date_time = Field()
    year = Field()
    month = Field()
    # from self.attributes
    # Type
    # Secteur
    # Étage
    # Surface habitable

    # optional fields
    # from announcement
    n_bathrooms = Field()
    total_area = Field()
    # from self.attributes
    # Salons
    # Âge du bien
    # Frais de syndic / mois


class YakeeyAnnouncementItem(Item):
    url = Field()
    attributes = Field()
    equipments = Field()

    # required fields
    # from announcement
    type = Field()
    price = Field()
    neighborhood = Field()
    city = Field()
    title = Field()
    reference = Field()
    # from self.attributes
    # Nb. de chambres
    # Nb. de salles de bains
    # Surface habitable
    # Étage du bien
    # Surface totale
    # Nb. d'étages dans l'immeuble
    # Nb. de salles d'eau

    # optional fields
    # the rest of self.attributes
