# 🏥 MedPages Scraper

A high-performance parallel web scraper for extracting healthcare professional data from MedPages.info.

## ✨ Features

- 🚀 **Parallel Processing**: Leverages all CPU cores for maximum performance
- 📊 **Comprehensive Coverage**: Scrapes 100+ medical service categories
- 🔄 **Automated Updates**: GitHub Actions workflow for scheduled scraping
- 💾 **JSON Output**: Clean, structured data in JSON format
- 📦 **CI/CD Ready**: Automatic artifact upload and repository commits

## 🖥️ System Requirements

- Python 3.10+
- Multi-core processor (automatically detected and utilized)
- Internet connection

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/adgsenpai/ExtractingMedPages.git
cd ExtractingMedPages

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Local Execution

```bash
python scrapeAll.py
```

The script will:
1. Auto-detect your CPU cores
2. Spawn optimal number of worker threads (2x CPU cores, max 16)
3. Scrape all services in parallel
4. Save results to `medpages_all_data.json`

### Performance

- **Sequential**: ~150 seconds for 100 services
- **Parallel (8 cores)**: ~20-30 seconds for 100 services
- **Speed improvement**: 5-7x faster

## 📋 Data Sources

The scraper reads from two CSV files:

1. `medpages_full_links.csv` - General medical practitioners
2. `medpages_mental_health.csv` - Mental health professionals

## 📁 Output Format

```json
{
  "Service Name": [
    {
      "name": "Dr. John Doe",
      "title": "Clinical Psychologist",
      "location": "Cape Town, Western Cape",
      "description": "Specializes in...",
      "profile_url": "https://www.medpages.info/sf/...",
      "latitude": -33.9249,
      "longitude": 18.4241
    }
  ]
}
```

## 🤖 GitHub Actions Workflow

### Triggers

- **Manual**: Via workflow_dispatch
- **Scheduled**: Every Sunday at 00:00 UTC
- **Automatic**: On push to main (if scraper files change)

### What it does

1. ✅ Runs the scraper on Ubuntu (latest)
2. 📊 Generates summary statistics
3. 📤 Uploads JSON as artifact (90-day retention)
4. 🔄 Commits and pushes data back to repository

### Running Manually

1. Go to **Actions** tab in GitHub
2. Select **Scrape MedPages Data** workflow
3. Click **Run workflow**
4. Download artifact from workflow run

## 📊 Output Statistics

The scraper provides detailed statistics:

- Total services scraped
- Total professionals found
- Execution time
- Average time per service
- CPU cores utilized
- Worker threads spawned

## 🔧 Configuration

### Adjust Workers

Edit `scrapeAll.py`:

```python
max_workers = min(cpu_count * 2, 16)  # Adjust multiplier or max
```

### Change Delay

```python
def scrape_listing(service_name, service_code, total_services, delay=0.5):
```

Increase `delay` if you encounter rate limiting.

## 📝 CSV Format

Your CSV files should have these columns:

```csv
Name,Full URL
Service Name,https://www.medpages.info/sf/index.php?page=listing&servicecode=123...
```

The scraper automatically extracts the service code from URLs.

## 🛠️ Technologies

- **requests**: HTTP client
- **BeautifulSoup4**: HTML parsing
- **ThreadPoolExecutor**: Parallel processing
- **GitHub Actions**: CI/CD automation

## 📈 Performance Tips

1. **Increase workers** for faster scraping (if server allows)
2. **Reduce delay** between requests (use responsibly)
3. **Use SSD** for faster I/O operations
4. **Run on dedicated server** for uninterrupted execution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect MedPages.info's terms of service and rate limits.

## ⚠️ Disclaimer

This scraper is intended for research and data analysis purposes. Always:
- Respect robots.txt
- Use reasonable rate limiting
- Comply with website terms of service
- Don't overload servers

## 🐛 Troubleshooting

### "Failed to fetch" errors
- Check internet connection
- Verify service codes in CSV files
- Increase timeout in `requests.get(..., timeout=30)`

### Rate limiting
- Increase delay between requests
- Reduce number of workers
- Add exponential backoff

### Memory issues
- Process services in batches
- Write to file incrementally
- Reduce max_workers

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ by [ADGSENPAI](https://github.com/adgsenpai)
