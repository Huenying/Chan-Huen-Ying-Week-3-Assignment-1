# BBC Web scraping — Data cleaning & Data validation

This repository contains a small pipeline to scrape a BBC Future article, clean the scraped data, validate it, and produce a simple quality report.

Files of interest
- `scrape_bbc_future.py` — (provided) scraper for the BBC Future article; writes `sample_data.json`.
- `cleaner.py` — cleans `sample_data.json` and writes `cleaned_output.json`.
- `validator.py` — validates `cleaned_output.json` and writes `validation_report.json`.
- `quality_report.txt` — human-readable summary of validation results.
- `requirements.txt` — Python dependencies.

Quick setup (Windows, cmd.exe)
1. Create and activate a virtual environment in the project folder:

```cmd
cd /d "c:\Users\carri\OneDrive\Desktop\IIMT3688 Advanced AI Application in Business\Assignment 1"
python -m venv .venv
.\.venv\Scripts\activate.bat
```

2. Install dependencies:

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the pipeline

```cmd
python cleaner.py sample_data.json cleaned_output.json
python validator.py cleaned_output.json validation_report.json
```

Outputs
- `cleaned_output.json` — cleaned and normalized JSON ready for downstream use.
- `validation_report.json` — per-record validation results.
- `quality_report.txt` — aggregated completeness and quality summary.

Notes
- `python-dateutil` is optional but improves date parsing; it is included in `requirements.txt`.
- If BeautifulSoup raises the MarkupResemblesLocatorWarning during HTML stripping, it is harmless for local text cleaning and can be suppressed if desired.
