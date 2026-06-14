from .importer import import_source
from .db import init_schema


if __name__ == '__main__':
    sample_url = 'https://raw.githubusercontent.com/szbelateszt-lgtm/kinga/main/data/sample_jobs.csv'
    init_schema()
    result = import_source(sample_url)
    print(f"Imported={result['imported']}, Duplicates={result['duplicates']}, Total={result['total']}")
