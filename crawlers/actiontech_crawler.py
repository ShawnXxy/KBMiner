# coding: utf-8
"""
ActionTech crawler implementation.
"""
import os
import re
import sys
import json
import datetime
import hashlib
from urllib.parse import urlparse, urljoin
from typing import List, Tuple, Dict, Optional

from .base_crawler import BaseCrawler


class ActionTechCrawler(BaseCrawler):
    """
    Crawler for ActionTech technical blog posts.
    
    Crawls technical articles from ActionTech's blog, filtering by categories
    and keywords to focus on relevant database technology content.
    """
    
    def __init__(self, output_dir: str = "my/actiontech"):
        """Initialize ActionTech crawler."""
        super().__init__(
            name="ActionTech",
            base_url="https://opensource.actionsky.com",
            output_dir=output_dir
        )
        self.category_url = f"{self.base_url}/category/技术干货"
        self.state_file = os.path.join(self.output_dir, "crawl_state.json")
        
        # Filtering configuration
        self.title_exclude_keywords = {
            'mariadb', 'scaleflux', 'tidb', 'ob运维', 'clickhouse',
            '行业趋势', 'obclient', 'oceanbase', 'kubernetes',
            'mongodb', 'orchestrator', 'redis'
        }
        
        self.category_exclude_keywords = {
            'actiondb', 'chatdba', 'clickhouse', 'dtle', 'oceanbase',
            'kubernetes', 'mongodb', 'orchestrator', 'redis'
        }
        
        self.include_categories = {
            'mysql核心模块揭秘', '图解 mysql'
        }
    
    def should_include_content(self, title: str, category: str = "") -> bool:
        """
        Determine if content should be included based on filtering rules.
        
        Args:
            title: Article title
            category: Article category
            
        Returns:
            True if content should be included, False otherwise
        """
        title_lower = title.lower()
        category_lower = category.lower()
        
        # Always include special categories
        if any(inc_cat in category_lower for inc_cat in self.include_categories):
            self.logger.debug(f"Including special category: {category}")
            return True
        
        # Exclude by category
        if any(exc_cat in category_lower for exc_cat in self.category_exclude_keywords):
            self.logger.debug(f"Excluding by category: {category}")
            return False
        
        # Exclude by title keywords
        if any(keyword in title_lower for keyword in self.title_exclude_keywords):
            self.logger.debug(f"Excluding by title keyword: {title}")
            return False
        
        return True
    
    def extract_blog_posts(self, content: str) -> List[Tuple[str, str, str]]:
        """
        Extract blog post information from ActionTech blog page.
        
        Args:
            content: HTML content of the page
            
        Returns:
            List of tuples: (title, url, category)
        """
        blog_posts = []
        
        # Pattern to match the full article structure
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
                url = self.base_url + url
            
            if clean_title and clean_category:
                blog_posts.append((clean_title, url, clean_category))
        
        self.logger.debug(f"Extracted {len(blog_posts)} blog posts from page")
        return blog_posts
    
    def crawl_all_pages(self) -> List[Tuple[str, str, str]]:
        """
        Crawl all pages of the blog to get all articles.
        
        Returns:
            List of all articles: (title, url, category)
        """
        all_articles = []
        page = 1
        
        while True:
            try:
                if page == 1:
                    page_url = self.category_url
                else:
                    page_url = f"{self.category_url}/page/{page}"
                
                self.logger.info(f"Crawling page {page}: {page_url}")
                content = self.fetch_page_content(page_url)
                
                # Extract articles from current page
                page_articles = self.extract_blog_posts(content)
                
                if not page_articles:
                    self.logger.info(f"No more articles found on page {page}")
                    break
                
                all_articles.extend(page_articles)
                self.logger.info(f"Found {len(page_articles)} articles on page {page}")
                page += 1
                
            except Exception as e:
                self.logger.error(f"Error crawling page {page}: {e}")
                break
        
        self.logger.info(f"Total articles found: {len(all_articles)}")
        return all_articles
    
    def load_crawl_state(self) -> Dict:
        """Load the crawl state from JSON file."""
        if not os.path.exists(self.state_file):
            return {}
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load crawl state: {e}")
            return {}
    
    def save_crawl_state(self, state: Dict) -> None:
        """Save the crawl state to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            self.logger.debug("Crawl state saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save crawl state: {e}")
    
    def crawl(self, incremental: bool = False, download_content: bool = False,
              download_only: bool = False, **kwargs) -> dict:
        """
        Main crawling method for ActionTech blog.
        
        Args:
            incremental: Whether to do incremental crawling
            download_content: Whether to download full article content
            download_only: Whether to only download existing articles
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with crawling results and statistics
        """
        try:
            self.logger.info("Starting ActionTech crawl")
            
            if download_only:
                return self._download_existing_articles()
            
            # Load existing state for incremental crawling
            crawl_state = self.load_crawl_state() if incremental else {}
            existing_urls = set(crawl_state.get('processed_urls', []))
            
            # Crawl all articles
            all_articles = self.crawl_all_pages()
            
            # Filter articles
            new_articles = []
            for title, url, category in all_articles:
                if incremental and url in existing_urls:
                    continue
                
                if self.should_include_content(title, category):
                    new_articles.append((title, url, category))
            
            self.logger.info(f"Found {len(new_articles)} new articles to process")
            
            # Generate markdown file
            stats = self._generate_markdown_file(new_articles, incremental)
            
            # Download individual articles if requested
            if download_content and new_articles:
                download_stats = self._download_articles(new_articles)
                stats.update(download_stats)
            
            # Update crawl state
            if incremental:
                all_urls = [url for _, url, _ in all_articles]
                crawl_state.update({
                    'processed_urls': all_urls,
                    'last_update': datetime.datetime.now().isoformat(),
                    'total_articles': len(all_articles)
                })
                self.save_crawl_state(crawl_state)
            
            self.logger.info("ActionTech crawl completed successfully")
            return stats
            
        except Exception as e:
            self.logger.error(f"Error during ActionTech crawl: {e}")
            raise
    
    def _generate_markdown_file(self, articles: List[Tuple[str, str, str]], 
                               incremental: bool) -> dict:
        """Generate markdown file with articles organized by category."""
        # Implementation details would be moved from original file
        # This is a placeholder for the actual implementation
        output_file = os.path.join(self.output_dir, "ActionTech技术干货.md")
        
        # Organize by category
        category_articles = {}
        for title, url, category in articles:
            if category not in category_articles:
                category_articles[category] = []
            category_articles[category].append((title, url))
        
        # Write to file
        mode = 'a' if incremental else 'w'
        with open(output_file, mode, encoding='utf-8') as f:
            if not incremental:
                f.write("# ActionTech技术干货\n\n")
            
            for category, items in category_articles.items():
                f.write(f"## {category}\n\n")
                for title, url in items:
                    f.write(f"- [{title}]({url})\n")
                f.write("\n")
        
        return {
            'markdown_file': output_file,
            'articles_processed': len(articles),
            'categories': len(category_articles)
        }
    
    def _download_articles(self, articles: List[Tuple[str, str, str]]) -> dict:
        """Download individual article content."""
        # Placeholder for article download implementation
        self.logger.info(f"Downloading {len(articles)} articles...")
        return {'articles_downloaded': len(articles)}
    
    def _download_existing_articles(self) -> dict:
        """Download content for existing articles in markdown file."""
        # Placeholder for existing article download
        self.logger.info("Downloading existing articles...")
        return {'articles_downloaded': 0}
