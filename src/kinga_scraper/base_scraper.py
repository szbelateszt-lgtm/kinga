import hashlib
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from .config import REQUEST_TIMEOUT, RETRY_ATTEMPTS, RETRY_BACKOFF, USER_AGENT
from .models import RawListing, NormalizedJob
from .normalizers import normalize_location, normalize_salary, normalize_remote


logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    def __init__(self, source_id: int):
        self.source_id = source_id

    @abstractmethod
    def fetch_listings(self) -> list[RawListing]:
        raise NotImplementedError

    @abstractmethod
    def parse_listing(self, raw: RawListing) -> NormalizedJob:
        raise NotImplementedError

    def request(self, url: str) -> requests.Response:
        session = requests.Session()
        session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Referer': 'https://www.google.com/',
        })
        last_exception = None
        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                response = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
                response.raise_for_status()
                return response
            except Exception as exc:
                logger.warning('Request failed (%s): %s', attempt, exc)
                last_exception = exc
                time.sleep(RETRY_BACKOFF ** attempt)
        raise last_exception

    @staticmethod
    def fingerprint(title: str, company: str | None, city: str | None) -> str:
        normalized = f"{title or ''}|{(company or '').lower()}|{(city or '').lower()}"
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    def compute_data_quality(self, job: NormalizedJob) -> int:
        score = 0
        if job.title:
            score += 10
        if job.company:
            score += 10
        if job.location_city or job.location_country:
            score += 10
        if job.url:
            score += 10
        if job.description_full:
            score += 10
        if job.salary_min or job.salary_max:
            score += 10
        if job.is_remote and job.is_remote != 'unknown':
            score += 10
        if job.position_type:
            score += 5
        if job.posted_date:
            score += 5
        if job.sector:
            score += 5
        return min(score * 2, 100)

    def save_job(self, job: NormalizedJob, connection):
        cursor = connection.cursor()
        existing = None
        cursor.execute(
            'SELECT id FROM kinga_job_listings WHERE fingerprint = %s',
            (job.fingerprint,)
        )
        row = cursor.fetchone()
        if row:
            existing = row[0]

        if existing:
            cursor.execute(
                'UPDATE kinga_job_listings SET last_seen = NOW(), is_active = 1, updated_at = NOW() WHERE id = %s',
                (existing,)
            )
            connection.commit()
            return existing, False

        cursor.execute(
            '''INSERT INTO kinga_job_listings
               (source_id, fingerprint, title, company, sector, position_type,
                location_city, location_country, is_remote, salary_min, salary_max,
                salary_currency, salary_period, description_full, url, posted_date,
                first_seen, last_seen, is_active, raw_html, data_quality_score,
                status, priority, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), 1, %s, %s, %s, %s, NOW(), NOW())''',
            (
                job.source_id,
                job.fingerprint,
                job.title,
                job.company,
                job.sector,
                job.position_type,
                job.location_city,
                job.location_country,
                job.is_remote,
                job.salary_min,
                job.salary_max,
                job.salary_currency,
                job.salary_period,
                job.description_full,
                job.url,
                job.posted_date,
                job.raw_html,
                job.data_quality_score,
                job.status,
                job.priority,
            )
        )
        connection.commit()
        return cursor.lastrowid, True

    def parse_common(self, raw: RawListing) -> NormalizedJob:
        location = normalize_location(raw.location or '')
        salary = normalize_salary(raw.description or '')
        remote = normalize_remote(raw.location or '')

        job = NormalizedJob(
            source_id=self.source_id,
            fingerprint=self.fingerprint(raw.title, raw.company, location.get('location_city')),
            title=raw.title,
            company=raw.company,
            sector=None,
            position_type=None,
            location_city=location.get('location_city'),
            location_country=location.get('location_country'),
            is_remote=remote,
            salary_min=salary.get('salary_min'),
            salary_max=salary.get('salary_max'),
            salary_currency=salary.get('salary_currency'),
            salary_period=salary.get('salary_period'),
            description_full=raw.description,
            url=raw.url,
            posted_date=raw.posted_date,
            raw_html=raw.raw_html,
            data_quality_score=0,
        )
        job.data_quality_score = self.compute_data_quality(job)
        return job
