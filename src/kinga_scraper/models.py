from dataclasses import dataclass
from typing import Optional


@dataclass
class RawListing:
    source_id: int
    url: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    posted_date: Optional[str] = None
    raw_html: Optional[str] = None


@dataclass
class NormalizedJob:
    source_id: int
    fingerprint: str
    title: str
    company: Optional[str] = None
    sector: Optional[str] = None
    position_type: Optional[str] = None
    location_city: Optional[str] = None
    location_country: Optional[str] = None
    is_remote: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    salary_period: Optional[str] = None
    description_full: Optional[str] = None
    url: Optional[str] = None
    secondary_url: Optional[str] = None
    posted_date: Optional[str] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    is_active: Optional[int] = 1
    raw_html: Optional[str] = None
    data_quality_score: Optional[int] = None
    status: Optional[str] = 'new'
    priority: Optional[str] = 'medium'
