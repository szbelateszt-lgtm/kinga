import os

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'kinga')

USER_AGENT = os.getenv('USER_AGENT', 'KingaJobScraper/1.0 (+https://github.com)')
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))
RETRY_BACKOFF = int(os.getenv('RETRY_BACKOFF', '2'))
