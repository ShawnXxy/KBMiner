# KBMiner - Knowledge Base Mining Tool

> A unified command-line tool for crawling technical content from various sources

## 📚 Overview

KBMiner provides a unified interface to crawl and organize technical content from multiple sources. Currently supports MySQL-related content from ActionTech and Alibaba database monthly reports.

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/ShawnXxy/KBminer.git
cd KBminer
```

### Basic Usage

```bash
# Crawl all MySQL sources
python miner.py --source mysql

# Incremental crawl (recommended for regular updates)
python miner.py --source mysql --incremental

# Crawl with content download
python miner.py --source mysql --download

# Test mode with limited content
python miner.py --source mysql --test
```

## 💡 Features

### Unified Command Interface
- Single `miner` command for all sources
- Case-insensitive source selection
- Comprehensive help and validation

### Smart Content Filtering
- **ActionTech**: Filters by categories and keywords to focus on MySQL/database content
- **Alibaba**: Includes only MySQL/InnoDB articles, excludes PolarDB, MariaDB, etc.

### Incremental Processing
- Tracks processed content to avoid duplicates
- Only processes new articles on subsequent runs
- Efficient for automated/scheduled crawling

### Flexible Options
- **Test mode**: Validate functionality with limited content
- **Download mode**: Fetch full article content in addition to indexes
- **Verbose logging**: Debug and monitor crawling progress
- **Source selection**: Choose specific sources or crawl all

## 📖 Command Reference

### Required Arguments
```bash
--source, -s {mysql,MySQL,MYSQL}    # Source to crawl (case-insensitive)
```

### Crawling Modes
```bash
--incremental, -i      # Only process new content (recommended)
--full, -f            # Process all content, ignore existing
--download, -d        # Download full article content
--download-only       # Only download existing articles, no new crawling
```

### Testing & Debugging
```bash
--test, -t            # Test mode with limited content
--test-articles       # Test article download functionality
--verbose, -v         # Enable debug logging
--quiet, -q          # Reduce output to warnings only
```

### Source Control
```bash
--sources {actiontech,alibaba,all}  # Specific sources within category
```

## 📁 Output Structure

```
my/
├── actiontech/                     # ActionTech content
│   ├── ActionTech技术干货.md        # Main index file
│   ├── crawl_state.json           # Incremental tracking
│   └── articles/                  # Individual articles (with --download)
└── ali_monthly/                   # Alibaba content
    ├── 阿里数据库内核月报.md         # Main index file
    ├── .processed_months.txt      # Incremental tracking
    └── articles/                  # Individual articles (with --download)
```

## 🎯 Content Sources

### MySQL Sources
- **ActionTech**: Technical blog posts focused on database technologies
- **Alibaba**: Monthly database kernel reports with MySQL/InnoDB insights

## 📊 Statistics

| Source | Articles | Focus | Update Frequency |
|--------|----------|-------|------------------|
| ActionTech | 600+ | Practical MySQL/DB content | Active |
| Alibaba | 450+ | Deep MySQL/InnoDB technical articles | Monthly |

## 🔧 Advanced Usage

### Automated Scheduling

#### Linux/macOS (crontab)
```bash
# Daily incremental update at 8 AM
0 8 * * * cd /path/to/KBminer && python miner.py --source mysql --incremental --quiet
```

#### Windows (Task Scheduler)
- Create basic task for daily execution
- Program: `python`
- Arguments: `miner.py --source mysql --incremental --quiet`
- Start in: `C:\path\to\KBminer`

### Customization

The crawler behavior can be customized by modifying the crawler classes in the `crawlers/` directory:

- `crawlers/actiontech_crawler.py` - ActionTech filtering rules
- `crawlers/ali_crawler.py` - Alibaba filtering rules
- `crawlers/mysql_crawler.py` - MySQL meta-crawler coordination

## 🛠️ Technical Details

### Architecture
- **Object-oriented design** with inheritance and composition
- **High cohesion, low coupling** following SOLID principles
- **Modular crawler system** for easy extension
- **Comprehensive logging** for debugging and monitoring

### Key Classes
- `BaseCrawler`: Abstract base class with common functionality
- `ActionTechCrawler`: ActionTech-specific implementation
- `AliCrawler`: Alibaba monthly reports implementation
- `MySQLCrawler`: Meta-crawler coordinating MySQL sources

### Error Handling
- Graceful failure handling - one source failure doesn't stop others
- Comprehensive logging with configurable levels
- Automatic retry and recovery mechanisms
- Validation of command-line arguments

## 🚦 Examples

### Basic Crawling
```bash
# First-time full crawl
python miner.py --source mysql

# Regular incremental updates
python miner.py --source mysql --incremental
```

### Content Download
```bash
# Crawl and download full articles
python miner.py --source mysql --download

# Download articles from existing indexes only
python miner.py --source mysql --download-only
```

### Testing and Debugging
```bash
# Test with verbose logging
python miner.py --source mysql --test --verbose

# Test specific sources
python miner.py --source mysql --test --sources actiontech

# Quiet mode for automated scripts
python miner.py --source mysql --incremental --quiet
```

## 🔮 Future Extensions

The architecture supports easy addition of new sources:

```bash
# Future possibilities
python miner.py --source postgresql    # PostgreSQL content
python miner.py --source mongodb      # MongoDB content
python miner.py --source redis        # Redis content
```

## 🤝 Contributing

1. Follow the object-oriented design patterns
2. Inherit from `BaseCrawler` for new sources
3. Add comprehensive logging and error handling
4. Include filtering logic appropriate for the source
5. Update this README with new features

## 📄 License

This project is open source and available under the MIT License.

---

**Built with Python 3** | **No external dependencies** | **Cross-platform compatible**
