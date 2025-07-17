# coding: utf-8
import os
import re
import urllib.request
import urllib.parse
import sys
import json
import datetime
from urllib.parse import urlparse, urljoin
import hashlib


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


def write_markdown_file(output_file, new_posts, existing_posts=None, incremental=False):
    """Write blog posts to a markdown file grouped by category."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Combine new and existing posts if incremental
    all_posts = new_posts[:]
    if incremental and existing_posts:
        # Add existing posts that are not in new_posts
        new_urls = {url for _, url, _ in new_posts}
        for url, title in existing_posts.items():
            if url not in new_urls:
                # Try to extract category from URL or use default
                category = extract_category_from_url(url)
                all_posts.append((title, url, category))
    
    # Group posts by category
    categories = {}
    for title, url, category in all_posts:
        if category not in categories:
            categories[category] = []
        categories[category].append((title, url))
    
    # Sort articles within each category by title
    for category in categories:
        categories[category].sort(key=lambda x: x[0])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write main title
        f.write('# ActionTech 开源社区技术干货\n\n')
        f.write(f'**数据抓取时间**: {get_current_datetime()}\n')
        f.write('**来源**: https://opensource.actionsky.com/category/技术干货\n')
        f.write(f'**总文章数**: {len(all_posts)}\n')
        f.write(f'**分类数**: {len(categories)}\n')
        
        if incremental and new_posts:
            f.write(f'**新增文章数**: {len(new_posts)}\n')
        
        f.write('\n')
        
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
    
    return len(all_posts), len(categories)


def extract_category_from_url(url):
    """Extract category from URL or return default category."""
    if "技术专栏/揭秘" in url:
        return "MySQL 核心模块揭秘"
    elif "技术专栏/mysql-picture" in url:
        return "图解 MySQL"
    elif "mysql" in url.lower():
        return "MySQL 新特性"
    else:
        return "技术干货"


def get_current_datetime():
    """Get current date and time in readable format."""
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def load_crawl_state(state_file):
    """Load the previous crawl state from file."""
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                return state.get('crawled_urls', set()), state.get('last_crawl_time', '')
        except Exception as e:
            print(f"Warning: Could not load crawl state: {e}")
    return set(), ''


def save_crawl_state(state_file, crawled_urls, crawl_time):
    """Save the current crawl state to file."""
    try:
        state = {
            'crawled_urls': list(crawled_urls),
            'last_crawl_time': crawl_time,
            'total_articles': len(crawled_urls)
        }
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save crawl state: {e}")


def load_existing_posts(output_file):
    """Load existing posts from the markdown file to avoid duplicates."""
    existing_posts = {}
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract URLs from markdown links, but exclude table of contents (anchor links)
                url_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
                for title, url in url_pattern.findall(content):
                    # Skip anchor links (table of contents)
                    if not url.startswith('#') and url.startswith('http'):
                        existing_posts[url] = title.strip()
        except Exception as e:
            print(f"Warning: Could not load existing posts: {e}")
    return existing_posts


def download_image(img_url, img_dir, base_url):
    """Download an image and return the local path."""
    try:
        # Make image URL absolute
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            img_url = urljoin(base_url, img_url)
        elif not img_url.startswith('http'):
            img_url = urljoin(base_url, img_url)
        
        # Create a hash-based filename to avoid conflicts
        url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
        parsed_url = urlparse(img_url)
        
        # Try to get file extension from URL
        path = parsed_url.path
        if '.' in path:
            ext = path.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                filename = f"{url_hash}.{ext}"
            else:
                filename = f"{url_hash}.jpg"  # Default to jpg
        else:
            filename = f"{url_hash}.jpg"
        
        local_path = os.path.join(img_dir, filename)
        
        # Skip if already downloaded
        if os.path.exists(local_path):
            return filename
        
        # Download the image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        request = urllib.request.Request(img_url, headers=headers)
        
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.read())
                print(f"    Downloaded image: {filename}")
                return filename
            else:
                print(f"    Failed to download image: {img_url} (Status: {response.status})")
                return None
                
    except Exception as e:
        print(f"    Error downloading image {img_url}: {e}")
        return None


def extract_article_content(url):
    """Extract the main article content from single-post-wrap entry-content class."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read().decode('utf-8')
        
        # First try to find the more specific single-post-wrap entry-content class
        specific_pattern = r'<div[^>]*class="[^"]*single-post-wrap[^"]*entry-content[^"]*"[^>]*>(.*?)</div>'
        match = re.search(specific_pattern, content, re.S | re.I)
        
        if not match:
            # Fallback to original entry-content pattern
            entry_content_pattern = r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>'
            match = re.search(entry_content_pattern, content, re.S | re.I)
        
        if not match:
            # Additional fallback patterns for more robust extraction
            fallback_patterns = [
                r'<div[^>]*class="[^"]*post-content[^"]*"[^>]*>(.*?)</div>',
                r'<div[^>]*class="[^"]*article-content[^"]*"[^>]*>(.*?)</div>',
                r'<article[^>]*>(.*?)</article>',
                r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>'
            ]
            
            for pattern in fallback_patterns:
                match = re.search(pattern, content, re.S | re.I)
                if match:
                    print(f"    Using fallback pattern for content extraction in {url}")
                    break
        
        if not match:
            print(f"    Warning: Could not find any content div in {url}")
            return None, None, None
        
        article_content = match.group(1)
        
        # Validate that we have actual content (not just empty tags)
        text_content = re.sub(r'<[^>]+>', '', article_content).strip()
        if len(text_content) < 50:  # Minimum content length check
            print(f"    Warning: Extracted content too short ({len(text_content)} chars) from {url}")
            return None, None, None
        
        # Extract title from h1 tag
        title_match = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', content, re.S | re.I)
        if not title_match:
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.S | re.I)
        
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        else:
            # Fallback to title tag
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.S | re.I)
            if title_match:
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                # Clean up title (remove site name if present)
                title = re.sub(r'\s*[-–|]\s*.*?ActionTech.*$', '', title, flags=re.I).strip()
            else:
                title = "Untitled Article"
        
        # Extract publish date
        date_patterns = [
            r'<time[^>]*datetime="([^"]+)"',
            r'<meta[^>]*property="article:published_time"[^>]*content="([^"]+)"',
            r'<span[^>]*class="[^"]*date[^"]*"[^>]*>([^<]+)</span>'
        ]
        
        publish_date = None
        for pattern in date_patterns:
            match = re.search(pattern, content, re.I)
            if match:
                publish_date = match.group(1).strip()
                break
        
        return title, article_content, publish_date
        
    except Exception as e:
        print(f"    Error extracting content from {url}: {e}")
        return None, None, None


