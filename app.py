# app.py
from flask import Flask, jsonify, request, send_from_directory
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode, quote_plus
import time

app = Flask(__name__, static_folder=".", static_url_path="")

# --- Defaults ---------------------------------------------------------------
DEFAULT_URL = "https://www.higheredjobs.com/search/advanced_action.cfm?JobCat=115&PosType=1&InstType=1&Keyword=professor+AND+%28civil+OR+infrastructure+OR+construction+OR+building%29&Remote=1&Region=&Submit=Search+Jobs"

# --- Helpers -----------------------------------------------------------------
def build_search_url(required: str, fields: str) -> str:
    """
    Build HigherEdJobs search URL.
    - If inputs are empty -> use DEFAULT_URL (fixed link you provided).
    - Otherwise, compose: required AND (field1 OR field2 ...)
    Keep key flags (JobCat/PosType/InstType/Remote).
    """
    required = (required or "").strip()
    fields = (fields or "").strip()
    if not required and not fields:
        return DEFAULT_URL

    # split fields by comma or pipe
    parts = []
    if "," in fields:
        parts = [p.strip() for p in fields.split(",") if p.strip()]
    elif "|" in fields:
        parts = [p.strip() for p in fields.split("|") if p.strip()]
    elif fields:
        parts = [fields]

    if parts:
        field_expr = " OR ".join(parts)
        keyword_expr = f"{required} AND ({field_expr})" if required else f"({field_expr})"
        keyword_expr = keyword_expr.format(required=required, field_expr=field_expr)
    else:
        keyword_expr = required

    base = "https://www.higheredjobs.com/search/advanced_action.cfm"
    params = {
        "JobCat": 115,
        "PosType": 1,
        "InstType": 1,
        "Remote": 1,
        "Region": "",
        "Submit": "Search Jobs",
        "SortBy": 1,
        "NumJobs": 50,
    }
    kw = quote_plus(keyword_expr)
    return f"{base}?{urlencode(params)}&Keyword={kw}"

def make_driver():
    """Configure a quiet and stable headless Chrome."""
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,2000")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--mute-audio")
    opts.add_argument("--disable-speech-api")
    opts.add_argument("--blink-settings=imagesEnabled=false")
    opts.add_argument("--disable-features=Translate,BackForwardCache,MediaRouter")
    opts.add_argument("--lang=en-US")
    opts.add_argument("--user-agent=Mozilla/5.0")
    opts.add_argument("--log-level=3")
    opts.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    return driver

def scrape_with_selenium(url: str, timeout: int = 30):
    """Load the URL and parse job cards. Return (jobs, debug_html_if_empty)."""
    driver = make_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        candidate_selectors = [
            ".JobListItem", ".jobWrap", ".jobItem",
            ".JobList .Row", ".job-list .job"
        ]
        for sel in candidate_selectors:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                )
                break
            except Exception:
                continue

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        cards = []
        for sel in candidate_selectors:
            cards.extend(soup.select(sel))
        cards = list(dict.fromkeys(cards))

        jobs = []
        for card in cards:
            title_el = (
                card.select_one(".jobTitle a") or
                card.select_one("a[href*='job/']") or
                card.select_one("a")
            )
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            href = (title_el.get("href") or "").strip()
            if href and not href.startswith("http"):
                href = "https://www.higheredjobs.com/" + href.lstrip("/")

            inst_el = (
                card.select_one(".institution, .jobInstitution, .colInst") or
                card.select_one(".Institution, .inst, [data-inst]")
            )
            loc_el = (
                card.select_one(".location, .jobLocation, .colLocation") or
                card.select_one(".Location, .loc, [data-loc]")
            )

            jobs.append({
                "title": title,
                "institution": inst_el.get_text(strip=True) if inst_el else "",
                "location": loc_el.get_text(strip=True) if loc_el else "",
                "url": href
            })

        return jobs, (html if not jobs else None)

    finally:
        time.sleep(1.5)
        driver.quit()

# --- Routes ------------------------------------------------------------------
@app.route("/")
def serve_index():
    """Serve index.html so frontend and API share the same origin."""
    return send_from_directory(".", "index.html")

@app.route("/api/scrape")
def api_scrape():
    """Scrape results and return JSON."""
    required = (request.args.get("required") or "").strip()
    fields = (request.args.get("fields") or "").strip()
    url = build_search_url(required, fields)

    jobs, debug_html = scrape_with_selenium(url)
    if not jobs:
        return jsonify({
            "jobs": [],
            "source": url,
            "note": "no cards parsed; site may have changed or blocked",
            "html_head": (debug_html[:800] if debug_html else "")
        })
    return jsonify({"jobs": jobs, "source": url})

# --- Main --------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
