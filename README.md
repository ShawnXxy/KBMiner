# MySQL Knowledge Base Miner

A powerful Python crawler for building a comprehensive MySQL knowledge base from Alibaba's Database Kernel Monthly Reports.

## 🎯 Features

- **Incremental Updates**: Only processes new monthly reports, avoiding redundant work
- **Smart Content Filtering**: Focuses on MySQL/InnoDB content while excluding other database technologies
- **Individual Article Download**: Extracts full content from each article and saves as separate markdown files
- **Automatic Image Management**: Downloads all images and creates local references in markdown files
- **Progress Tracking**: Maintains processing state for reliable resumption after interruptions
- **Clean Output**: Well-organized markdown files with proper formatting and metadata

## 📁 Output Structure

```
ali_monthly/
├── 阿里数据库内核月报.md          # Summary with all article links
├── .processed_months.txt          # Tracking file for incremental updates
└── articles/                      # Individual article contents
    ├── .img/                      # Downloaded images (shared folder)
    │   ├── db2d90cc428f_optimizer_logical_arch.png (2.4MB)
    │   ├── 34ba0cd650e7_optimizer_code_arch.png (368KB)
    │   ├── 432b9559c8ae_Query_expression.png (312KB)
    │   └── ... (all images with unique naming)
    ├── 2025-05_MySQL无锁哈希表LF_HASH.md
    ├── 2024-12_MySQL优化器代码速览.md (with 6 images)
    ├── 2024-12_MySQL查询优化分析-常见慢查问题与优化方法.md
    └── ... (453 total articles)
```

## 🖼️ Image Management

The crawler automatically handles images with advanced features:

- **Automatic Detection**: Finds all images in article HTML content
- **Smart Download**: Downloads images to a shared `.img` folder under articles
- **Unique Naming**: Uses URL hash + original filename to prevent conflicts
- **Local References**: Updates markdown to use relative paths (`![description](.img/filename.png)`)
- **Format Support**: Handles PNG, JPG, GIF, and other web image formats
- **Size Optimization**: Preserves original image quality and dimensions
- **Deduplication**: Skips re-downloading existing images

## 🚀 Usage

### Basic Commands

```bash
# Update summary with new monthly reports
python ali_crawler.py

# Download a few sample articles for testing
python ali_crawler.py --test-articles

# Download ALL individual articles (may take time)
python ali_crawler.py --download-articles

# Run filtering logic tests
python ali_crawler.py --test

# Show help information
python ali_crawler.py --help
```

### First Run
On the first run, the crawler will:
1. Fetch all 131 monthly reports (2014-2025)
2. Filter 453 MySQL/InnoDB focused articles
3. Create a summary markdown file
4. Optionally download individual article contents

### Subsequent Runs
The crawler automatically detects new content and only processes updates, making it perfect for:
- Daily/weekly scheduled runs
- Automated knowledge base maintenance
- Keeping your MySQL documentation current

## 🔍 Content Filtering

The crawler intelligently filters content based on:

**Include**: Articles containing "MySQL" or "InnoDB" keywords
**Exclude**: Articles about PolarDB, MariaDB, MyRocks, RocksDB, TokuDB, HybridDB, X-Engine, or industry news

This ensures your knowledge base stays focused on core MySQL technologies.

## 📊 Statistics

- **Total Monthly Reports**: 131 (from 2014/08 to 2025/06)
- **MySQL Articles Found**: 453
- **Coverage Period**: Over 10 years of MySQL innovations
- **Content Quality**: High-technical depth from Alibaba's MySQL team

## 🛠 Technical Details

- **Language**: Python 3 with standard library only
- **Architecture**: Modular function-based design
- **Error Handling**: Robust with graceful degradation
- **Encoding**: Full UTF-8 support for Chinese content
- **Network**: Efficient with incremental updates

## 📝 Article Format

Each downloaded article includes:
- **Title**: Original article title
- **Metadata**: Publication date and source URL
- **Image Count**: Number of images downloaded for the article
- **Content**: Full article text converted to markdown
- **Local Images**: All images downloaded and referenced with local paths
- **Formatting**: Clean, readable markdown structure with preserved diagrams

## 🔄 Automation Ready

Perfect for automated knowledge base updates:
- Stateless operation (safe for cron jobs)
- Incremental processing (minimal resource usage)
- Error recovery (continues from interruption point)
- No configuration required

## 📚 Use Cases

- **Learning**: Comprehensive MySQL/InnoDB knowledge base
- **Research**: Historical trends in MySQL development
- **Documentation**: Offline access to technical articles
- **Analysis**: Content mining and knowledge extraction

## 🎉 Getting Started

1. Clone this repository
2. Run `python ali_crawler.py` to build your knowledge base
3. Explore the generated markdown files
4. Set up automated runs for continuous updates

Happy knowledge mining! 🚀
