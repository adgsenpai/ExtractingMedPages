from bs4 import BeautifulSoup
import csv

# Paste your HTML content here (or load it from file)
html = """
<table class="table-condensed table-dropdown">
		<tbody>
			<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=143" class="larger-body-16">Psychologist</a></td>
	<td><span class="badge">231</span></td>
</tr>
<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=496" class="larger-body-16">Psychologist - Clinical</a></td>
	<td><span class="badge">3,147</span></td>
</tr>
<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=497" class="larger-body-16">Psychologist - Counselling</a></td>
	<td><span class="badge">1,603</span></td>
</tr>
<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=498" class="larger-body-16">Psychologist - Educational</a></td>
	<td><span class="badge">1,488</span></td>
</tr>
<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=499" class="larger-body-16">Psychologist - Industrial</a></td>
	<td><span class="badge">421</span></td>
</tr>
<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=956" class="larger-body-16">Psychologist - Neuro</a></td>
	<td><span class="badge">70</span></td>
</tr>
<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=500" class="larger-body-16">Psychologist - Research</a></td>
	<td><span class="badge">34</span></td>
</tr>
<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=455" class="larger-body-16">Psychometrist</a></td>
	<td><span class="badge">459</span></td>
</tr>
<tr>
	<td><a href="index.php?page=servicecountry&amp;servicecode=554" class="larger-body-16">Registered Counsellor</a></td>
	<td><span class="badge">1,493</span></td>
</tr>

		</tbody>
	</table>
"""

# Parse the HTML
soup = BeautifulSoup(html, "html.parser")

# Define your base URL (this will be concatenated)
base_url = "https://www.medpages.info/sf/index.php?page=listing&servicecode=857&countryid=1&regioncode=&subregioncode="

# Extract all hrefs inside <a> tags in the table
links = []
for a in soup.select("table.table-dropdown a"):
    href = a.get("href")
    name = a.get_text(strip=True)
    if href:
        full_url = base_url + href  # concatenate the given base with each href
        links.append((name, full_url))

# Save to CSV
with open("medpages_mental_health.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Full URL"])
    writer.writerows(links)

print(f"✅ Extracted {len(links)} links and saved to medpages_full_links.csv")
for name, url in links[:5]:  # show first 5 for preview
    print(name, "→", url)
