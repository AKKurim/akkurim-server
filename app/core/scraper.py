from atletika_scraper import PrivateCASScraper, PublicCASScraper

from .config import settings

# this file is to prevent creating multiple scraper instances
private_scraper = PrivateCASScraper(
    # TODO change the club_id to be configurable
    username=settings.IS_CAS_USERNAME,
    password=settings.IS_CAS_PASSWORD,
    club_id=10245,
)
public_scraper = PublicCASScraper()


def get_private_scraper() -> PrivateCASScraper:
    return private_scraper


def get_public_scraper() -> PublicCASScraper:
    return public_scraper
