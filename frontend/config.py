from dataclasses import dataclass

@dataclass
class Config:
    PATH_TO_DW: str = "./data/dw/datawarehouse.db"
    PAGE_TITLE: str = "Moroccan Real Estate Dashboard"
    PAGE_ICONE: str = "🏠"
