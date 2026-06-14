from .importer import import_source


if __name__ == '__main__':
    sample_url = 'https://raw.githubusercontent.com/<your-user>/<repo>/main/data/sample_jobs.csv'
    result = import_source(sample_url)
    print(f"Imported={result['imported']}, Duplicates={result['duplicates']}, Total={result['total']}")