def clean_html_content(html_content, base_url, img_dir):
    """Clean HTML content and convert to markdown-friendly format with proper image handling."""
    if not html_content:
        return ""
    
    # Ensure img_dir exists
    os.makedirs(img_dir, exist_ok=True)
    
    # Download images and update references
    img_pattern = re.compile(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', re.I)
    
    def replace_image(match):
        img_tag = match.group(0)
        img_url = match.group(1)
        
        # Download image
        local_filename = download_image(img_url, img_dir, base_url)
        if local_filename:
            # Create relative path for markdown (from articles folder to .img folder)
            relative_path = f".img/{local_filename}"
            
            # Extract alt text if available
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag, re.I)
            alt_text = alt_match.group(1) if alt_match else "Image"
            
            return f"![{alt_text}]({relative_path})"
        else:
            # Fallback: keep original URL but in markdown format
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag, re.I)
            alt_text = alt_match.group(1) if alt_match else "Image"
            return f"![{alt_text}]({img_url})"
    
    # Replace images first
    html_content = img_pattern.sub(replace_image, html_content)
    
    # Convert HTML to markdown
    # Headers - be more specific with patterns
    for i in range(1, 7):
        html_content = re.sub(
            rf'<h{i}[^>]*>(.*?)</h{i}>',
            lambda m: '#' * i + ' ' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '\n\n',
            html_content,
            flags=re.S | re.I
        )
    
    # Paragraphs
    html_content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html_content, flags=re.S | re.I)
    
    # Links
    html_content = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html_content, flags=re.S | re.I)
    
    # Code blocks (preserve code structure)
    html_content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```\n\n', html_content, flags=re.S | re.I)
    html_content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html_content, flags=re.S | re.I)
    
    # Lists
    html_content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html_content, flags=re.S | re.I)
    html_content = re.sub(r'<[uo]l[^>]*>(.*?)</[uo]l>', r'\1\n', html_content, flags=re.S | re.I)
    
    # Bold and italic
    html_content = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', html_content, flags=re.S | re.I)
    html_content = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', html_content, flags=re.S | re.I)
    
    # Tables (basic conversion)
    html_content = re.sub(r'<table[^>]*>(.*?)</table>', lambda m: convert_table_to_markdown(m.group(1)), html_content, flags=re.S | re.I)
    
    # Blockquotes
    html_content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n\n', html_content, flags=re.S | re.I)
    
    # Line breaks
    html_content = re.sub(r'<br[^>]*/?>', '\n', html_content, flags=re.I)
    
    # Remove remaining HTML tags
    html_content = re.sub(r'<[^>]+>', '', html_content)
    
    # Clean up whitespace
    html_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', html_content)
    html_content = re.sub(r'^\s+', '', html_content, flags=re.M)
    
    # Decode HTML entities
    html_entities = {
        '&nbsp;': ' ',
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&#39;': "'",
        '&ldquo;': '"',
        '&rdquo;': '"',
        '&lsquo;': "'",
        '&rsquo;': "'",
        '&mdash;': '—',
        '&ndash;': '–'
    }
    
    for entity, char in html_entities.items():
        html_content = html_content.replace(entity, char)
    
    return html_content.strip()


def convert_table_to_markdown(table_html):
    """Convert HTML table to markdown format."""
    try:
        # Extract table rows
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.S | re.I)
        if not rows:
            return ""
        
        markdown_rows = []
        for i, row in enumerate(rows):
            # Extract cells (th or td)
            cells = re.findall(r'<(th|td)[^>]*>(.*?)</\1>', row, re.S | re.I)
            if cells:
                cell_contents = [re.sub(r'<[^>]+>', '', cell[1]).strip() for cell in cells]
                markdown_row = '| ' + ' | '.join(cell_contents) + ' |'
                markdown_rows.append(markdown_row)
                
                # Add header separator after first row
                if i == 0:
                    separator = '| ' + ' | '.join(['---'] * len(cell_contents)) + ' |'
                    markdown_rows.append(separator)
        
        return '\n' + '\n'.join(markdown_rows) + '\n\n'
    except Exception as e:
        print(f"    Error converting table to markdown: {e}")
        return ""


def save_article_content(title, url, content, publish_date, articles_dir, category):
    """Save article content to a markdown file with proper naming."""
    try:
        # Create a safe filename
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        safe_title = re.sub(r'[^\w\s-]', '', safe_title)
        safe_title = safe_title.strip()[:80]  # Limit length
        
        # Simple filename format: title.md
        filename = f"{safe_title}.md"
        filepath = os.path.join(articles_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"    ✓ Article already exists, skipping: {filename}")
            return filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            
            f.write(f"**原文链接**: {url}\n")
            f.write(f"**分类**: {category}\n")
            if publish_date:
                f.write(f"**发布时间**: {publish_date}\n")
            f.write("\n---\n\n")
            f.write(content)
        
        print(f"    ✓ Saved new article: {filename}")
        return filename
        
    except Exception as e:
        print(f"    ✗ Error saving article {title}: {e}")
        return None


def generate_individual_articles(posts, base_dir):
    """Generate individual markdown files for each blog post."""
    articles_dir = os.path.join(base_dir, 'articles')
    img_dir = os.path.join(articles_dir, '.img')
    
    # Create directories
    os.makedirs(articles_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    
    print("\n� Generating individual article files...")
    print(f"  Articles directory: {articles_dir}")
    print(f"  Images directory: {img_dir}")
    
    successful_downloads = 0
    failed_downloads = 0
    skipped_existing = 0
    
    for i, (title, url, category) in enumerate(posts, 1):
        print(f"\n📄 [{i}/{len(posts)}] Processing: {title}")
        
        try:
            # Check if file already exists
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = re.sub(r'[^\w\s-]', '', safe_title)
            safe_title = safe_title.strip()[:80]
            filename = f"{safe_title}.md"
            filepath = os.path.join(articles_dir, filename)
            
            if os.path.exists(filepath):
                print(f"    ✓ Already exists, skipping: {filename}")
                skipped_existing += 1
                continue
            
            # Extract article content from entry-content class
            extracted_title, html_content, publish_date = extract_article_content(url)
            
            if html_content:
                # Clean HTML and handle images
                clean_content = clean_html_content(html_content, url, img_dir)
                
                # Use extracted title if available, otherwise use the original
                final_title = extracted_title if extracted_title else title
                
                # Save article
                saved_filename = save_article_content(
                    final_title, url, clean_content, publish_date, articles_dir, category
                )
                
                if saved_filename:
                    successful_downloads += 1
                else:
                    failed_downloads += 1
            else:
                print("    ✗ Failed to extract entry-content")
                failed_downloads += 1
                
        except Exception as e:
            print(f"    ✗ Error processing article: {e}")
            failed_downloads += 1
    
    print("\n✅ Article generation complete!")
    print(f"  ✓ New articles created: {successful_downloads}")
    print(f"  ⏭ Existing articles skipped: {skipped_existing}")
    print(f"  ✗ Failed: {failed_downloads}")
    print(f"  📊 Total processed: {len(posts)}")
    
    return successful_downloads, skipped_existing, failed_downloads


def print_help():
    """Print help information about available commands."""
    help_text = """
ActionTech Blog Crawler - Help

Usage:
    python actiontech_crawler.py [options]

Options:
    (no options)        Run crawler in full mode to fetch all blog posts
    --incremental, -i   Run crawler in incremental mode (only new posts)
    --full, -f          Force full crawl (override incremental mode)
    --download, -d      Download full article content and images
    --download-only     Download content for existing posts only (skip crawling)
    --test              Run test to fetch first page only
    --test-filter       Test category filtering logic
    --help, -h          Show this help message

Features:
    ✓ Fetches all blog posts from ActionTech open source community
    ✓ Extracts post titles, URLs, and categories
    ✓ Handles pagination automatically
    ✓ Groups posts by category in markdown output
    ✓ Smart filtering - excludes ActionDB, ChatDBA, ClickHouse, DTLE, OceanBase, Kubernetes, MongoDB, Orchestrator, Redis
    ✓ Title filtering - excludes MariaDB, ScaleFlux, TiDB, OB运维, clickhouse, 行业趋势, obclient, OceanBase, kubernetes, Mongo, orchestrator, Redis
    ✓ Hard filters for MySQL核心模块揭秘 and 图解 MySQL categories
    ✓ Incremental crawling to avoid re-processing existing articles
    ✓ State tracking for efficient periodic runs
    ✓ Full article content downloading with image handling
    ✓ Automatic image download and local reference conversion
    ✓ HTML to Markdown conversion
    ✓ Provides summary statistics

Output:
    actiontech/
    ├── ActionTech技术干货.md      # All blog posts organized by category
    ├── crawl_state.json          # State file for incremental crawling
    └── articles/                 # Downloaded article content (with --download)
        ├── .img/                 # Downloaded images
        └── *.md                  # Individual article files

Examples:
    python actiontech_crawler.py              # Full crawl (posts only)
    python actiontech_crawler.py -i           # Incremental crawl (new posts only)
    python actiontech_crawler.py -d           # Full crawl with content download
    python actiontech_crawler.py -i -d        # Incremental with content download
    python actiontech_crawler.py --download-only  # Download content for existing posts
    python actiontech_crawler.py --test       # Test with first page only
    python actiontech_crawler.py --test-filter # Test filtering logic

Content Download Features:
    - Extracts content from HTML class="single-post-wrap entry-content" primarily
    - Falls back to class="entry-content" and other content patterns
    - Validates content length to avoid empty files
    - Converts HTML to clean Markdown format
    - Downloads all images referenced in articles
    - Updates image references to local paths (.img/ folder)
    - Preserves article structure (headers, lists, tables, code)
    - Generates individual .md files for each article
    - Skips existing files to avoid regeneration
    - Handles duplicate downloads efficiently

Incremental Mode:
    - Tracks previously crawled articles
    - Only processes new articles on subsequent runs
    - Maintains complete article database
    - Ideal for scheduled/periodic execution
    - Significantly faster for regular updates
    - Content download respects incremental mode
    """
    print(help_text)


def test_single_page():
    """Test function to crawl only the first page."""
    base_url = 'https://opensource.actionsky.com/category/技术干货'
    output_dir = 'actiontech'
    output_file = os.path.join(output_dir, 'ActionTech技术干货_测试.md')
    
    # Check if download is enabled
    download_content = '--download' in sys.argv or '-d' in sys.argv
    
    print("Testing single page crawl...")
    if download_content:
        print("Content download enabled for test")
    
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
        
        # Test content download if enabled
        if download_content and posts:
            print(f"\n📥 Testing content download for {len(posts)} posts...")
            successful, skipped, failed = generate_individual_articles(posts, output_dir)
            print("✓ Content download test completed:")
            print(f"  New articles: {successful}")
            print(f"  Skipped existing: {skipped}")
            print(f"  Failed: {failed}")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")


def test_filtering():
    """Test the category and title filtering logic with sample data."""
    
    # Test category filtering
    category_test_cases = [
        ("ActionDB", False),                    # Should be excluded
        ("ChatDBA", False),                     # Should be excluded
        ("ClickHouse", False),                  # Should be excluded
        ("ClickHouse 系列", False),              # Should be excluded
        ("DTLE", False),                        # Should be excluded
        ("DTLE 数据传输组件", False),             # Should be excluded
        ("OceanBase", False),                   # Should be excluded
        ("Kubernetes", False),                  # Should be excluded
        ("MongoDB", False),                     # Should be excluded (keyword match)
        ("Orchestrator 工具", False),           # Should be excluded (keyword match)
        ("Redis 缓存", False),                  # Should be excluded (keyword match)
        ("技术分享", True),                     # Should be included
        ("故障分析", True),                     # Should be included
        ("MySQL 新特性", True),                 # Should be included
        ("技术干货", True),                     # Should be included
        ("MySQL 核心模块揭秘", True),            # Should be included
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
        ("OB运维经验分享", False),                               # Should be excluded
        ("ClickHouse 性能优化", False),                          # Should be excluded
        ("行业趋势分析报告", False),                             # Should be excluded
        ("obclient 使用指南", False),                           # Should be excluded
        ("OceanBase 架构设计", False),                          # Should be excluded
        ("Kubernetes 部署实践", False),                         # Should be excluded
        ("MongoDB 数据建模", False),                            # Should be excluded
        ("Orchestrator 高可用", False),                         # Should be excluded
        ("Redis 集群管理", False),                              # Should be excluded
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
        ("图解MySQL架构", "图解 MySQL", "https://opensource.actionsky.com/category/技术专栏/mysql-picture/901", True),  # Should be included (hard filter)
        ("TiDB图解分析", "其他分类", "https://opensource.actionsky.com/category/技术专栏/mysql-picture/234", True),  # Should be included (hard filter overrides title filter)
        ("OB运维实践", "技术分享", "https://opensource.actionsky.com/345", False),                       # Should be excluded (title)
        ("Redis 缓存优化", "Redis", "https://opensource.actionsky.com/456", False),                    # Should be excluded (both title and category)
    ]
    
    print("\nTesting combined filtering logic:")
    for title, category, url, expected in combined_test_cases:
        result = should_include_post(title, category, url)
        status = "✓" if result == expected else "✗"
        reason = "title" if not should_include_title(title) else "category" if not should_include_category(category) else "both" if not should_include_title(title) and not should_include_category(category) else "hard filter" if "技术专栏/揭秘" in url or "技术专栏/mysql-picture" in url else "unknown"
        print(f"{status} '{title}' [{category}] -> {result} (expected: {expected})")
        if result != expected:
            print(f"    Reason: {reason} filter")


def should_include_category(category):
    """
    Determine if a blog post should be included based on category filtering rules.
    
    Rules:
    - Exclude categories containing keywords: "ActionDB", "ChatDBA", "ClickHouse", "DTLE", "OceanBase"
    - Keyword-based matching for better coverage
    - Include all other categories
    """
    # Convert to lowercase for case-insensitive comparison
    category_lower = category.lower()
    
    # List of category keywords to exclude (using keyword-based matching)
    excluded_category_keywords = [
        'actiondb',
        'chatdba',
        'clickhouse',
        'dtle',
        'oceanbase',
        'kubernetes',
        'mongo',
        'orchestrator',
        'redis'
    ]
    
    # Check if category contains any excluded keywords
    for keyword in excluded_category_keywords:
        if keyword in category_lower:
            return False
    
    return True


def should_include_title(title):
    """
    Determine if a blog post should be included based on title filtering rules.
    
    Rules:
    - Exclude titles containing: "MariaDB", "ScaleFlux", "TiDB", "OB运维", "clickhouse",
      "行业趋势", "obclient", "OceanBase", "kubernetes", "Mongo", "orchestrator", "Redis"
    - Case-insensitive matching
    """
    # Convert to lowercase for case-insensitive comparison
    title_lower = title.lower()
    
    # List of keywords to exclude from titles
    excluded_keywords = [
        'mariadb',
        'scaleflux',
        'tidb',
        'ob运维',
        'clickhouse',
        '行业趋势',
        'obclient',
        'oceanbase',
        'kubernetes',
        'mongo',
        'orchestrator',
        'redis'
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
    - Hard filter: Always include blogs from "图解 MySQL" category (URL contains "技术专栏/mysql-picture")
    """
    # Hard filter: Always include MySQL core module articles
    if url and "技术专栏/揭秘" in url:
        print(f"  Hard filter: Including MySQL核心模块揭秘 article: {title}")
        return True
    
    # Hard filter: Always include 图解 MySQL articles
    if url and "技术专栏/mysql-picture" in url:
        print(f"  Hard filter: Including 图解 MySQL article: {title}")
        return True
    
    return should_include_title(title) and should_include_category(category)


def main():
    """Main function to crawl ActionTech blog."""
    base_urls = [
        'https://opensource.actionsky.com/category/技术干货',
        'https://opensource.actionsky.com/category/技术专栏/揭秘',  # MySQL核心模块揭秘 category
        'https://opensource.actionsky.com/category/技术专栏/mysql-picture'  # 图解 MySQL category
    ]
    output_dir = 'actiontech'
    output_file = os.path.join(output_dir, 'ActionTech技术干货.md')
    state_file = os.path.join(output_dir, 'crawl_state.json')
    
    # Check for mode flags
    incremental_mode = '--incremental' in sys.argv or '-i' in sys.argv
    force_full = '--full' in sys.argv or '-f' in sys.argv
    download_content = '--download' in sys.argv or '-d' in sys.argv
    download_only = '--download-only' in sys.argv
    
    print("ActionTech Blog Crawler")
    print("=" * 40)
    
    if download_only:
        print("📥 Running in download-only mode")
        # Load existing posts from markdown file
        existing_posts = load_existing_posts(output_file)
        if not existing_posts:
            print("❌ No existing posts found. Run crawler first to generate post list.")
            return
        
        # Convert to the expected format for generate_individual_articles
        posts_for_processing = []
        for url, title in existing_posts.items():
            # Extract category from URL or use default
            category = extract_category_from_url(url)
            posts_for_processing.append((title, url, category))
        
        generate_individual_articles(posts_for_processing, output_dir)
        return
    
    if incremental_mode and not force_full:
        print("🔄 Running in incremental mode")
    else:
        print("🌐 Running in full crawl mode")
    
    if download_content:
        print("📥 Content download enabled")
    
    try:
        current_time = get_current_datetime()
        
        # Load previous crawl state and existing posts
        crawled_urls, last_crawl_time = load_crawl_state(state_file)
        existing_posts = load_existing_posts(output_file) if incremental_mode and not force_full else {}
        
        if incremental_mode and not force_full and last_crawl_time:
            print(f"📅 Last crawl: {last_crawl_time}")
            print(f"📄 Existing articles: {len(existing_posts)}")
        
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
        
        # Filter new posts if in incremental mode
        if incremental_mode and not force_full:
            new_posts = []
            for title, url, category in unique_posts:
                if url not in crawled_urls:
                    new_posts.append((title, url, category))
            
            print(f"📰 New posts found: {len(new_posts)}")
            
            if not new_posts:
                print("✅ No new articles found. Database is up to date!")
                return
                
            # Use only new posts for filtering
            posts_to_process = new_posts
        else:
            posts_to_process = unique_posts
        
        # Apply filtering and track statistics
        filtered_posts = []
        excluded_count = 0
        
        for title, url, category in posts_to_process:
            if should_include_post(title, category, url):
                filtered_posts.append((title, url, category))
            else:
                excluded_count += 1
                print(f"  Excluded [{category}]: {title}")
        
        if incremental_mode and not force_full:
            print("\n📊 Processing Summary:")
            print(f"  New posts found: {len(posts_to_process)}")
            print(f"  New posts excluded: {excluded_count}")
            print(f"  New posts to add: {len(filtered_posts)}")
        else:
            print("\n📊 Processing Summary:")
            print(f"  Total posts found: {len(posts_to_process)}")
            print(f"  Posts excluded: {excluded_count}")
            print(f"  Posts after filtering: {len(filtered_posts)}")
        
        # Write to markdown file
        total_posts, total_categories = write_markdown_file(
            output_file,
            filtered_posts,
            existing_posts if incremental_mode and not force_full else None,
            incremental_mode and not force_full
        )
        
        # Update crawl state
        all_filtered_urls = {url for _, url, _ in filtered_posts}
        if incremental_mode and not force_full:
            # Add new URLs to existing crawled URLs
            updated_crawled_urls = crawled_urls.union(all_filtered_urls)
        else:
            # Replace with current URLs
            updated_crawled_urls = all_filtered_urls
        
        save_crawl_state(state_file, updated_crawled_urls, current_time)
        
        print("\n✅ Successfully crawled ActionTech blog!")
        print(f"  Total articles in database: {total_posts}")
        if incremental_mode and not force_full:
            print(f"  New articles added: {len(filtered_posts)}")
        print(f"  Categories: {total_categories}")
        print(f"  Output file: {output_file}")
        print(f"  State file: {state_file}")
        
        if excluded_count > 0:
            print("\n🚫 Filtering Summary:")
            print(f"  Excluded {excluded_count} articles from unwanted categories/titles")
            print("  Excluded categories: ActionDB, ChatDBA, ClickHouse, DTLE, OceanBase, Kubernetes, MongoDB, Orchestrator, Redis")
            print("  Excluded title keywords: MariaDB, ScaleFlux, TiDB, OB运维, clickhouse, 行业趋势, obclient, OceanBase, kubernetes, Mongo, orchestrator, Redis")
        
        # Show category breakdown for new posts
        if filtered_posts:
            categories = {}
            for title, url, category in filtered_posts:
                categories[category] = categories.get(category, 0) + 1
            
            if incremental_mode and not force_full:
                print("\n📈 New articles by category:")
            else:
                print("\n📈 Articles by category:")
            for category, count in sorted(categories.items()):
                print(f"  {category}: {count} 篇")
        
        # Download article content if requested
        if download_content and filtered_posts:
            # Generate individual article files
            if incremental_mode and not force_full:
                articles_to_process = filtered_posts
                print(f"\n� Generating individual articles for {len(articles_to_process)} new posts...")
            else:
                # Load all posts for full processing
                all_posts_for_processing = []
                existing_posts_full = load_existing_posts(output_file)
                for url, title in existing_posts_full.items():
                    category = extract_category_from_url(url)
                    all_posts_for_processing.append((title, url, category))
                articles_to_process = all_posts_for_processing
                print(f"\n� Generating individual articles for all {len(articles_to_process)} posts...")
            
            generate_individual_articles(articles_to_process, output_dir)
        
    except Exception as e:
        print(f"✗ Error during crawling: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check command line arguments
    show_help = '--help' in sys.argv or '-h' in sys.argv
    run_test = '--test' in sys.argv
    test_filter = '--test-filter' in sys.argv
    incremental_mode = '--incremental' in sys.argv or '-i' in sys.argv
    force_full = '--full' in sys.argv or '-f' in sys.argv
    download_content = '--download' in sys.argv or '-d' in sys.argv
    download_only = '--download-only' in sys.argv
    
    if show_help:
        print_help()
    elif test_filter:
        test_filtering()
    elif run_test:
        test_single_page()
    else:
        main()
