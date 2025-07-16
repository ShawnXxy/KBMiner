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


def extract_article_links(content):
    """Extract article titles and links from monthly page content."""
    re_article_title_link = re.compile(r'class="main" href="/monthly/(.*?)">(.*?)</a></h3></li>', re.S)
    return re.findall(re_article_title_link, content)


def write_markdown_file(output_file, topic, base_url, month_links):
    """Write all content to markdown file."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write main title
        f.write(f'## {topic}\n\n')
        
        # Process each monthly report
        for month in month_links:
            # Fetch monthly page content
            month_url = base_url + month
            month_content = fetch_page_content(month_url)
            article_links = extract_article_links(month_content)
            
            # Only write month section if there are articles
            if article_links:
                f.write(f'### {month}\n')
                f.write('---\n\n')
                
                # Write each article as a bullet point on its own line
                for article_link, article_title in article_links:
                    full_link = base_url + article_link
                    f.write(f'- [{article_title}]({full_link})\n')
                
                f.write('\n')


def main():
    """Main function to crawl Alibaba MySQL monthly reports."""
    base_url = 'http://mysql.taobao.org/monthly/'
    output_dir = 'ali_monthly'
    output_file = os.path.join(output_dir, '阿里数据库内核月报.md')
    
    # Fetch main page and extract data
    main_content = fetch_page_content(base_url)
    topic = extract_topic(main_content)
    month_links = extract_month_links(main_content)
    
    # Generate markdown file
    write_markdown_file(output_file, topic, base_url, month_links)
    
    print(f"Successfully crawled {len(month_links)} monthly reports")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    main()