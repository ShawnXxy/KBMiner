# coding: utf-8
import os
import re
import urllib.request
import urllib.parse
import sys


def fetch_page_content(url):
    """Fetch and decode webpage content."""
    # Properly encode the URL to handle Chinese characters
    encoded_url = urllib.parse.quote(url, safe=':/?#[]@!$&\'()*+,;=')
    response = urllib.request.urlopen(encoded_url)
    return response.read().decode('utf-8')


def extract_blog_posts(content):
    """
    Extract blog post information from ActionTech blog page.
    Returns list of tuples: (title, url, category)
    """
    blog_posts = []
    
    # Improved approach: Find all articles with their associated categories
    # Pattern to match the full article structure: category + title + content
    article_pattern = re.compile(
        r'<h6[^>]*class="category[^"]*"[^>]*>\s*<a[^>]*href="[^"]*category[^"]*"[^>]*>(.*?)</a>[^<]*</h6>.*?'
        r'<h2[^>]*>\s*<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>\s*</h2>',
        re.S | re.I
    )
    
    article_matches = article_pattern.findall(content)
    
    for category, url, title in article_matches:
        # Clean up category
        clean_category = re.sub(r'<[^>]+>', '', category).strip()
        clean_category = clean_category.replace('\n', ' ').replace('\r', '')
        clean_category = re.sub(r'\s+', ' ', clean_category)
        
        # Clean up title
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        clean_title = clean_title.replace('\n', ' ').replace('\r', '')
        clean_title = re.sub(r'\s+', ' ', clean_title)
        
        # Ensure URL is absolute
        if url.startswith('/'):
            url = 'https://opensource.actionsky.com' + url
        elif not url.startswith('http'):
            url = 'https://opensource.actionsky.com/' + url
        
        if clean_title and url and should_include_post(clean_title, clean_category, url):
            blog_posts.append((clean_title, url, clean_category))
    
    # If the improved approach didn't find enough results, fall back to simpler approach
    if len(blog_posts) < 3:
        print(f"    Improved extraction found {len(blog_posts)} posts, trying fallback method...")
        
        # Fallback: Pattern for article titles and URLs only
        title_url_pattern = re.compile(
            r'<h2[^>]*>\s*<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>\s*</h2>',
            re.S | re.I
        )
        title_url_matches = title_url_pattern.findall(content)
        
        for url, title in title_url_matches:
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            clean_title = clean_title.replace('\n', ' ').replace('\r', '')
            clean_title = re.sub(r'\s+', ' ', clean_title)
            
            if url.startswith('/'):
                url = 'https://opensource.actionsky.com' + url
            elif not url.startswith('http'):
                url = 'https://opensource.actionsky.com/' + url
            
            if clean_title and url and should_include_post(clean_title, "技术干货", url):
                blog_posts.append((clean_title, url, "技术干货"))
    
    return blog_posts


def get_all_pages_content(base_url):
    """
    Fetch content from all pages of the blog.
    ActionTech blog uses pagination.
    """
    all_posts = []
    page_num = 1
    
    print("Fetching blog posts from all pages...")
    
    while True:
        if page_num == 1:
            current_url = base_url
        else:
            current_url = f"{base_url}/page/{page_num}/"
        
        try:
            print(f"  Fetching page {page_num}...")
            content = fetch_page_content(current_url)
            posts = extract_blog_posts(content)
            
            if not posts:
                print(f"  No posts found on page {page_num}, stopping.")
                break
            
            all_posts.extend(posts)
            print(f"  Found {len(posts)} posts on page {page_num}")
            
            # Check if there's a next page
            # Look for pagination links
            next_page_pattern = re.compile(r'href="[^"]*page/(\d+)/"[^>]*>.*?下一页|next', re.S | re.I)
            if not next_page_pattern.search(content):
                # Also check for numeric pagination
                page_pattern = re.compile(rf'href="[^"]*page/{page_num + 1}/"', re.I)
                if not page_pattern.search(content):
                    print(f"  No next page found after page {page_num}, stopping.")
                    break
            
            page_num += 1
            
            # Safety limit
            if page_num > 200:  # Reasonable limit
                print(f"  Reached page limit ({page_num}), stopping.")
                break
                
        except Exception as e:
            print(f"  Error fetching page {page_num}: {e}")
            break
    
    return all_posts


