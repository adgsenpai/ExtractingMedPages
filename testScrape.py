import requests
from bs4 import BeautifulSoup
import json
import re
import time

BASE = "https://www.medpages.info/sf/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MedpagesScraper/1.0)"}

def extract_people(html):
    """Parse one Medpages listing page and return list of dicts."""
    soup = BeautifulSoup(html, "html.parser")
    people = []

    # Check if there are no details
    if "No Details" in soup.text:
        return []

    # Find each result record
    for section in soup.select("section.result-record"):
        person = {}
        h2 = section.find("h2")
        h3 = section.find("h3")
        h4 = section.find("h4")
        desc = section.find("p")
        link = section.find("a", href=re.compile("page=person"))
        person["name"] = h2.get_text(strip=True) if h2 else None
        person["title"] = h3.get_text(strip=True) if h3 else None
        person["location"] = h4.get_text(strip=True) if h4 else None
        person["description"] = desc.get_text(strip=True) if desc else None
        if link:
            person["profile_url"] = BASE + link["href"]
        people.append(person)

    # Optional: extract coordinates from JS var locations
    js_match = re.search(r"var locations\s*=\s*(\[.*?\]);", html, re.S)
    if js_match:
        try:
            import ast
            coords = ast.literal_eval(js_match.group(1))
            for i, loc in enumerate(coords):
                if i < len(people):
                    people[i]["latitude"] = loc[0]
                    people[i]["longitude"] = loc[1]
        except Exception:
            pass

    return people

def extract_pagination(html):
    """Return list of all page numbers."""
    soup = BeautifulSoup(html, "html.parser")
    pages = []
    for a in soup.select("ul.pagination a"):
        m = re.search(r"pageno=(\d+)", a["href"])
        if m:
            pages.append(int(m.group(1)))
    return sorted(set(pages))

def scrape_listing(service_code, delay=1.5):
    """Scrape all pages for a given service code."""
    base_url = f"{BASE}index.php?page=listing&servicecode={service_code}&countryid=1&regioncode=0&subregioncode=0&suburbcode=0"
    r = requests.get(base_url, headers=HEADERS)
    if r.status_code != 200:
        print(f"Failed to fetch {base_url}")
        return []

    html = r.text
    all_people = extract_people(html)
    pages = extract_pagination(html)

    for p in pages[1:]:  # skip first
        url = f"{base_url}&pageno={p}"
        time.sleep(delay)
        print(f"Scraping page {p} for service {service_code}...")
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            all_people.extend(extract_people(r.text))

    return all_people

# Example: scrape all clinical psychologists (servicecode=496)
data = {"Psychologist - Clinical": scrape_listing(496)}

# Save to nested JSON
with open("medpages_psychologists.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Done — saved to medpages_psychologists.json")
