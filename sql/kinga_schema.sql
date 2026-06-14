CREATE DATABASE IF NOT EXISTS kinga CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE kinga;

CREATE TABLE IF NOT EXISTS kinga_websites (
  id INT AUTO_INCREMENT PRIMARY KEY,
  url VARCHAR(512) NOT NULL,
  careers_url VARCHAR(512),
  name VARCHAR(255) NOT NULL,
  country VARCHAR(8),
  sector VARCHAR(64),
  source_type ENUM('jobboard','company_careers','manual') DEFAULT 'jobboard',
  language VARCHAR(16),
  scrape_method ENUM('rss','html','api') DEFAULT 'html',
  search_keywords TEXT,
  careers_selector VARCHAR(255),
  listing_selector VARCHAR(255),
  pagination_selector VARCHAR(255),
  last_scraped DATETIME,
  last_success_count INT DEFAULT 0,
  consecutive_failures INT DEFAULT 0,
  is_active TINYINT(1) DEFAULT 1,
  added_by ENUM('user','auto') DEFAULT 'auto',
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS kinga_job_listings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  source_id INT,
  fingerprint VARCHAR(64) NOT NULL,
  title VARCHAR(512) NOT NULL,
  company VARCHAR(255),
  sector VARCHAR(128),
  position_type ENUM('full-time','part-time','freelance','contract') DEFAULT NULL,
  location_city VARCHAR(128),
  location_country VARCHAR(8),
  is_remote ENUM('none','hybrid','full','unknown') DEFAULT 'unknown',
  salary_min INT,
  salary_max INT,
  salary_currency VARCHAR(8),
  salary_period ENUM('monthly','yearly','hourly') DEFAULT NULL,
  description_full LONGTEXT,
  url VARCHAR(1024),
  secondary_url VARCHAR(1024),
  posted_date DATE,
  first_seen DATETIME,
  last_seen DATETIME,
  is_active TINYINT(1) DEFAULT 1,
  raw_html LONGTEXT,
  data_quality_score INT,
  status ENUM('new','viewed','saved','applied','interview','offer','hired','rejected','ignored') DEFAULT 'new',
  priority ENUM('low','medium','high','urgent') DEFAULT 'medium',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_fingerprint (fingerprint),
  INDEX idx_source_id (source_id),
  FOREIGN KEY (source_id) REFERENCES kinga_websites(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS kinga_change_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  job_id INT NOT NULL,
  field_name VARCHAR(128) NOT NULL,
  old_value TEXT,
  new_value TEXT,
  detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (job_id) REFERENCES kinga_job_listings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS kinga_scraper_runs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  started_at DATETIME NOT NULL,
  finished_at DATETIME,
  sources_checked INT DEFAULT 0,
  raw_found INT DEFAULT 0,
  duplicates INT DEFAULT 0,
  new_inserted INT DEFAULT 0,
  errors INT DEFAULT 0,
  quality_report JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS kinga_fuzzy_duplicates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  job_id_a INT NOT NULL,
  job_id_b INT NOT NULL,
  similarity_score FLOAT NOT NULL,
  resolved TINYINT(1) DEFAULT NULL,
  FOREIGN KEY (job_id_a) REFERENCES kinga_job_listings(id) ON DELETE CASCADE,
  FOREIGN KEY (job_id_b) REFERENCES kinga_job_listings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
