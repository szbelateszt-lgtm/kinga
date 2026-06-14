# GitHub push utasítások

Ez a projekt már készen áll GitHub-ra feltöltésre.

## 1. Git telepítése

Ha a `git` parancs nem elérhető, telepítsd a Git-et:
- Windows: https://git-scm.com/download/win
- Linux: `sudo apt install git` vagy a rendszered csomagkezelője

## 2. Git inicializálása a projekt gyökérben

```powershell
cd C:\xampp\htdocs\g5\kinga
git init
git add .
git commit -m "Initial Kinga scraper project"
```

## 3. Távoli repository beállítása és feltöltés

A GitHub repo URL-je:
`https://github.com/szbelateszt-lgtm/kinga.git`

```powershell
git branch -M main
git remote add origin https://github.com/szbelateszt-lgtm/kinga.git
git push -u origin main
```

## 4. Ellenőrzés

GitHubon nézd meg:
- van-e `main` branch
- működik-e a `.github/workflows/scraper.yml`
- elérhető-e a `data/sample_jobs.csv` és `data/sample_jobs.xml`

## 5. Későbbi futtatás

A GitHub Actions a `push` eseményre és napi ütemezéssel fut.

A helyi futtatáshoz:
```powershell
python -m src.import_example
```
