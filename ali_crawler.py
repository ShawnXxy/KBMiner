# coding: utf-8
import os
import re
import urllib.request


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


if __name__ == "__main__":
    # Uncomment the next line to run tests
    # test_filtering()
    main()