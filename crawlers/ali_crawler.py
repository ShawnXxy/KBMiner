# coding: utf-8
"""
Alibaba Database Monthly Report crawler implementation.
"""
import os
import re
import hashlib
from urllib.parse import urljoin, urlparse
from typing import List, Tuple, Dict, Optional

from .base_crawler import BaseCrawler


class AliCrawler(BaseCrawler):
    """
    Crawler for Alibaba Database Monthly Reports.
    
    Crawls MySQL/InnoDB focused articles from Alibaba's monthly database reports,
    filtering out other database technologies to maintain focus.
    """
    
    def __init__(self, output_dir: str = "my/ali_monthly"):
        """Initialize Alibaba crawler."""
        super().__init__(
            name="Alibaba",
            base_url="http://mysql.taobao.org/monthly/",
            output_dir=output_dir
        )
        self.tracking_file = os.path.join(self.output_dir, '.processed_months.txt')
        
        # Filtering configuration
        self.exclusion_keywords = [
            'polardb', 'plardb', 'mariadb', 'tokudb', 'myrocks',
            'rocksdb', 'hybriddb', 'x-engine', '行业动态', '行业洞察', '社区见闻'
        ]
    
    def should_include_content(self, title: str, **kwargs) -> bool:
        """
        Determine if an article should be included based on title filtering rules.
        
        Rules:
        - Include if title contains "MySQL" or "InnoDB" (case-insensitive)
        - Exclude if title contains exclusion keywords, even if it has MySQL/InnoDB
        
        Args:
            title: Article title to check
            **kwargs: Additional parameters (unused)
            
        Returns:
            True if content should be included, False otherwise
        """
        title_lower = title.lower()
        
        # First check exclusion keywords
        for keyword in self.exclusion_keywords:
            if keyword in title_lower:
                self.logger.debug(f"Excluding article by keyword '{keyword}': {title}")
                return False
        
        # Check if it contains MySQL or InnoDB
        include = 'mysql' in title_lower or 'innodb' in title_lower
        if include:
            self.logger.debug(f"Including MySQL/InnoDB article: {title}")
        else:
            self.logger.debug(f"Excluding non-MySQL/InnoDB article: {title}")
        
        return include
    
    def extract_topic(self, content: str) -> str:
        """Extract webpage title from content."""
        re_topic = re.compile(r'<!-- <title>(.*?)</title> -->', re.S)
        matches = re.findall(re_topic, content)
        return matches[0] if matches else "Alibaba Database Monthly Reports"
    
    def extract_month_links(self, content: str) -> List[str]:
        """Extract monthly report links from main page content."""
        re_month_blog_address = re.compile(
            r'<a target="_top" class="main" href="/monthly/(.*?)">', re.S
        )
        return re.findall(re_month_blog_address, content)
    
    def extract_article_links(self, content: str) -> List[Tuple[str, str]]:
        """Extract article titles and links from monthly page content."""
        re_article_title_link = re.compile(
            r'<a class="post-link" href="(.*?)".*?<strong>(.*?)</strong>', re.S
        )
        all_articles = re.findall(re_article_title_link, content)
        
        # Filter articles based on the inclusion criteria
        filtered_articles = [
            (link, title) for link, title in all_articles
            if self.should_include_content(title)
        ]
        
        self.logger.debug(
            f"Filtered {len(filtered_articles)} articles from {len(all_articles)} total"
        )
        return filtered_articles
    
    def crawl(self, incremental: bool = True, download_articles: bool = False,
              test_articles: bool = False, **kwargs) -> dict:
        """
        Main crawling method for Alibaba monthly reports.
        
        Args:
            incremental: Whether to do incremental crawling
            download_articles: Whether to download full article content
            test_articles: Whether to test with a few articles only
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with crawling results and statistics
        """
        try:
            self.logger.info("Starting Alibaba monthly reports crawl")
            
            # Fetch main page content
            main_content = self.fetch_page_content(self.base_url)
            topic = self.extract_topic(main_content)
            all_month_links = self.extract_month_links(main_content)
            
            self.logger.info(f"Found {len(all_month_links)} monthly reports")
            
            # Determine which months to process
            if incremental:
                existing_months = self.load_processed_items(self.tracking_file)
                new_months = [month for month in all_month_links if month not in existing_months]
                self.logger.info(f"Processing {len(new_months)} new months (incremental mode)")
            else:
                new_months = all_month_links
                self.logger.info(f"Processing all {len(new_months)} months (full mode)")
            
            # Generate or update markdown file
            output_file = os.path.join(self.output_dir, "阿里数据库内核月报.md")
            
            if incremental and new_months:
                stats = self._append_new_months_to_file(output_file, topic, new_months)
            elif not incremental:
                stats = self._write_complete_markdown_file(output_file, topic, all_month_links)
            else:
                stats = {'total_articles': 0, 'filtered_articles': 0}
                self.logger.info("No new months to process")
            
            # Download individual articles if requested
            if download_articles:
                if test_articles:
                    download_stats = self._test_article_download(all_month_links[:3])
                else:
                    download_stats = self._download_all_articles(all_month_links)
                stats.update(download_stats)
            
            self.logger.info("Alibaba crawl completed successfully")
            return stats
            
        except Exception as e:
            self.logger.error(f"Error during Alibaba crawl: {e}")
            raise
    
    def _write_complete_markdown_file(self, output_file: str, topic: str, 
                                     month_links: List[str]) -> dict:
        """Write complete markdown file with all months."""
        total_articles = 0
        filtered_articles = 0
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'## {topic} (MySQL/InnoDB Focus)\n\n')
            
            for month in month_links:
                try:
                    month_url = self.base_url + month
                    month_content = self.fetch_page_content(month_url)
                    filtered_article_links = self.extract_article_links(month_content)
                    
                    total_articles += len(filtered_article_links)
                    filtered_articles += len(filtered_article_links)
                    
                    if filtered_article_links:
                        f.write(f'### {month}\n---\n\n')
                        for article_link, article_title in filtered_article_links:
                            full_link = self.base_url + article_link
                            f.write(f'- [{article_title}]({full_link})\n')
                        f.write('\n')
                    
                    self.logger.info(f"Processed {month}: {len(filtered_article_links)} articles")
                    
                except Exception as e:
                    self.logger.warning(f"Could not process {month}: {e}")
        
        return {'total_articles': total_articles, 'filtered_articles': filtered_articles}
    
    def _append_new_months_to_file(self, output_file: str, topic: str, 
                                  new_months: List[str]) -> dict:
        """Append only new months to existing markdown file."""
        total_articles = 0
        filtered_articles = 0
        
        # Create file with header if it doesn't exist
        if not os.path.exists(output_file):
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f'## {topic} (MySQL/InnoDB Focus)\n\n')
        
        # Append new months
        with open(output_file, 'a', encoding='utf-8') as f:
            for month in new_months:
                try:
                    month_url = self.base_url + month
                    month_content = self.fetch_page_content(month_url)
                    filtered_article_links = self.extract_article_links(month_content)
                    
                    total_articles += len(filtered_article_links)
                    filtered_articles += len(filtered_article_links)
                    
                    if filtered_article_links:
                        f.write(f'### {month}\n---\n\n')
                        for article_link, article_title in filtered_article_links:
                            full_link = self.base_url + article_link
                            f.write(f'- [{article_title}]({full_link})\n')
                        f.write('\n')
                    
                    # Save processed month
                    self.save_processed_item(self.tracking_file, month)
                    self.logger.info(f"Processed {month}: {len(filtered_article_links)} articles")
                    
                except Exception as e:
                    self.logger.warning(f"Could not process {month}: {e}")
        
        return {'total_articles': total_articles, 'filtered_articles': filtered_articles}
    
    def _download_all_articles(self, month_links: List[str]) -> dict:
        """Download all individual articles."""
        # Placeholder for article download implementation
        self.logger.info(f"Would download articles from {len(month_links)} months")
        return {'articles_downloaded': 0}
    
    def _test_article_download(self, test_months: List[str]) -> dict:
        """Test download with a few articles."""
        # Placeholder for test download implementation
        self.logger.info(f"Testing download with {len(test_months)} months")
        return {'articles_downloaded': 0}
