from atletika_scraper import PrivateCASScraper, PublicCASScraper

from .config import settings

# this file is to prevent creating multiple scraper instances
private_scraper = PrivateCASScraper(
    username=settings.IS_CAS_USERNAME, password=settings.IS_CAS_PASSWORD
)
public_scraper = PublicCASScraper()


def get_private_scraper() -> PrivateCASScraper:
    return private_scraper


def get_public_scraper() -> PublicCASScraper:
    return public_scraper
