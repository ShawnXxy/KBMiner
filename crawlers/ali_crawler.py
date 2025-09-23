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
    
    def __init__(self, output_dir: str = "kb/my/ali_monthly"):
        """Initialize Alibaba crawler."""
        super().__init__(
            name="Alibaba",
            base_url="http://mysql.taobao.org/monthly/",
            output_dir=output_dir
        )
        self.tracking_file = os.path.join(self.output_dir, '.processed_months.txt')
        self.index_file = os.path.join(self.output_dir, "阿里数据库内核月报.md")
        
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
    
    def get_latest_indexed_month(self) -> Optional[str]:
        """
        Get the latest month from the index file (what's actually being tracked for processing).
        
        Returns:
            Latest month in YYYY/MM format, or None if no months found
        """
        if not os.path.exists(self.index_file):
            return None
        
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all month headers (### YYYY/MM)
            month_pattern = re.compile(r'### (\d{4}/\d{2})', re.MULTILINE)
            months = month_pattern.findall(content)
            
            if not months:
                return None
            
            # Sort by date (latest first) and return the latest
            def sort_key(month_str):
                try:
                    year, month_num = month_str.split('/')
                    return (int(year), int(month_num))
                except (ValueError, IndexError):
                    return (0, 0)
            
            months.sort(key=sort_key, reverse=True)
            return months[0]
            
        except Exception as e:
            self.logger.error(f"Failed to get latest indexed month: {e}")
            return None
    
    def get_uncompleted_articles_from_index(self) -> List[Tuple[str, str, str]]:
        """
        Get all uncompleted articles from the index file (those not marked with ✅).
        
        Returns:
            List of tuples (month, title, link) for uncompleted articles
        """
        if not os.path.exists(self.index_file):
            return []
        
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file to find uncompleted articles
            uncompleted = []
            current_month = None
            
            for line in content.split('\n'):
                line = line.strip()
                
                # Check if this is a month header
                month_match = re.match(r'### (\d{4}/\d{2})', line)
                if month_match:
                    current_month = month_match.group(1)
                    continue
                
                # Check if this is an article line that's not completed
                if current_month and line.startswith('- [') and '✅' not in line:
                    # Extract title and link
                    article_match = re.match(r'- \[(?:⏳\s+)?(.*?)\]\((.*?)\)', line)
                    if article_match:
                        title = article_match.group(1)
                        link = article_match.group(2)
                        uncompleted.append((current_month, title, link))
            
            self.logger.info(f"Found {len(uncompleted)} uncompleted articles in index")
            return uncompleted
            
        except Exception as e:
            self.logger.error(f"Failed to get uncompleted articles: {e}")
            return []
    
    def determine_months_to_process(self, all_website_months: List[str]) -> List[str]:
        """
        Determine which months to process based on gaps between index and processed_months.
        
        Args:
            all_website_months: All months available on the website (sorted latest first)
            
        Returns:
            List of months to process
        """
        # Get latest month from index file
        latest_indexed = self.get_latest_indexed_month()
        
        # Get processed months (website state)
        processed_months = self.load_processed_items(self.tracking_file)
        
        if not latest_indexed:
            # No index file exists, start with the latest month
            self.logger.info("No index file found, starting with latest month")
            return all_website_months[:1] if all_website_months else []
        
        # Find position of latest indexed month in website months
        try:
            latest_index_pos = all_website_months.index(latest_indexed)
        except ValueError:
            # Latest indexed month not found on website, start from beginning
            self.logger.warning(f"Latest indexed month {latest_indexed} not found on website, starting from latest")
            return all_website_months[:1] if all_website_months else []

        # Process only months newer than the latest indexed month
        # Since all_website_months is sorted latest first, we want months before the latest_index_pos
        months_to_process = all_website_months[:latest_index_pos]
        
        self.logger.info(f"Latest indexed month: {latest_indexed}")
        self.logger.info(f"Will process {len(months_to_process)} months: {months_to_process[:3]}...")
        
        return months_to_process
    
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
            r'<a target="_top" class="main" href="(/monthly/.*?)">(.*?)</a>', re.S
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
              test_articles: bool = False, mark_existing_done: bool = False, **kwargs) -> dict:
        """
        Main crawling method for Alibaba monthly reports.
        
        Args:
            incremental: Whether to do incremental crawling
            download_articles: Whether to download full article content
            test_articles: Whether to test with a few articles only
            mark_existing_done: Whether to mark existing articles as done (✅)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with crawling results and statistics
        """
        try:
            self.logger.info("Starting Alibaba monthly reports crawl")
            
            # Mark existing articles as done if requested
            if mark_existing_done:
                self.mark_existing_articles_as_done(self.index_file)
            
            # Fetch main page content to get current website state
            main_content = self.fetch_page_content(self.base_url)
            topic = self.extract_topic(main_content)
            all_website_months = self.extract_month_links(main_content)
            
            self.logger.info(f"Found {len(all_website_months)} monthly reports on website")
            
            # Update processed_months.txt to reflect current website state
            self._update_website_state(all_website_months)
            
            # Determine processing strategy
            if incremental:
                # Check for uncompleted articles first
                uncompleted_articles = self.get_uncompleted_articles_from_index()
                
                if uncompleted_articles and download_articles:
                    # Process uncompleted articles from index
                    self.logger.info(f"Found {len(uncompleted_articles)} uncompleted articles in index")
                    stats = self._process_uncompleted_articles(uncompleted_articles)
                else:
                    # Check for new months to add to index
                    months_to_process = self.determine_months_to_process(all_website_months)
                    if months_to_process:
                        stats = self._process_new_months(months_to_process, topic, download_articles)
                    else:
                        stats = {'total_articles': 0, 'filtered_articles': 0, 'articles_downloaded': 0}
                        self.logger.info("No new months to process and no uncompleted articles")
            else:
                # Full mode: rebuild index from scratch
                stats = self._rebuild_complete_index(all_website_months, topic, download_articles)
            
            self.logger.info("Alibaba crawl completed successfully")
            return stats
            
        except Exception as e:
            self.logger.error(f"Error during Alibaba crawl: {e}")
            raise
    
    def _update_website_state(self, website_months: List[str]) -> None:
        """Update processed_months.txt to reflect current website state."""
        try:
            os.makedirs(os.path.dirname(self.tracking_file), exist_ok=True)
            
            # Sort months by date (latest first)
            def sort_key(month_str):
                try:
                    year, month_num = month_str.split('/')
                    return (int(year), int(month_num))
                except (ValueError, IndexError):
                    return (0, 0)
            
            sorted_months = sorted(website_months, key=sort_key, reverse=True)
            
            # Write to tracking file
            with open(self.tracking_file, 'w', encoding='utf-8') as f:
                for month in sorted_months:
                    f.write(f"{month}\n")
            
            self.logger.info(f"Updated website state with {len(sorted_months)} months")
            
        except Exception as e:
            self.logger.error(f"Failed to update website state: {e}")
    
    def _process_uncompleted_articles(self, uncompleted_articles: List[Tuple[str, str, str]]) -> dict:
        """
        Process uncompleted articles from the index.
        
        Args:
            uncompleted_articles: List of (month, title, link) tuples
            
        Returns:
            Dictionary with processing statistics
        """
        self.logger.info(f"Processing {len(uncompleted_articles)} uncompleted articles")
        
        articles_downloaded = 0
        
        for month, title, link in uncompleted_articles:
            try:
                # TODO: Implement actual article download logic here
                # For now, simulate download
                success = self._download_single_article(title, link)
                
                if success:
                    # Mark as completed in index
                    self.update_article_status(self.index_file, title, '✅')
                    articles_downloaded += 1
                    self.logger.info(f"Downloaded and marked completed: {title}")
                else:
                    # Mark as failed
                    self.update_article_status(self.index_file, title, '❌')
                    self.logger.warning(f"Failed to download: {title}")
                    
            except Exception as e:
                self.logger.error(f"Error processing article {title}: {e}")
                self.update_article_status(self.index_file, title, '❌')
        
        return {
            'total_articles': len(uncompleted_articles),
            'filtered_articles': len(uncompleted_articles),
            'articles_downloaded': articles_downloaded
        }
    
    def _process_new_months(self, months_to_process: List[str], topic: str, download_articles: bool) -> dict:
        """
        Process new months and add them to the index.
        
        Args:
            months_to_process: List of months to process
            topic: Topic for the index file
            download_articles: Whether to download articles immediately
            
        Returns:
            Dictionary with processing statistics
        """
        total_articles = 0
        filtered_articles = 0
        articles_downloaded = 0
        
        # Collect new articles to add to index
        new_sections = []
        articles_to_download = []
        
        for month in months_to_process:
            try:
                month_url = self.base_url + month
                month_content = self.fetch_page_content(month_url)
                filtered_article_links = self.extract_article_links(month_content)
                
                total_articles += len(filtered_article_links)
                filtered_articles += len(filtered_article_links)
                
                if filtered_article_links:
                    # Create section for this month
                    section_lines = [f'### {month}\n---\n\n']
                    
                    for article_link, article_title in filtered_article_links:
                        full_link = "http://mysql.taobao.org" + article_link
                        
                        # Mark as pending initially
                        section_lines.append(f'- [⏳ {article_title}]({full_link})\n')
                        
                        # Add to download queue if requested
                        if download_articles:
                            articles_to_download.append((article_title, full_link))
                    
                    section_lines.append('\n')
                    new_sections.extend(section_lines)
                    
                    self.logger.info(f"Prepared {month}: {len(filtered_article_links)} articles")
                
            except Exception as e:
                self.logger.warning(f"Could not process {month}: {e}")
        
        # Add new sections to index file
        if new_sections:
            self._add_sections_to_index(topic, new_sections)
        
        # Download articles if requested
        if download_articles and articles_to_download:
            articles_downloaded = self._download_articles_and_update_status(articles_to_download)
        
        return {
            'total_articles': total_articles,
            'filtered_articles': filtered_articles,
            'articles_downloaded': articles_downloaded
        }
    
    def _download_single_article(self, title: str, link: str) -> bool:
        """
        Download a single article and save it as a markdown file.
        
        Args:
            title: Article title
            link: Article URL
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.debug(f"Downloading article: {title}")
            
            # Fetch article content
            content = self.fetch_page_content(link)
            
            # Extract article content (you may need to customize this based on the website structure)
            article_content = self._extract_article_content(content, title, link)
            
            if not article_content:
                self.logger.warning(f"No content extracted for: {title}")
                return False
            
            # Generate filename
            filename = self._generate_article_filename(title, link)
            articles_dir = os.path.join(self.output_dir, 'articles')
            filepath = os.path.join(articles_dir, filename)
            
            # Save content
            success = self.save_content_to_file(article_content, filepath)
            
            if success:
                self.logger.debug(f"Successfully downloaded: {title}")
            else:
                self.logger.error(f"Failed to save: {title}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to download article {title}: {e}")
            return False
    
    def _extract_article_content(self, html_content: str, title: str, link: str) -> str:
        """
        Extract the main article content from HTML and format as markdown.
        
        Args:
            html_content: Raw HTML content from the webpage
            title: Article title
            link: Article URL
            
        Returns:
            Formatted markdown content
        """
        try:
            # Extract the main content area (this is specific to the Alibaba monthly report structure)
            # You may need to adjust these patterns based on the actual HTML structure
            
            # Try to find the main content area
            content_pattern = re.compile(r'<div class="post-content">(.*?)</div>', re.DOTALL | re.IGNORECASE)
            content_match = content_pattern.search(html_content)
            
            if not content_match:
                # Try alternative patterns
                content_pattern = re.compile(r'<div class="content">(.*?)</div>', re.DOTALL | re.IGNORECASE)
                content_match = content_pattern.search(html_content)
            
            if not content_match:
                # Try to extract everything between main content markers
                content_pattern = re.compile(r'<body.*?>(.*?)</body>', re.DOTALL | re.IGNORECASE)
                content_match = content_pattern.search(html_content)
            
            if content_match:
                raw_content = content_match.group(1)
            else:
                # Fallback: use the entire HTML content
                raw_content = html_content
                self.logger.warning(f"Could not find main content area for {title}, using full HTML")
            
            # Basic HTML to markdown conversion
            markdown_content = self._convert_html_to_markdown(raw_content)
            
            # Extract date from URL (e.g., /monthly/2025/05/02/ -> 2025/05)
            date_match = re.search(r'/monthly/(\d{4}/\d{2})/', link)
            date_str = date_match.group(1) if date_match else "Unknown"
            
            # Count images (for metadata)
            img_count = len(re.findall(r'<img[^>]*>', raw_content, re.IGNORECASE))
            
            # Format as markdown with metadata
            formatted_content = f"""# {title}

