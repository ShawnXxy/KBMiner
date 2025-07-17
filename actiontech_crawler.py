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
    
    # Pattern to match the blog post structure based on observed HTML
    # Looking for posts with title, link, and category information
    
    # Pattern for article titles and URLs
    title_url_pattern = re.compile(
        r'<h2[^>]*>\s*<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>\s*</h2>',
        re.S | re.I
    )
    
    # Find all title-URL pairs
    title_url_matches = title_url_pattern.findall(content)
    
    # Split content into sections to match categories with posts
    # Each post section typically starts with a category and follows with the post
    sections = re.split(r'<h6[^>]*>\s*<a[^>]*href="[^"]*category', content)
    
    current_category = "未分类"  # Default category
    
    for i, section in enumerate(sections):
        if i == 0:
            continue  # Skip the first section (before any category)
            
        # Extract category from this section
        category_match = re.search(r'"[^>]*>(.*?)</a>\s*</h6>', section, re.S | re.I)
        if category_match:
            current_category = category_match.group(1).strip()
            # Clean up category text
            current_category = re.sub(r'<[^>]+>', '', current_category).strip()
        
        # Find blog posts in this section
        section_posts = title_url_pattern.findall(section)
        
        for url, title in section_posts:
            # Clean up title
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            clean_title = clean_title.replace('\n', ' ').replace('\r', '')
            clean_title = re.sub(r'\s+', ' ', clean_title)
            
            # Ensure URL is absolute
            if url.startswith('/'):
                url = 'https://opensource.actionsky.com' + url
            elif not url.startswith('http'):
                url = 'https://opensource.actionsky.com/' + url
            
            if clean_title and url:
                blog_posts.append((clean_title, url, current_category))
    
    # If the section-based approach didn't work well, fall back to simpler approach
    if len(blog_posts) < 5:  # If we got very few results, try alternative
        blog_posts = []
        # Alternative approach: extract all posts and assign default category
        for url, title in title_url_matches:
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            clean_title = clean_title.replace('\n', ' ').replace('\r', '')
            clean_title = re.sub(r'\s+', ' ', clean_title)
            
            if url.startswith('/'):
                url = 'https://opensource.actionsky.com' + url
            elif not url.startswith('http'):
                url = 'https://opensource.actionsky.com/' + url
            
            if clean_title and url:
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
    (no options)        Run crawler to fetch all blog posts
    --test              Run test to fetch first page only
    --help, -h          Show this help message

Features:
    ✓ Fetches all blog posts from ActionTech open source community
    ✓ Extracts post titles, URLs, and categories
    ✓ Handles pagination automatically
    ✓ Groups posts by category in markdown output
    ✓ Provides summary statistics

Output:
    actiontech/
    └── ActionTech技术干货.md      # All blog posts organized by category

Examples:
    python actiontech_crawler.py              # Fetch all blog posts
    python actiontech_crawler.py --test       # Test with first page only
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


def main():
    """Main function to crawl ActionTech blog."""
    base_url = 'https://opensource.actionsky.com/category/技术干货'
    output_dir = 'actiontech'
    output_file = os.path.join(output_dir, 'ActionTech技术干货.md')
    
    print("ActionTech Blog Crawler")
    print("=" * 40)
    
    try:
        # Fetch all posts from all pages
        all_posts = get_all_pages_content(base_url)
        
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
        
        # Write to markdown file
        total_posts, total_categories = write_markdown_file(output_file, unique_posts)
        
        print("\n✓ Successfully crawled ActionTech blog!")
        print(f"  Total articles: {total_posts}")
        print(f"  Categories: {total_categories}")
        print(f"  Output file: {output_file}")
        
        # Show category breakdown
        categories = {}
        for title, url, category in unique_posts:
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
    
    if show_help:
        print_help()
    elif run_test:
        test_single_page()
    else:
        main()
