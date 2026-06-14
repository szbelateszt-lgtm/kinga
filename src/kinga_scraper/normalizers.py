import re


def normalize_salary(text: str) -> dict:
    if not text:
        return {}

    normalized = {
        'salary_min': None,
        'salary_max': None,
        'salary_currency': None,
        'salary_period': None,
    }

    text = text.replace('\xa0', ' ').replace('\u202f', ' ').strip()
    text_lower = text.lower()

    currency_match = re.search(r'(€|eur|euró|eurós|usd|usd|gbp|£)', text_lower)
    if currency_match:
        symbol = currency_match.group(1)
        if '€' in symbol or 'eur' in symbol:
            normalized['salary_currency'] = 'EUR'
        elif 'usd' in symbol:
            normalized['salary_currency'] = 'USD'
        elif '£' in symbol or 'gbp' in symbol:
            normalized['salary_currency'] = 'GBP'

    if 'per maand' in text_lower or 'per month' in text_lower or 'maand' in text_lower:
        normalized['salary_period'] = 'monthly'
    elif 'per jaar' in text_lower or 'per year' in text_lower or 'yearly' in text_lower or 'jaar' in text_lower:
        normalized['salary_period'] = 'yearly'
    elif 'per uur' in text_lower or 'per hour' in text_lower or 'hourly' in text_lower or 'uur' in text_lower:
        normalized['salary_period'] = 'hourly'

    range_match = re.search(r'(\d+[\.,]?\d*)\s*[kK]?(?:\s*[–-]\s*(\d+[\.,]?\d*)\s*[kK]?)', text)
    if range_match:
        low = range_match.group(1).replace('.', '').replace(',', '.')
        high = range_match.group(2).replace('.', '').replace(',', '.')
        low_value = float(low)
        high_value = float(high)
        if 'k' in text_lower:
            low_value *= 1000
            high_value *= 1000
        normalized['salary_min'] = int(low_value)
        normalized['salary_max'] = int(high_value)
        return normalized

    single_match = re.search(r'(\d+[\.,]?\d*)(?:\s*[kK])?', text)
    if single_match:
        value = single_match.group(1).replace('.', '').replace(',', '.')
        salary_value = float(value)
        if 'k' in text_lower:
            salary_value *= 1000
        normalized['salary_min'] = int(salary_value)
        normalized['salary_max'] = int(salary_value)

    return normalized


def normalize_location(text: str) -> dict:
    if not text:
        return {}

    text_lower = text.lower()
    country = None
    city = None
    is_remote = 'unknown'

    if 'remote' in text_lower or 'thuiswerken' in text_lower or 'work from home' in text_lower:
        is_remote = 'full'
        if 'hybrid' in text_lower or 'hybride' in text_lower or 'gedeeltelijk' in text_lower:
            is_remote = 'hybrid'
    elif 'on-site' in text_lower or 'on site' in text_lower or 'op kantoor' in text_lower:
        is_remote = 'none'

    if 'amsterdam' in text_lower:
        city = 'Amsterdam'
        country = 'NL'
    elif 'rotterdam' in text_lower:
        city = 'Rotterdam'
        country = 'NL'
    elif 'brussel' in text_lower or 'brussels' in text_lower:
        city = 'Brussel'
        country = 'BE'
    elif 'antwerpen' in text_lower or 'antwerp' in text_lower:
        city = 'Antwerpen'
        country = 'BE'
    elif 'berlijn' in text_lower or 'berlin' in text_lower:
        city = 'Berlin'
        country = 'DE'
    elif 'nederland' in text_lower or 'netherlands' in text_lower:
        country = 'NL'
    elif 'belgië' in text_lower or 'belgium' in text_lower or 'belgie' in text_lower:
        country = 'BE'
    elif 'germany' in text_lower or 'deutschland' in text_lower or 'deutsch' in text_lower:
        country = 'DE'
    elif 'eu' in text_lower:
        country = 'EU'

    return {
        'location_city': city,
        'location_country': country,
        'is_remote': is_remote,
    }


def normalize_remote(text: str) -> str:
    if not text:
        return 'unknown'

    text_lower = text.lower()
    if '100% remote' in text_lower or 'remote' in text_lower or 'thuiswerken' in text_lower or 'work from home' in text_lower:
        if 'hybrid' in text_lower or 'hybride' in text_lower or 'gedeeltelijk' in text_lower:
            return 'hybrid'
        return 'full'
    if 'on-site' in text_lower or 'on site' in text_lower or 'op kantoor' in text_lower or 'office' in text_lower:
        return 'none'
    return 'unknown'
