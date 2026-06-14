# Manual GitHub Actions Run

A GitHub workflow mostantól manuálisan is indítható.

## Mit kell tenni

1. Commitold a változtatást:
```powershell
git add .github/workflows/scraper.yml
git commit -m "Enable manual workflow dispatch"
```

2. Pushold fel:
```powershell
git push
```

3. A GitHub repo `Actions` oldalán kattints a `Kinga scraper` workflow-re.

4. Kattints a `Run workflow` gombra.

5. Válaszd a `main` branch-et és indítsd el.