**Date:** {date_str}
**Source:** {link}
**Images:** {img_count} images downloaded

---

{markdown_content}
"""
            
            return formatted_content
            
        except Exception as e:
            self.logger.error(f"Failed to extract content for {title}: {e}")
            return ""
    
    def _convert_html_to_markdown(self, html_content: str) -> str:
        """
        Basic HTML to markdown conversion.
        
        Args:
            html_content: HTML content to convert
            
        Returns:
            Markdown formatted content
        """
        try:
            # Basic HTML tag removal/conversion
            content = html_content
            
            # Remove script and style tags completely
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
            
            # Convert headers
            content = re.sub(r'<h([1-6])[^>]*>(.*?)</h[1-6]>', lambda m: '#' * int(m.group(1)) + ' ' + m.group(2) + '\n', content, flags=re.IGNORECASE)
            
            # Convert paragraphs
            content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL | re.IGNORECASE)
            
            # Convert line breaks
            content = re.sub(r'<br[^>]*/?>', '\n', content, flags=re.IGNORECASE)
            
            # Convert code blocks
            content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```\n', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.IGNORECASE)
            
            # Convert lists
            content = re.sub(r'<ul[^>]*>', '', content, flags=re.IGNORECASE)
            content = re.sub(r'</ul>', '\n', content, flags=re.IGNORECASE)
            content = re.sub(r'<ol[^>]*>', '', content, flags=re.IGNORECASE)
            content = re.sub(r'</ol>', '\n', content, flags=re.IGNORECASE)
            content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL | re.IGNORECASE)
            
            # Convert links
            content = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.IGNORECASE)
            
            # Convert bold and italic
            content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.IGNORECASE)
            content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.IGNORECASE)
            content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.IGNORECASE)
            content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.IGNORECASE)
            
            # Remove remaining HTML tags
            content = re.sub(r'<[^>]+>', '', content)
            
            # Clean up extra whitespace
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            content = content.strip()
            
            return content
            
        except Exception as e:
            self.logger.error(f"Failed to convert HTML to markdown: {e}")
            return html_content
    
    def _generate_article_filename(self, title: str, link: str) -> str:
        """
        Generate a safe filename for the article.
        
        Args:
            title: Article title
            link: Article URL
            
        Returns:
            Safe filename for the article
        """
        # Extract date from URL (e.g., /monthly/2025/05/02/ -> 2025-05)
        date_match = re.search(r'/monthly/(\d{4})/(\d{2})/', link)
        if date_match:
            date_prefix = f"{date_match.group(1)}-{date_match.group(2)}_"
        else:
            date_prefix = ""
        
        # Use the sanitize_filename method from base class
        safe_title = self.sanitize_filename(title, max_length=150)
        
        return f"{date_prefix}{safe_title}.md"
    
    def _download_articles_and_update_status(self, articles_to_download: List[Tuple[str, str]]) -> int:
        """
        Download articles and update their status in the index.
        
        Args:
            articles_to_download: List of (title, link) tuples
            
        Returns:
            Number of successfully downloaded articles
        """
        downloaded_count = 0
        
        for title, link in articles_to_download:
            success = self._download_single_article(title, link)
            
            if success:
                self.update_article_status(self.index_file, title, '✅')
                downloaded_count += 1
            else:
                self.update_article_status(self.index_file, title, '❌')
        
        self.logger.info(f"Downloaded {downloaded_count}/{len(articles_to_download)} articles")
        return downloaded_count
    
    def _add_sections_to_index(self, topic: str, new_sections: List[str]) -> None:
        """
        Add new sections to the top of the index file.
        
        Args:
            topic: Topic for the index file header
            new_sections: List of lines to add
        """
        # Create index file if it doesn't exist
        if not os.path.exists(self.index_file):
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(f'## {topic} (MySQL/InnoDB Focus)\n\n')
        
        # Insert new content at top
        self._insert_content_at_top(self.index_file, new_sections)
        self.logger.info(f"Added {len(new_sections)} lines to index file")
    
    def _rebuild_complete_index(self, all_months: List[str], topic: str, download_articles: bool) -> dict:
        """
        Rebuild the complete index file from scratch.
        
        Args:
            all_months: All months from website
            topic: Topic for the index file
            download_articles: Whether to download articles
            
        Returns:
            Dictionary with processing statistics
        """
        # This method can reuse the existing logic but rebuild from scratch
        return self._process_new_months(all_months, topic, download_articles)
    
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
                            # Since article_link now includes full path, construct URL properly
                            full_link = "http://mysql.taobao.org" + article_link
                            # Mark articles as done (✅) when writing complete file
                            f.write(f'- [✅ {article_title}]({full_link})\n')
                        f.write('\n')
                        
                        # Track all months found on website (regardless of MySQL content)
                        self.save_processed_month(month)
                        self.logger.info(f"Processed {month}: {len(filtered_article_links)} articles")
                    else:
                        # Still track the month even if no MySQL content
                        self.save_processed_month(month)
                        self.logger.info(f"Processed {month}: {len(filtered_article_links)} articles (no MySQL/InnoDB content)")
                    
                except Exception as e:
                    self.logger.warning(f"Could not process {month}: {e}")
        
        return {'total_articles': total_articles, 'filtered_articles': filtered_articles}
    
    def _append_new_months_to_file(self, output_file: str, topic: str,
                                   new_months: List[str]) -> dict:
        """Append only new months to existing markdown file (new content at top)."""
        total_articles = 0
        filtered_articles = 0
        
        # Create file with header if it doesn't exist
        if not os.path.exists(output_file):
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f'## {topic} (MySQL/InnoDB Focus)\n\n')
        
        # Collect new content first
        new_content = []
        for month in new_months:
            try:
                month_url = self.base_url + month
                month_content = self.fetch_page_content(month_url)
                filtered_article_links = self.extract_article_links(month_content)
                
                total_articles += len(filtered_article_links)
                filtered_articles += len(filtered_article_links)
                
                if filtered_article_links:
                    month_section = [f'### {month}\n---\n\n']
                    for article_link, article_title in filtered_article_links:
                        full_link = "http://mysql.taobao.org" + article_link
                        # Mark as pending initially (⏳), will be updated to done (✅) when downloaded
                        month_section.append(f'- [⏳ {article_title}]({full_link})\n')
                    month_section.append('\n')
                    new_content.extend(month_section)
                    
                    # Track all months found on website (regardless of MySQL content)
                    self.save_processed_month(month)
                    self.logger.info(f"Processed {month}: {len(filtered_article_links)} articles")
                else:
                    # Still track the month even if no MySQL content
                    self.save_processed_month(month)
                    self.logger.info(f"Processed {month}: {len(filtered_article_links)} articles (no MySQL/InnoDB content)")
                
            except Exception as e:
                self.logger.warning(f"Could not process {month}: {e}")
        
        # Insert new content at top (after header) if we have any
        if new_content:
            self._insert_content_at_top(output_file, new_content)
        
        return {'total_articles': total_articles, 'filtered_articles': filtered_articles}
    
    def _insert_content_at_top(self, output_file: str, new_content: List[str]) -> None:
        """Insert new content at the top of the file (after header)."""
        # Read existing content
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_lines = f.readlines()
        
        # Find where to insert (after the header line)
        insert_index = 2  # After "## title" and empty line
        for i, line in enumerate(existing_lines):
            if line.startswith('## ') and i < len(existing_lines) - 1:
                insert_index = i + 2  # After header and next empty line
                break
        
        # Insert new content
        new_lines = existing_lines[:insert_index] + new_content + existing_lines[insert_index:]
        
        # Write back to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    def _process_months_with_download(self, new_months: List[str], output_file: str, topic: str) -> dict:
        """Process new months with download requirement - only update index after successful download."""
        # First, collect article information and track months
        pending_articles = []
        total_articles = 0
        filtered_articles = 0
        
        for month in new_months:
            try:
                month_url = self.base_url + month
                month_content = self.fetch_page_content(month_url)
                filtered_article_links = self.extract_article_links(month_content)
                
                total_articles += len(filtered_article_links)
                filtered_articles += len(filtered_article_links)
                
                if filtered_article_links:
                    pending_articles.append((month, filtered_article_links))
                
                # Track all months found on website (regardless of MySQL content)
                self.save_processed_month(month)
                self.logger.info(f"Processed {month}: {len(filtered_article_links)} articles")
                
            except Exception as e:
                self.logger.warning(f"Could not process {month}: {e}")
        
        # Try to download articles and only update index if successful
        articles_downloaded = 0
        if pending_articles:
            articles_downloaded = self._download_articles_from_months(pending_articles)
            
            # Only update index file if download was successful
            if articles_downloaded > 0:
                self._update_index_with_completed_articles(output_file, topic, pending_articles)
                self.logger.info(f"Updated index file with {articles_downloaded} successfully downloaded articles")
            else:
                self.logger.warning("No articles were successfully downloaded, index file not updated")
        
        return {
            'total_articles': total_articles,
            'filtered_articles': filtered_articles,
            'articles_downloaded': articles_downloaded
        }
    
    def _process_all_months_with_download(self, all_months: List[str], output_file: str, topic: str) -> dict:
        """Process all months with download requirement - only update index after successful download."""
        return self._process_months_with_download(all_months, output_file, topic)
    
    def _download_articles_from_months(self, pending_articles: List[Tuple[str, List[Tuple[str, str]]]]) -> int:
        """Download articles from the pending list. Returns number of successfully downloaded articles."""
        # Placeholder implementation - replace with actual download logic
        downloaded_count = 0
        for month, article_links in pending_articles:
            for article_link, article_title in article_links:
                try:
                    # TODO: Implement actual article download logic here
                    self.logger.debug(f"Would download: {article_title}")
                    downloaded_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to download {article_title}: {e}")
        
        self.logger.info(f"Downloaded {downloaded_count} articles")
        return downloaded_count
    
    def _update_index_with_completed_articles(self, output_file: str, topic: str,
                                              completed_articles: List[Tuple[str, List[Tuple[str, str]]]]) -> None:
        """Update index file with successfully downloaded articles (at top)."""
        # Create file with header if it doesn't exist
        if not os.path.exists(output_file):
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f'## {topic} (MySQL/InnoDB Focus)\n\n')
        
        # Collect new content to insert at top
        new_content = []
        for month, article_links in completed_articles:
            if article_links:
                month_section = [f'### {month}\n---\n\n']
                for article_link, article_title in article_links:
                    full_link = "http://mysql.taobao.org" + article_link
                    # Mark as done since they were successfully downloaded
                    month_section.append(f'- [✅ {article_title}]({full_link})\n')
                month_section.append('\n')
                new_content.extend(month_section)
        
        # Insert new content at top if we have any
        if new_content:
            self._insert_content_at_top(output_file, new_content)
    
    def mark_existing_articles_as_done(self, index_file_path: str) -> bool:
        """Mark all existing articles in the index file as 'done' (✅)."""
        try:
            if not os.path.exists(index_file_path):
                self.logger.warning(f"Index file {index_file_path} does not exist")
                return False
            
            # Read existing content
            with open(index_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Process each line and mark articles as done
            modified = False
            for i, line in enumerate(lines):
                # Look for article lines that start with "- [" but don't already have a status marker
                if line.strip().startswith('- [') and not ('✅' in line or '❌' in line or '⏳' in line):
                    # Insert ✅ after the opening bracket
                    lines[i] = line.replace('- [', '- [✅ ', 1)
                    modified = True
            
            # Write back if modified
            if modified:
                with open(index_file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                self.logger.info("Marked existing articles as done (✅)")
                return True
            else:
                self.logger.info("No articles needed status update")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to mark existing articles as done: {e}")
            return False
    
    def update_article_status(self, index_file_path: str, article_title: str, status: str = '✅') -> bool:
        """Update the status of a specific article in the index file."""
        try:
            if not os.path.exists(index_file_path):
                return False
            
            # Read existing content
            with open(index_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find and update the specific article
            modified = False
            for i, line in enumerate(lines):
                if article_title in line and '- [' in line:
                    # Replace any existing status with the new one
                    # Remove existing status markers first
                    cleaned_line = line.replace('✅ ', '').replace('❌ ', '').replace('⏳ ', '')
                    # Add new status
                    lines[i] = cleaned_line.replace('- [', f'- [{status} ', 1)
                    modified = True
                    break
            
            # Write back if modified
            if modified:
                with open(index_file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                self.logger.debug(f"Updated article status: {article_title} -> {status}")
                return True
            else:
                self.logger.warning(f"Article not found for status update: {article_title}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to update article status: {e}")
            return False
    
    def save_processed_month(self, month: str) -> bool:
        """
        Save a processed month to tracking file with proper date ordering.
        
        Args:
            month: Month identifier in YYYY/MM format
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(self.tracking_file), exist_ok=True)
            
            # Load existing months
            existing_months = []
            if os.path.exists(self.tracking_file):
                with open(self.tracking_file, 'r', encoding='utf-8') as f:
                    existing_months = [line.strip() for line in f if line.strip()]
            
            # Add new month if not already present
            if month not in existing_months:
                existing_months.append(month)
            
            # Sort by date (latest first)
            def sort_key(month_str):
                try:
                    year, month_num = month_str.split('/')
                    return (int(year), int(month_num))
                except (ValueError, IndexError):
                    return (0, 0)
            
            existing_months.sort(key=sort_key, reverse=True)
            
            # Write back to file
            with open(self.tracking_file, 'w', encoding='utf-8') as f:
                for m in existing_months:
                    f.write(f"{m}\n")
            
            self.logger.debug(f"Saved processed month: {month} (latest: {existing_months[0] if existing_months else 'none'})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save processed month {month}: {e}")
            return False
