import csv
import os
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import requests

from .base_scraper import BaseScraper
from .db import get_connection
from .models import NormalizedJob
from .normalizers import normalize_location, normalize_salary, normalize_remote


class ImportScraper(BaseScraper):
    def __init__(self, source_id: int = 0):
        super().__init__(source_id)

    def fetch_listings(self):
        raise NotImplementedError('ImportScraper does not implement fetch_listings')

    def parse_listing(self, raw):
        raise NotImplementedError('ImportScraper does not implement parse_listing')


def download_source(source_url: str, destination: str) -> str:
    response = requests.get(source_url, timeout=30)
    response.raise_for_status()
    with open(destination, 'wb') as target_file:
        target_file.write(response.content)
    return destination


def infer_format(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == '.csv':
        return 'csv'
    if suffix == '.xml':
        return 'xml'
    raise ValueError(f'Nem ismert formátum: {suffix}')


def parse_csv(path: str) -> list[dict[str, Any]]:
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def parse_xml(path: str) -> list[dict[str, Any]]:
    tree = ET.parse(path)
    root = tree.getroot()
    records: list[dict[str, Any]] = []
    for item in root.findall('.//job'):
        record = {}
        for child in item:
            record[child.tag] = child.text or ''
        records.append(record)
    return records


def build_job(record: dict[str, Any]) -> NormalizedJob:
    title = (record.get('title') or record.get('job_title') or '').strip()
    company = (record.get('company') or record.get('employer') or '').strip() or None
    location = (record.get('location') or record.get('city') or '').strip() or None
    description = (record.get('description_full') or record.get('description') or '').strip() or None
    posted_date = (record.get('posted_date') or record.get('date_posted') or '').strip() or None
    url = (record.get('url') or record.get('job_url') or '').strip() or None
    raw_html = (record.get('raw_html') or '').strip() or None
    source_id = int(record.get('source_id')) if record.get('source_id') else None

    location_data = normalize_location(location or '')
    salary_data = normalize_salary(record.get('salary') or '')
    remote_status = normalize_remote(record.get('remote') or location or '')

    job = NormalizedJob(
        source_id=source_id,
        fingerprint=BaseScraper.fingerprint(title, company, location_data.get('location_city')),
        title=title,
        company=company,
        sector=(record.get('sector') or '').strip() or None,
        position_type=(record.get('position_type') or '').strip() or None,
        location_city=location_data.get('location_city'),
        location_country=location_data.get('location_country'),
        is_remote=remote_status,
        salary_min=salary_data.get('salary_min'),
        salary_max=salary_data.get('salary_max'),
        salary_currency=salary_data.get('salary_currency'),
        salary_period=salary_data.get('salary_period'),
        description_full=description,
        url=url,
        posted_date=posted_date,
        raw_html=raw_html,
        data_quality_score=0,
        status=(record.get('status') or 'new').strip() or 'new',
        priority=(record.get('priority') or 'medium').strip() or 'medium',
    )
    job.data_quality_score = ImportScraper(source_id or 0).compute_data_quality(job)
    return job


def import_source(path_or_url: str, fmt: str | None = None) -> dict[str, int]:
    local_path = path_or_url
    if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=Path(path_or_url).suffix)
        tmp_path = tmp_file.name
        tmp_file.close()
        local_path = download_source(path_or_url, tmp_path)

    if fmt is None:
        fmt = infer_format(local_path)

    if fmt == 'csv':
        records = parse_csv(local_path)
    elif fmt == 'xml':
        records = parse_xml(local_path)
    else:
        raise ValueError(f'Unsupported format: {fmt}')

    conn = get_connection()
    imported = 0
    duplicates = 0
    importer = ImportScraper(source_id=0)
    for row in records:
        if not row.get('title'):
            continue
        job = build_job(row)
        _, inserted = importer.save_job(job, conn)
        if inserted:
            imported += 1
        else:
            duplicates += 1
    conn.close()
    return {'imported': imported, 'duplicates': duplicates, 'total': len(records)}
