# AI-assisted development log

Date: 2026-02-05

Summary
- Purpose: build a small pipeline to scrape a BBC Future article, clean the scraped data, validate it, and produce a quality report.

Actions performed (chronological)
- Provided a scraping script `scrape_bbc_future.py` that fetches the article and writes `sample_data.json` (user supplied / pre-existing).
- Created `cleaner.py` to:
  - remove HTML artifacts and extra whitespace,
  - normalize Unicode and HTML entities,
  - standardize date fields to ISO format,
  - write cleaned data to `cleaned_output.json`.
  - Verified by running it; output: `cleaned_output.json` written.
- Created `validator.py` to:
  - check required fields (`title`, `content`, `url`),
  - validate URL format,
  - enforce minimum content length,
  - flag invalid records with reasons and write `validation_report.json`.
  - Verified by running it; result: 1 record processed, 1 valid, 0 invalid.
- Generated a short summary and saved it as `validation_summary.json`, then renamed it to `quality_report.txt` per request.
- Added `requirements.txt` to pin the project's runtime dependencies.

Files added or modified
- `cleaner.py` — cleaning script
- `cleaned_output.json` — cleaned data (generated)
- `validator.py` — validation script
- `validation_report.json` — validation results (generated)
- `quality_report.txt` — human-readable summary
- `requirements.txt` — dependency manifest (added)
- `prompt-log.md` — this file

Commands used (Windows cmd.exe)
```
cd /d "c:\Users\carri\OneDrive\Desktop\IIMT3688 Advanced AI Application in Business\Assignment 1"
.\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python cleaner.py sample_data.json cleaned_output.json
python validator.py cleaned_output.json validation_report.json
```

Dependencies (recorded in `requirements.txt`)
- requests >= 2.0.0
- beautifulsoup4 >= 4.9.0
- lxml >= 4.6.0
- python-dateutil >= 2.8.0 (optional but recommended)

Quick verification notes
- `cleaned_output.json` contains cleaned text and an ISO-formatted `scraped_at` timestamp.
- `validation_report.json` shows 1 total record, all valid in this run.
- `quality_report.txt` summarizes completeness and common failures (none for this dataset).
