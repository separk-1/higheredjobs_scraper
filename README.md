# HigherEdJobs Scraper

This project provides a simple web-based interface and backend service for scraping job postings from [HigherEdJobs](https://www.higheredjobs.com/). It allows users to filter academic job postings by keywords and categories, and view them in multiple formats.

## Features

- **Backend (Flask + Requests/BeautifulSoup)**
  - `/api/scrape`: Scrapes HigherEdJobs with either the default preset search or user-provided keywords/fields.
  - Uses a default query: `professor AND (civil OR infrastructure OR construction OR building)` with remote jobs included.
  - Returns results in JSON format: title, institution, location, and job URL.

- **Frontend (HTML + CSS + JavaScript)**
  - Simple UI with input fields for *Required Keywords* and *Optional Fields*.
  - Default values are pre-filled with the same query as the backend preset.
  - Tabs to view results as:
    - **Job Cards** (clean UI list)
    - **JSON Viewer**
    - **Raw HTML**
  - Action buttons:
    - Start / Stop auto-scraping (polling every few seconds)
    - Run once
    - Reset to default query
    - Clear log/results
  - Export results to JSON, HTML, or CSV.

- **Styling**
  - Minimal dark-themed design (`styles.css`).
  - Responsive layout with clean form grid and results panel.

## Usage

1. Create a virtual environment:
   ```bash
   conda create -n job_scraper python==3.10
   conda activate job_scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```bash
   python app.py
   ```

4. Open the frontend in a browser:
   ```
   http://localhost:5000
   ```

## Notes

- HigherEdJobs may change their HTML structure at any time, so CSS selectors may need updates.
- This tool is intended for personal/research use. Respect the website's terms of service.
- Default query is automatically applied if no input is provided, but users can override via the form.

