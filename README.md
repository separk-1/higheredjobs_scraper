# 🏗️ Civil Engineering Professor Job Scraper

A comprehensive web application for automatically collecting and monitoring professor job postings in Civil Engineering, Construction Management, and Building Sciences from HigherEdJobs.com.

## 🌟 Features

### 🔍 Smart Filtering System
- **Required Keywords (AND)**: Ensure all specified terms are present (e.g., "professor")
- **Field Keywords (OR)**: Match any of the specified field terms (e.g., "civil", "construction", "building")
- Advanced text matching across job titles, descriptions, and specializations

### 📊 Real-time Monitoring
- **Automated Scraping**: Set custom intervals (60-3600 seconds)
- **Live Status Dashboard**: Monitor scraping status, job counts, and next update countdown
- **Manual Override**: Run scraping manually at any time

### 💾 Multiple Export Formats
- **JSON**: Structured data with metadata and search criteria
- **HTML**: Formatted web page ready for sharing
- **CSV**: Spreadsheet-compatible format for analysis

### 🎯 Civil Engineering Focus
Specialized for academic positions in:
- Civil Engineering
- Construction Management
- Building Sciences
- Structural Engineering
- Building Information Modeling (BIM)
- Sustainable Construction
- Smart Buildings
- Infrastructure Systems

## 🚀 Quick Start

### Option 1: GitHub Pages (Recommended)
1. Fork this repository
2. Enable GitHub Pages in repository settings
3. Access your app at `https://yourusername.github.io/civil-engineering-job-scraper`

### Option 2: Local Development
1. Clone the repository:
```bash
git clone https://github.com/yourusername/civil-engineering-job-scraper.git
cd civil-engineering-job-scraper
```

2. Open `index.html` in your browser or serve it locally:
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000
```

3. Navigate to `http://localhost:8000`

## 🎮 Usage Guide

### Basic Operation
1. **Configure Keywords**: Set your required keywords (must include "professor") and field keywords
2. **Set Interval**: Choose update frequency (300 seconds recommended)
3. **Start Scraping**: Click "Start Scraping" to begin automated collection
4. **Monitor Progress**: Watch the status dashboard for real-time updates

### Advanced Features
- **Manual Run**: Force immediate scraping outside the scheduled interval
- **Data Management**: Clear collected data when needed
- **Export Options**: Download data in JSON, HTML, or CSV formats
- **Tab Navigation**: Switch between job listings, raw JSON, and HTML preview

### Keyword Configuration Examples
- **Basic**: Required: `professor`, Field: `civil, construction, building`
- **Specific**: Required: `assistant professor`, Field: `structural, geotechnical`
- **Broad**: Required: `professor`, Field: `civil, construction, building, infrastructure, BIM`

## 📁 Project Structure

```
civil-engineering-job-scraper/
├── index.html          # Main application file
├── README.md           # This file
├── LICENSE             # MIT License
└── docs/              # Documentation (optional)
    └── screenshots/   # Application screenshots
```

## 🛠️ Technical Details

### Current Implementation
- **Frontend**: Pure HTML5, CSS3, JavaScript (ES6+)
- **Storage**: Browser memory (session-based)
- **Data Source**: Mock data generator (for demonstration)
- **Responsive Design**: Mobile-friendly interface

### Production Requirements
For real-world deployment, you'll need:

1. **Backend Service** (Python/Node.js):
```python
# Example Python backend with Flask + BeautifulSoup
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/api/scrape')
def scrape_jobs():
    # Implement actual scraping logic
    return jsonify({"jobs": []})
```

2. **CORS Proxy** (to bypass browser restrictions):
```javascript
// Use a proxy service or set up your own
const PROXY_URL = 'https://cors-anywhere.herokuapp.com/';
const TARGET_URL = 'https://www.higheredjobs.com/search/...';
```

3. **Database Integration** (optional):
```sql
-- PostgreSQL schema example
CREATE TABLE job_postings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    institution VARCHAR(255),
    location VARCHAR(100),
    posted_date DATE,
    scraped_at TIMESTAMP DEFAULT NOW()
);
```

## 🚧 Development Roadmap

### Phase 1: Core Features ✅
- [x] Mock data generation
- [x] Keyword filtering system
- [x] Real-time status monitoring
- [x] Export functionality
- [x] Responsive design

### Phase 2: Backend Integration 🚧
- [ ] Python/Flask backend
- [ ] Real web scraping implementation
- [ ] Rate limiting and error handling
- [ ] API endpoints for data access

### Phase 3: Advanced Features 📋
- [ ] Email notifications for new jobs
- [ ] Job alerts based on criteria
- [ ] Historical data tracking
- [ ] Advanced search filters
- [ ] University ranking integration

### Phase 4: Production Ready 🎯
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Database optimization
- [ ] Monitoring and logging
- [ ] Scale handling

## ⚠️ Important Notes

### Legal Considerations
- **Respect robots.txt**: Always check and comply with website scraping policies
- **Rate Limiting**: Implement appropriate delays between requests
- **Terms of Service**: Review and comply with HigherEdJobs.com terms
- **Academic Use**: Consider reaching out for API access or partnerships

### Ethical Scraping
- Use reasonable request intervals (300+ seconds recommended)
- Don't overwhelm the target server
- Respect website structure and don't scrape unnecessary data
- Consider caching to reduce repeated requests

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/civil-engineering-job-scraper.git

# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes
# Test thoroughly

# Commit and push
git add .
git commit -m "Description of your changes"
git push origin feature/your-feature-name
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/yourusername/civil-engineering-job-scraper/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/civil-engineering-job-scraper/discussions)
- **Email**: Contact the maintainer at your.email@domain.com

## 📊 Screenshots

### Main Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Job Listings
![Job Listings](docs/screenshots/job-listings.png)

### Export Options
![Export](docs/screenshots/export-options.png)

## 🙏 Acknowledgments

- **HigherEdJobs.com** for providing academic job listings
- **Open Source Libraries** used in this project
- **Contributors** who help improve the project
- **Academic Community** for feedback and suggestions

---

**⭐ Star this repository if you find it useful!**

**🍴 Fork it to create your own version!**

**🐛 Report issues to help us improve!**