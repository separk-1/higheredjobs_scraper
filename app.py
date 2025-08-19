# app.py (Playwright version)
from flask import Flask, jsonify, request, send_from_directory
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus
from playwright.sync_api import sync_playwright
import time

app = Flask(__name__, static_folder=".", static_url_path="")
DEFAULT_URL = "https://www.higheredjobs.com/search/advanced_action.cfm?JobCat=115&PosType=1&InstType=1&Keyword=professor+AND+%28civil+OR+infrastructure+OR+construction+OR+building%29&Remote=1&Region=&Submit=Search+Jobs&SortBy=1&NumJobs=50"

def build_search_url(required: str, fields: str) -> str:
    required = (required or "").strip()
    fields = (fields or "").strip()
    if not required and not fields:
        return DEFAULT_URL
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

def scrape_with_playwright(url: str, timeout_ms: int = 35000):
    """Load URL in headless Chromium (Playwright) and parse job cards.
    Returns (jobs, html_if_empty)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"
        ])
        context = browser.new_context(
            user_agent="Mozilla/5.0",
            locale="en-US",
            viewport={"width":1280, "height":2000},
        )
        # Stealth-lite: hide webdriver
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # Block images to be gentle
        context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())
        page = context.new_page()
        page.set_default_timeout(timeout_ms)
        page.goto(url, wait_until="domcontentloaded")
        # Let JS/WAF finish their checks
        page.wait_for_load_state("networkidle")
        time.sleep(1.0)

        # Collect HTML from main frame + iframes
        html_blobs = [page.content()]
        for fr in page.frames:
            try:
                if fr != page.main_frame:
                    html_blobs.append(fr.content())
            except Exception:
                pass

        jobs = []
        selectors = [
            ".JobListItem", ".jobWrap", ".jobItem",
            ".JobList .Row", ".job-list .job", "article[class*='job']",
            "li[class*='job']", "div[class*='job']"
        ]

        def add_job(title_el, root):
            if not title_el: return
            title = title_el.get_text(strip=True)
            href = (title_el.get("href") or "").strip()
            if href and not href.startswith("http"):
                href = "https://www.higheredjobs.com/" + href.lstrip("/")
            inst_el = root.select_one(".institution, .jobInstitution, .colInst, [data-inst]")
            loc_el  = root.select_one(".location, .jobLocation, .colLocation, [data-loc]")
            jobs.append({
                "title": title,
                "institution": inst_el.get_text(strip=True) if inst_el else "",
                "location":  loc_el.get_text(strip=True)  if loc_el  else "",
                "url": href
            })

        for html in html_blobs:
            if "Incapsula" in html or "Access denied" in html or "way-All-which-sitie" in html:
                context.close(); browser.close()
                return [], html
            soup = BeautifulSoup(html, "html.parser")
            cards = []
            for sel in selectors:
                cards.extend(soup.select(sel))
            # Card-based
            for c in dict.fromkeys(cards):
                t = (c.select_one(".jobTitle a") or
                     c.select_one("a[href*='job/']") or
                     c.select_one("a[href*='jobdetails']") or
                     c.select_one("a"))
                add_job(t, c)
            # Fallback: link-pattern only
            if not jobs:
                for a in soup.select("a[href]"):
                    h = a.get("href","")
                    if ("job" in h or "Job" in h) and ("higheredjobs.com" in h or h.startswith("/")):
                        add_job(a, soup)

        context.close()
        browser.close()
        return jobs, (html_blobs[0] if not jobs else None)

@app.route("/")
def root():
    return send_from_directory(".", "index.html")

@app.route("/api/scrape")
def api_scrape():
    required = (request.args.get("required") or "").strip()
    fields   = (request.args.get("fields") or "").strip()
    url = build_search_url(required, fields)
    jobs, dbg = scrape_with_playwright(url)
    if not jobs:
        return jsonify({"jobs": [], "source": url, "note": "blocked or zero results", "html_head": (dbg[:800] if dbg else "")})
    return jsonify({"jobs": jobs, "source": url})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
