import requests
from bs4 import BeautifulSoup
import json
import re
import time
import csv
from urllib.parse import urlparse, parse_qs

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

def extract_service_code(url):
    """Extract service code from URL - get the LAST servicecode parameter."""
    # Find all servicecode occurrences
    matches = re.findall(r'servicecode=(\d+)', url)
    
    if matches:
        # Return the LAST service code found (the actual service, not the parent category)
        return matches[-1]
    
    return None

def scrape_listing(service_name, service_code, delay=1.5):
    """Scrape all pages for a given service code."""
    base_url = f"{BASE}index.php?page=listing&servicecode={service_code}&countryid=1&regioncode=0&subregioncode=0&suburbcode=0"
    
    print(f"\n🔍 Scraping {service_name} (service code: {service_code})...")
    
    try:
        r = requests.get(base_url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print(f"   ❌ Failed to fetch (status {r.status_code})")
            return []

        html = r.text
        all_people = extract_people(html)
        pages = extract_pagination(html)

        if not all_people and not pages:
            print(f"   ℹ️  No results found")
            return []

        print(f"   ✓ Found {len(all_people)} results on page 1")

        for p in pages[1:]:  # skip first page
            url = f"{base_url}&pageno={p}"
            time.sleep(delay)
            print(f"   📄 Scraping page {p}...")
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                page_people = extract_people(r.text)
                all_people.extend(page_people)
                print(f"      ✓ Found {len(page_people)} results")

        print(f"   ✅ Total: {len(all_people)} results for {service_name}")
        return all_people
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return []

def load_services_from_csv(csv_file):
    """Load service names and codes from CSV file."""
    services = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name']
            url = row['Full URL']
            service_code = extract_service_code(url)
            
            if service_code:
                services.append({
                    'name': name,
                    'code': service_code
                })
            else:
                print(f"⚠️  Could not extract service code from {name}: {url}")
    
    return services

# Main scraping logic
print("=" * 70)
print("🚀 Starting Medpages Scraper")
print("=" * 70)

# Load services from both CSV files
print("\n📂 Loading services from CSV files...")
services_full = load_services_from_csv("medpages_full_links.csv")
services_mental = load_services_from_csv("medpages_mental_health.csv")

# Combine and deduplicate services
all_services = {}
for service in services_full + services_mental:
    # Use service code as key to avoid duplicates
    all_services[service['code']] = service['name']

print(f"✓ Loaded {len(all_services)} unique services")

# Scrape all services
all_data = {}
total_services = len(all_services)
current = 0

for service_code, service_name in all_services.items():
    current += 1
    print(f"\n[{current}/{total_services}]", end=" ")
    
    people = scrape_listing(service_name, service_code)
    
    if people:
        all_data[service_name] = people
    
    # Be respectful with rate limiting
    time.sleep(1.5)

# Save to JSON
output_file = "medpages_all_data.json"
print(f"\n{'=' * 70}")
print(f"💾 Saving data to {output_file}...")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

# Print summary
total_people = sum(len(people) for people in all_data.values())
print(f"✅ Done!")
print(f"📊 Summary:")
print(f"   - Services scraped: {len(all_data)}")
print(f"   - Total professionals: {total_people}")
print(f"   - Output file: {output_file}")
print("=" * 70)
