from bs4 import BeautifulSoup

from .base_scraper import BaseScraper
from .models import RawListing


class IndeedNLScraper(BaseScraper):
    BASE_URL = 'https://www.indeed.nl'

    def __init__(self, source_id: int = 1):
        super().__init__(source_id)

    def fetch_listings(self) -> list[RawListing]:
        url = f'{self.BASE_URL}/jobs?q=healthcare+wellness+sport&l=Netherlands'
        response = self.request(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.select('a.tapItem')
        listings = []

        for card in job_cards:
            title_tag = card.select_one('h2.jobTitle span')
            company_tag = card.select_one('span.companyName')
            location_tag = card.select_one('div.companyLocation')
            summary_tag = card.select_one('div.job-snippet')
            link = card.get('href')
            if not title_tag or not link:
                continue

            url = link if link.startswith('http') else f'{self.BASE_URL}{link}'
            listings.append(RawListing(
                source_id=self.source_id,
                url=url,
                title=title_tag.get_text(strip=True),
                company=company_tag.get_text(strip=True) if company_tag else None,
                location=location_tag.get_text(strip=True) if location_tag else None,
                description=summary_tag.get_text(separator=' ', strip=True) if summary_tag else None,
                raw_html=str(card),
            ))
        return listings

    def parse_listing(self, raw: RawListing):
        return self.parse_common(raw)
