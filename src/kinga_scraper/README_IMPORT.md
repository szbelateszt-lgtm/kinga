# Import from GitHub in Actions

This project now supports importing sample job data directly from GitHub instead of scraping Indeed.

## How it works

- `src/kinga_scraper/importer.py` downloads CSV or XML files from GitHub.
- `src/kinga_scraper/import_example.py` points to the sample CSV in `szbelateszt-lgtm/kinga`.
- The workflow runs `python -m src.kinga_scraper.import_example`.

## Run locally

```bash
cd C:\xampp\htdocs\g5\kinga
python -m src.kinga_scraper.import_example
```

## Run in GitHub Actions

The workflow now uses the GitHub-hosted sample file instead of calling Indeed.