def write_markdown_file(output_file, posts):
    """Write all blog posts to a markdown file grouped by category."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Group posts by category
    categories = {}
    for title, url, category in posts:
        if category not in categories:
            categories[category] = []
        categories[category].append((title, url))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write main title
        f.write('# ActionTech 开源社区技术干货\n\n')
        f.write(f'**数据抓取时间**: {get_current_datetime()}\n')
        f.write('**来源**: https://opensource.actionsky.com/category/技术干货\n')
        f.write(f'**总文章数**: {len(posts)}\n')
        f.write(f'**分类数**: {len(categories)}\n\n')
        
        # Write table of contents
        f.write('## 目录\n\n')
        for category in sorted(categories.keys()):
            article_count = len(categories[category])
            f.write(f'- [{category}](#{category.replace(" ", "-").lower()}) ({article_count} 篇)\n')
        f.write('\n---\n\n')
        
        # Write each category
        for category in sorted(categories.keys()):
            f.write(f'## {category}\n\n')
            
            # Write articles in this category
            for title, url in categories[category]:
                f.write(f'- [{title}]({url})\n')
            
            f.write('\n')
    
    return len(posts), len(categories)


def get_current_datetime():
    """Get current date and time in readable format."""
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def print_help():
    """Print help information about available commands."""
    help_text = """
ActionTech Blog Crawler - Help

Usage:
    python actiontech_crawler.py [options]

Options:
    (no options)        Run crawler to fetch all blog posts with filtering
    --test              Run test to fetch first page only
    --test-filter       Test category filtering logic
    --help, -h          Show this help message

Features:
    ✓ Fetches all blog posts from ActionTech open source community
    ✓ Extracts post titles, URLs, and categories
    ✓ Handles pagination automatically
    ✓ Groups posts by category in markdown output
    ✓ Smart filtering - excludes ActionDB, ChatDBA, ClickHouse, DTLE, OceanBase
    ✓ Provides summary statistics

Output:
    actiontech/
    └── ActionTech技术干货.md      # All blog posts organized by category (filtered)

