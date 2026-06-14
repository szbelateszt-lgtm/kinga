import logging
from datetime import datetime

from .base_scraper import logger
from .db import get_connection, init_schema
from .indeed_nl_scraper import IndeedNLScraper


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def main():
    logger.info('Initializing Kinga scraper schema...')
    init_schema()

    scraper = IndeedNLScraper(source_id=1)
    listings = scraper.fetch_listings()
    logger.info('Found %d raw listings', len(listings))

    conn = get_connection()
    new_count = 0
    duplicate_count = 0

    for raw in listings:
        job = scraper.parse_listing(raw)
        _, inserted = scraper.save_job(job, conn)
        if inserted:
            new_count += 1
        else:
            duplicate_count += 1

    conn.close()
    logger.info('Inserted %d new jobs, %d duplicates', new_count, duplicate_count)


if __name__ == '__main__':
    main()
