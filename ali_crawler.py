# coding: utf-8
import os
import re
import urllib.request
import sys


def fetch_page_content(url):
    """Fetch and decode webpage content."""
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def extract_topic(content):
    """Extract webpage title from content."""
    re_topic = re.compile(r'<!-- <title>(.*?)</title> -->', re.S)
    return re.findall(re_topic, content)[0]


def extract_month_links(content):
    """Extract monthly report links from main page content."""
    re_month_blog_address = re.compile(r'<a target="_top" class="main" href="/monthly/(.*?)">', re.S)
    return re.findall(re_month_blog_address, content)


def should_include_article(title):
    """
    Determine if an article should be included based on title filtering rules.
    
    Rules:
    - Include if title contains "MySQL" or "InnoDB" (case-insensitive)
    - Exclude if title contains "PolarDB", "PlarDB", "MariaDB", "HybridDB", "RocksDB", "TokuDB", "MyRocks", "X-Engine", or "行业动态", "行业洞察", "社区见闻"
      (case-insensitive), even if it has MySQL/InnoDB
    """
    title_lower = title.lower()
    
    # First check exclusion keywords - if found, exclude regardless of MySQL/InnoDB presence
    exclusion_keywords = ['polardb', 'plardb', 'mariadb', 'tokudb', 'myrocks', 'rocksdb', 'hybriddb', 'x-engine', '行业动态', '行业洞察', '社区见闻']
    for keyword in exclusion_keywords:
        if keyword in title_lower:
            return False
    
    # Check if it contains MySQL or InnoDB
    return 'mysql' in title_lower or 'innodb' in title_lower


def extract_article_links(content):
    """Extract article titles and links from monthly page content."""
    re_article_title_link = re.compile(r'class="main" href="/monthly/(.*?)">(.*?)</a></h3></li>', re.S)
    all_articles = re.findall(re_article_title_link, content)
    
    # Filter articles based on the inclusion criteria
    return [(link, title) for link, title in all_articles if should_include_article(title)]


