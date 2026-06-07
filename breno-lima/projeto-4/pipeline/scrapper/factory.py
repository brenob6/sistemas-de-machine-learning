from scrapper.scrapper import Scraper
from scrapper.itausa import ItausaScraper
from scrapper.mrv import MRVScraper


class ScraperFactory:
    _registry: dict[str, type[Scraper]] = {}

    @classmethod
    def register(cls, name: str, scraper_class: type[Scraper]):
        cls._registry[name] = scraper_class

    @classmethod
    def create(cls, name: str) -> Scraper:
        if name not in cls._registry:
            available = ", ".join(cls._registry.keys())
            raise ValueError(
                f"Scraper '{name}' não encontrado. Disponíveis: {available}"
            )
        return cls._registry[name]()


ScraperFactory.register("itausa", ItausaScraper)
ScraperFactory.register("mrv", MRVScraper)
