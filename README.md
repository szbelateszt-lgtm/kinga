# Kinga Job Scraper

Python alapú scraper projekt a `kinga` MySQL adatbázishoz.

## Mi készült el
- MySQL sémák a `kinga_` prefixszel
- Python scraper architektúra `BaseScraper`, `IndeedNLScraper` és normalizáló modulok
- GitHub Actions workflow, amely lefuttatja a scrappert GitHubon és létrehozza a `kinga` adatbázist

## Futtatás helyben
1. másold a projektet egy Python 3.11 környezetbe
2. telepítsd a függőségeket:
   ```bash
   pip install -r requirements.txt
   ```
3. állítsd be a környezeti változókat:
   - `MYSQL_HOST`
   - `MYSQL_PORT`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
   - `MYSQL_DATABASE`

4. futtasd:
   ```bash
   python -m src.kinga_scraper.run
   ```

## GitHub Actions
A `.github/workflows/scraper.yml` file automatikusan futtatja a scrapert `push` eseményre és napi ütemezéssel.

## GitHub CSV/XML import
A `src/kinga_scraper/importer.py` modul GitHub-ról érkező CSV vagy XML fájlok importálására készült.

Példa futtatás helyben:
```bash
python -m src.import_example
```

GitHub URL-ről CSV import:
```bash
python -c "from src.kinga_scraper.importer import import_source; print(import_source('https://raw.githubusercontent.com/<user>/<repo>/main/data/sample_jobs.csv'))"
```

GitHub URL-ről XML import:
```bash
python -c "from src.kinga_scraper.importer import import_source; print(import_source('https://raw.githubusercontent.com/<user>/<repo>/main/data/sample_jobs.xml'))"
```

## Adatbázis
A `sql/kinga_schema.sql` fájl létrehozza a szükséges táblákat a `kinga` adatbázisban.