def write_markdown_file(output_file, topic, base_url, month_links):
    """Write all content to markdown file with MySQL/InnoDB filtering."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    total_articles = 0
    filtered_articles = 0
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write main title
        f.write(f'## {topic} (MySQL/InnoDB Focus)\n\n')
        
        # Process each monthly report
        for month in month_links:
            # Fetch monthly page content
            month_url = base_url + month
            month_content = fetch_page_content(month_url)
            all_article_links = extract_article_links(month_content)
            
            total_articles += len(all_article_links)
            
            # Filter articles based on title
            filtered_article_links = [
                (link, title) for link, title in all_article_links
                if should_include_article(title)
            ]
            
            filtered_articles += len(filtered_article_links)
            
            # Only write month section if there are filtered articles
            if filtered_article_links:
                f.write(f'### {month}\n')
                f.write('---\n\n')
                
                # Write each article as a bullet point on its own line
                for article_link, article_title in filtered_article_links:
                    full_link = base_url + article_link
                    f.write(f'- [{article_title}]({full_link})\n')
                
                f.write('\n')
    
    return total_articles, filtered_articles


def load_existing_months(output_dir):
    """Load existing months from a tracking file to avoid reprocessing."""
    tracking_file = os.path.join(output_dir, '.processed_months.txt')
    
    if not os.path.exists(tracking_file):
        return set()
    
    existing_months = set()
    try:
        with open(tracking_file, 'r', encoding='utf-8') as f:
            existing_months = set(line.strip() for line in f if line.strip())
    except Exception as e:
        print(f"Warning: Could not read tracking file {tracking_file}: {e}")
    
    return existing_months


def save_processed_month(output_dir, month):
    """Save a processed month to the tracking file."""
    tracking_file = os.path.join(output_dir, '.processed_months.txt')
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(tracking_file, 'a', encoding='utf-8') as f:
            f.write(f"{month}\n")
    except Exception as e:
        print(f"Warning: Could not save to tracking file {tracking_file}: {e}")


def append_new_months_to_file(output_file, topic, base_url, output_dir, new_month_links):
    """Append only new months to the existing markdown file."""
    total_articles = 0
    filtered_articles = 0
    
    # If file doesn't exist, create it with header
    if not os.path.exists(output_file):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'## {topic} (MySQL/InnoDB Focus)\n\n')
    
    # Append new months
    with open(output_file, 'a', encoding='utf-8') as f:
        for month in new_month_links:
            # Fetch monthly page content
            month_url = base_url + month
            try:
                month_content = fetch_page_content(month_url)
                all_article_links = extract_article_links(month_content)
                
                total_articles += len(all_article_links)
                
                # Filter articles based on title
                filtered_article_links = [
                    (link, title) for link, title in all_article_links
                    if should_include_article(title)
                ]
                
                filtered_articles += len(filtered_article_links)
                
                # Write month section if there are filtered articles
                if filtered_article_links:
                    f.write(f'### {month}\n')
                    f.write('---\n\n')
                    
                    # Write each article as a bullet point on its own line
                    for article_link, article_title in filtered_article_links:
                        full_link = base_url + article_link
                        f.write(f'- [{article_title}]({full_link})\n')
                    
                    f.write('\n')
                
                # Always log that we processed this month and save to tracking
                print(f"  Processed {month}: {len(filtered_article_links)} MySQL/InnoDB articles")
                save_processed_month(output_dir, month)
                
            except Exception as e:
                print(f"  Warning: Could not process {month}: {e}")
    
    return total_articles, filtered_articles


def sanitize_filename(filename):
    """Sanitize filename by removing invalid characters and limiting length."""
    # Remove or replace invalid characters for Windows filesystem
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Replace multiple spaces with single space and strip
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    # Limit filename length (Windows has 255 char limit, leave room for extension and path)
    if len(filename) > 100:
        filename = filename[:100].rsplit(' ', 1)[0]  # Cut at word boundary
    
    return filename


def extract_article_content(url):
    """Extract the main content from an article page."""
    try:
        content = fetch_page_content(url)
        
        # Extract the main article content using regex patterns
        # This matches the typical structure of Alibaba's monthly reports
        
        # First try to get content between <div class="post-content"> and </div>
        content_pattern = re.compile(r'<div class="post-content">(.*?)</div>\s*<div class="post-footer">', re.S)
        content_match = re.search(content_pattern, content)
        
        if content_match:
            article_html = content_match.group(1)
        else:
            # Fallback pattern - look for content between common markers
            content_pattern = re.compile(r'<div class="content">(.*?)<div class="footer">', re.S)
            content_match = re.search(content_pattern, content)
            if content_match:
                article_html = content_match.group(1)
            else:
                # Last resort - get content between body tags
                body_pattern = re.compile(r'<body[^>]*>(.*?)</body>', re.S)
                body_match = re.search(body_pattern, content)
                if body_match:
                    article_html = body_match.group(1)
                else:
                    return "Could not extract article content."
        
        # Convert HTML to markdown-like format
        article_content = html_to_markdown(article_html)
        
        return article_content
        
    except Exception as e:
        return f"Error fetching article content: {e}"


def html_to_markdown(html_content):
    """Convert HTML content to markdown format."""
    # Clean up the HTML content
    content = html_content
    
    # Remove script and style tags
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.S | re.I)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.S | re.I)
    
    # Convert headers
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content, flags=re.S | re.I)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content, flags=re.S | re.I)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content, flags=re.S | re.I)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', content, flags=re.S | re.I)
    content = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1', content, flags=re.S | re.I)
    content = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1', content, flags=re.S | re.I)
    
    # Convert paragraphs
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.S | re.I)
    
    # Convert line breaks
    content = re.sub(r'<br[^>]*/?>', '\n', content, flags=re.I)
    
    # Convert bold and italic
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.S | re.I)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.S | re.I)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.S | re.I)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.S | re.I)
    
    # Convert code blocks and inline code
    content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```\n', content, flags=re.S | re.I)
    content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.S | re.I)
    content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```\n', content, flags=re.S | re.I)
    
    # Convert lists
    content = re.sub(r'<ul[^>]*>(.*?)</ul>', lambda m: convert_list(m.group(1), '*'), content, flags=re.S | re.I)
    content = re.sub(r'<ol[^>]*>(.*?)</ol>', lambda m: convert_list(m.group(1), '1.'), content, flags=re.S | re.I)
    
    # Convert links
    content = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.S | re.I)
    
    # Convert images
    content = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)', content, flags=re.I)
    content = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*/?>', r'![](\1)', content, flags=re.I)
    
    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Multiple newlines to double newlines
    content = re.sub(r'[ \t]+', ' ', content)  # Multiple spaces to single space
    
    # Decode HTML entities
    content = content.replace('&nbsp;', ' ')
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('&amp;', '&')
    content = content.replace('&quot;', '"')
    content = content.replace('&#39;', "'")
    
    return content.strip()


def convert_list(list_content, marker):
    """Convert HTML list items to markdown."""
    items = re.findall(r'<li[^>]*>(.*?)</li>', list_content, flags=re.S | re.I)
    result = []
    for i, item in enumerate(items):
        item = re.sub(r'<[^>]+>', '', item).strip()  # Remove HTML tags
        if marker == '1.':
            result.append(f"{i+1}. {item}")
        else:
            result.append(f"{marker} {item}")
    return '\n'.join(result) + '\n\n'


def save_individual_articles(base_url, month_links, output_dir):
    """Download and save individual articles as separate markdown files."""
    articles_dir = os.path.join(output_dir, 'articles')
    os.makedirs(articles_dir, exist_ok=True)
    
    total_saved = 0
    
    for month in month_links:
        print(f"Processing articles for {month}...")
        
        # Fetch monthly page content
        month_url = base_url + month
        try:
            month_content = fetch_page_content(month_url)
            filtered_articles = extract_article_links(month_content)
            
            for article_link, article_title in filtered_articles:
                # Generate filename: month + title
                safe_title = sanitize_filename(article_title)
                filename = f"{month.replace('/', '-')}_{safe_title}.md"
                filepath = os.path.join(articles_dir, filename)
                
                # Skip if file already exists
                if os.path.exists(filepath):
                    print(f"  Skipping {filename} (already exists)")
                    continue
                
                # Fetch article content
                full_article_url = base_url + article_link
                print(f"  Downloading: {article_title}")
                
                article_content = extract_article_content(full_article_url)
                
                # Create markdown file with metadata
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {article_title}\n\n")
                    f.write(f"**Date:** {month}\n")
                    f.write(f"**Source:** {full_article_url}\n\n")
                    f.write("---\n\n")
                    f.write(article_content)
                
                total_saved += 1
                print(f"  ✓ Saved: {filename}")
                
        except Exception as e:
            print(f"  Error processing {month}: {e}")
    
    return total_saved


# Test function to verify filtering logic
def test_filtering():
    """Test the filtering logic with sample titles."""
    test_cases = [
        ("MySQL PolarDB 性能优化", False),  # Should be excluded
        ("InnoDB PlarDB 特性介绍", False),   # Should be excluded
        ("MySQL MariaDB 对比分析", False),   # Should be excluded
        ("TokuDB 存储引擎分析", False),      # Should be excluded
        ("MyRocks 与 InnoDB 比较", False),  # Should be excluded
        ("RocksDB 底层实现", False),        # Should be excluded
        ("HybridDB 架构设计", False),       # Should be excluded
        ("X-Engine 新特性", False),         # Should be excluded
        ("数据库行业动态分析", False),        # Should be excluded
        ("MySQL 行业洞察报告", False),       # Should be excluded
        ("InnoDB 社区见闻", False),         # Should be excluded
        ("MySQL 优化器分析", True),         # Should be included
        ("InnoDB 锁机制详解", True),        # Should be included
        ("普通文章标题", False),            # Should be excluded (no MySQL/InnoDB)
    ]
    
    print("Testing filtering logic:")
    for title, expected in test_cases:
        result = should_include_article(title)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{title}' -> {result} (expected: {expected})")


def print_help():
    """Print help information about available commands."""
    help_text = """