Examples:
    python actiontech_crawler.py              # Fetch all blog posts (filtered)
    python actiontech_crawler.py --test       # Test with first page only
    python actiontech_crawler.py --test-filter # Test filtering logic
    """
    print(help_text)


def test_single_page():
    """Test function to crawl only the first page."""
    base_url = 'https://opensource.actionsky.com/category/技术干货'
    output_dir = 'actiontech'
    output_file = os.path.join(output_dir, 'ActionTech技术干货_测试.md')
    
    print("Testing single page crawl...")
    
    try:
        content = fetch_page_content(base_url)
        posts = extract_blog_posts(content)
        
        print(f"Found {len(posts)} posts on first page")
        
        # Display first few posts for verification
        if posts:
            print("\nSample posts:")
            for i, (title, url, category) in enumerate(posts[:5]):
                print(f"  {i+1}. [{category}] {title}")
                print(f"     URL: {url}\n")
        
        # Write to test file
        total_posts, total_categories = write_markdown_file(output_file, posts)
        print(f"✓ Test completed. Saved {total_posts} posts in {total_categories} categories")
        print(f"  Output: {output_file}")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")


def test_filtering():
    """Test the category and title filtering logic with sample data."""
    
    # Test category filtering
    category_test_cases = [
        ("ActionDB", False),            # Should be excluded
        ("ChatDBA", False),             # Should be excluded
        ("ClickHouse", False),          # Should be excluded
        ("ClickHouse 系列", False),      # Should be excluded
        ("DTLE", False),                # Should be excluded
        ("DTLE 数据传输组件", False),     # Should be excluded
        ("OceanBase", False),           # Should be excluded
        ("技术分享", True),             # Should be included
        ("故障分析", True),             # Should be included
        ("MySQL 新特性", True),         # Should be included
        ("技术干货", True),             # Should be included
        ("MySQL 核心模块揭秘", True),    # Should be included
    ]
    
    print("Testing category filtering logic:")
    for category, expected in category_test_cases:
        result = should_include_category(category)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{category}' -> {result} (expected: {expected})")
    
    # Test title filtering
    title_test_cases = [
        ("MySQL优化技术分析", True),                              # Should be included
        ("MariaDB 性能对比研究", False),                         # Should be excluded
        ("ScaleFlux 存储技术介绍", False),                        # Should be excluded
        ("TiDB 分布式数据库架构", False),                        # Should be excluded
        ("MySQL 与 MariaDB 对比分析", False),                   # Should be excluded (contains MariaDB)
        ("InnoDB 存储引擎详解", True),                          # Should be included
        ("数据库故障分析", True),                               # Should be included
        ("tidb 集群部署实践", False),                           # Should be excluded (case insensitive)
    ]
    
    print("\nTesting title filtering logic:")
    for title, expected in title_test_cases:
        result = should_include_title(title)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{title}' -> {result} (expected: {expected})")
    
    # Test combined filtering
    combined_test_cases = [
        ("MySQL优化技术", "技术分享", "https://opensource.actionsky.com/123", True),                     # Should be included
        ("MariaDB 性能分析", "技术分享", "https://opensource.actionsky.com/456", False),                # Should be excluded (title)
        ("MySQL 新特性", "ChatDBA", "https://opensource.actionsky.com/789", False),                    # Should be excluded (category)
        ("TiDB 架构设计", "ActionDB", "https://opensource.actionsky.com/012", False),                  # Should be excluded (both)
        ("MySQL核心模块详解", "MySQL核心模块揭秘", "https://opensource.actionsky.com/category/技术专栏/揭秘/345", True),  # Should be included (hard filter)
        ("MariaDB核心分析", "其他分类", "https://opensource.actionsky.com/category/技术专栏/揭秘/678", True),  # Should be included (hard filter overrides title filter)
    ]
    
    print("\nTesting combined filtering logic:")
    for title, category, url, expected in combined_test_cases:
        result = should_include_post(title, category, url)
        status = "✓" if result == expected else "✗"
        reason = "title" if not should_include_title(title) else "category" if not should_include_category(category) else "both" if not should_include_title(title) and not should_include_category(category) else "hard filter" if "技术专栏/揭秘" in url else "unknown"
        print(f"{status} '{title}' [{category}] -> {result} (expected: {expected})")
        if result != expected:
            print(f"    Reason: {reason} filter")


def should_include_category(category):
    """
    Determine if a blog post should be included based on category filtering rules.
    
    Rules:
    - Exclude categories: "ActionDB", "ChatDBA", "ClickHouse", "DTLE", "OceanBase"
    - Include all other categories
    """
    # Convert to lowercase for case-insensitive comparison
    category_lower = category.lower()
    
    # List of categories to exclude
    excluded_categories = [
        'actiondb',
        'chatdba',
        'clickhouse',
        'clickhouse 系列',
        'dtle',
        'dtle 数据传输组件',
        'oceanbase'
    ]
    
    # Check if category should be excluded
    for excluded in excluded_categories:
        if excluded in category_lower:
            return False
    
    return True


def should_include_title(title):
    """
    Determine if a blog post should be included based on title filtering rules.
    
    Rules:
    - Exclude titles containing: "MariaDB", "ScaleFlux", "TiDB"
    - Case-insensitive matching
    """
    # Convert to lowercase for case-insensitive comparison
    title_lower = title.lower()
    
    # List of keywords to exclude from titles
    excluded_keywords = [
        'mariadb',
        'scaleflux',
        'tidb'
    ]
    
    # Check if title contains any excluded keywords
    for keyword in excluded_keywords:
        if keyword in title_lower:
            return False
    
    return True


def should_include_post(title, category, url=None):
    """
    Determine if a blog post should be included based on title, category, and URL filtering.
    
    Rules:
    - Must pass both title and category filters
    - Hard filter: Always include blogs from "MySQL核心模块揭秘" category (URL contains "技术专栏/揭秘")
    """
    # Hard filter: Always include MySQL core module articles
    if url and "技术专栏/揭秘" in url:
        print(f"  Hard filter: Including MySQL核心模块揭秘 article: {title}")
        return True
    
    return should_include_title(title) and should_include_category(category)


def main():
    """Main function to crawl ActionTech blog."""
    base_urls = [
        'https://opensource.actionsky.com/category/技术干货',
        'https://opensource.actionsky.com/category/技术专栏/揭秘'  # MySQL核心模块揭秘 category
    ]
    output_dir = 'actiontech'
    output_file = os.path.join(output_dir, 'ActionTech技术干货.md')
    
    print("ActionTech Blog Crawler")
    print("=" * 40)
    
    try:
        all_posts = []
        
        # Fetch all posts from all URLs
        for base_url in base_urls:
            print(f"\nFetching from: {base_url}")
            posts = get_all_pages_content(base_url)
            all_posts.extend(posts)
            print(f"Found {len(posts)} posts from this URL")
        
        if not all_posts:
            print("No blog posts found!")
            return
        
        print(f"\nTotal posts found: {len(all_posts)}")
        
        # Remove duplicates (in case of overlapping pages)
        unique_posts = []
        seen_urls = set()
        for title, url, category in all_posts:
            if url not in seen_urls:
                unique_posts.append((title, url, category))
                seen_urls.add(url)
        
        print(f"Unique posts after deduplication: {len(unique_posts)}")
        all_posts = unique_posts
        
        # Filter out excluded categories
        # Apply filtering and track statistics
        filtered_posts = []
        excluded_count = 0
        
        for title, url, category in all_posts:
            if should_include_post(title, category, url):
                filtered_posts.append((title, url, category))
            else:
                excluded_count += 1
                print(f"  Excluded [{category}]: {title}")
        
        all_posts = filtered_posts
        
        print(f"\nTotal posts found: {len(all_posts) + excluded_count}")
        print(f"Posts excluded by filtering: {excluded_count}")
        print(f"Posts after category filtering: {len(filtered_posts)}")
        
        # Write to markdown file
        total_posts, total_categories = write_markdown_file(output_file, filtered_posts)
        
        print("\n✓ Successfully crawled ActionTech blog!")
        print(f"  Total articles: {total_posts}")
        print(f"  Excluded articles: {excluded_count}")
        print(f"  Categories: {total_categories}")
        print(f"  Output file: {output_file}")
        
        if excluded_count > 0:
            print("\n🚫 Filtering Summary:")
            print(f"  Excluded {excluded_count} articles from unwanted categories")
            print("  Excluded categories: ActionDB, ChatDBA, ClickHouse, DTLE, OceanBase")
        
        # Show category breakdown
        categories = {}
        for title, url, category in filtered_posts:
            categories[category] = categories.get(category, 0) + 1
        
        print("\nCategory breakdown:")
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} 篇")
        
    except Exception as e:
        print(f"✗ Error during crawling: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check command line arguments
    show_help = '--help' in sys.argv or '-h' in sys.argv
    run_test = '--test' in sys.argv
    test_filter = '--test-filter' in sys.argv
    
    if show_help:
        print_help()
    elif test_filter:
        test_filtering()
    elif run_test:
        test_single_page()
    else:
        main()