MySQL Knowledge Base Crawler - Help

Usage:
    python ali_crawler.py [options]

Options:
    (no options)        Run normal crawler to update monthly report summary
    --download-articles Download ALL individual articles (may take a long time)
    --test-articles     Download a few sample articles for testing
    --test              Run filtering logic tests

Features:
    ✓ Incremental updates - only processes new months
    ✓ MySQL/InnoDB content filtering with keyword exclusions
    ✓ Individual article download with full content
    ✓ Automatic file naming: {month}_{title}.md
    ✓ Progress tracking and error handling

Output Structure:
    ali_monthly/
    ├── 阿里数据库内核月报.md          # Summary with all article links
    ├── .processed_months.txt          # Tracking file for incremental updates
    └── articles/                      # Individual article contents
        ├── 2025-05_MySQL无锁哈希表LF_HASH.md
        ├── 2024-12_MySQL优化器代码速览.md
        └── ...

Examples:
    python ali_crawler.py                  # Update summary only
    python ali_crawler.py --test-articles  # Download a few test articles
    python ali_crawler.py --download-articles  # Download all articles (453 files)
    """
    print(help_text)


def main():
    """Main function to crawl Alibaba MySQL monthly reports with incremental updates."""
    base_url = 'http://mysql.taobao.org/monthly/'
    output_dir = 'ali_monthly'
    output_file = os.path.join(output_dir, '阿里数据库内核月报.md')
    
    # Fetch main page and extract data
    main_content = fetch_page_content(base_url)
    topic = extract_topic(main_content)
    all_month_links = extract_month_links(main_content)
    
    # Load existing months to avoid reprocessing
    existing_months = load_existing_months(output_dir)
    print(f"Found {len(existing_months)} existing months in tracking file")
    if existing_months:
        print(f"Existing months (first 5): {', '.join(list(existing_months)[:5])}")
    
    new_month_links = [month for month in all_month_links if month not in existing_months]
    
    if not new_month_links:
        print(f"No new monthly reports found. All {len(all_month_links)} reports are already processed.")
        print(f"Existing file: {output_file}")
        
        # Ask if user wants to download individual articles
        print("\nWould you like to download individual article contents?")
        print("This will create separate markdown files for each article.")
        download_articles = input("Download articles? (y/n): ").lower().strip()
        
        if download_articles == 'y':
            print("Starting individual article download...")
            saved_count = save_individual_articles(base_url, all_month_links, output_dir)
            print(f"✓ Successfully saved {saved_count} individual articles")
        
        return
    
    print(f"Found {len(new_month_links)} new monthly reports out of {len(all_month_links)} total")
    print(f"New months to process: {', '.join(new_month_links[:5])}{'...' if len(new_month_links) > 5 else ''}")
    
    # Process only new months
    total_articles, filtered_articles = append_new_months_to_file(output_file, topic, base_url, output_dir, new_month_links)
    
    print(f"Successfully processed {len(new_month_links)} new monthly reports")
    print(f"New articles found: {total_articles}")
    print(f"New MySQL/InnoDB focused articles: {filtered_articles}")
    print(f"New articles excluded: {total_articles - filtered_articles}")
    if total_articles > 0:
        print(f"Filtering efficiency: {(total_articles - filtered_articles) / total_articles * 100:.1f}% excluded")
    print(f"Output updated: {output_file}")
    
    # Ask if user wants to download individual articles for new months
    if filtered_articles > 0:
        print(f"\nWould you like to download individual article contents for the {len(new_month_links)} new months?")
        download_articles = input("Download articles? (y/n): ").lower().strip()
        
        if download_articles == 'y':
            print("Starting individual article download for new months...")
            saved_count = save_individual_articles(base_url, new_month_links, output_dir)
            print(f"✓ Successfully saved {saved_count} individual articles")


def main_test_articles():
    """Test function to download a few articles for testing."""
    base_url = 'http://mysql.taobao.org/monthly/'
    output_dir = 'ali_monthly'
    
    # Test with just a few recent months
    test_months = ['2025/05', '2024/12']
    
    print("Testing article download with recent months...")
    saved_count = save_individual_articles(base_url, test_months, output_dir)
    print(f"✓ Test completed. Saved {saved_count} individual articles")


if __name__ == "__main__":
    # Check command line arguments
    download_all_articles = '--download-articles' in sys.argv
    test_articles = '--test-articles' in sys.argv
    run_tests = '--test' in sys.argv
    
    if run_tests:
        test_filtering()
    elif test_articles:
        main_test_articles()
    elif download_all_articles:
        # Direct download mode - download all articles without prompting
        print("Direct download mode: Downloading all individual articles...")
        base_url = 'http://mysql.taobao.org/monthly/'
        output_dir = 'ali_monthly'
        
        main_content = fetch_page_content(base_url)
        all_month_links = extract_month_links(main_content)
        
        saved_count = save_individual_articles(base_url, all_month_links, output_dir)
        print(f"✓ Successfully saved {saved_count} individual articles")
    else:
        print_help()