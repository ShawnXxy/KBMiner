# coding: utf-8
"""
Base crawler class providing common functionality for all crawlers.
"""
import os
import re
import urllib.request
import urllib.parse
import logging
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class BaseCrawler(ABC):
    """
    Abstract base class for all web crawlers.
    
    Provides common functionality like URL fetching, file operations,
    and logging while enforcing implementation of crawler-specific methods.
    """
    
    def __init__(self, name: str, base_url: str, output_dir: str):
        """
        Initialize the base crawler.
        
        Args:
            name: Name of the crawler for logging
            base_url: Base URL for the website to crawl
            output_dir: Directory to save crawled content
        """
        self.name = name
        self.base_url = base_url
        self.output_dir = output_dir
        self._setup_logging()
        self._ensure_output_directory()
    
    def _setup_logging(self) -> None:
        """Set up logging configuration for the crawler."""
        self.logger = logging.getLogger(f"crawler.{self.name}")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _ensure_output_directory(self) -> None:
        """Ensure the output directory exists."""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            self.logger.info(f"Output directory ready: {self.output_dir}")
        except Exception as e:
            self.logger.error(f"Failed to create output directory {self.output_dir}: {e}")
            raise
    
    def fetch_page_content(self, url: str) -> str:
        """
        Fetch and decode webpage content.
        
        Args:
            url: URL to fetch
            
        Returns:
            Decoded webpage content as string
            
        Raises:
            Exception: If unable to fetch or decode content
        """
        try:
            # Properly encode the URL to handle special characters
            encoded_url = urllib.parse.quote(url, safe=':/?#[]@!$&\'()*+,;=')
            self.logger.debug(f"Fetching: {encoded_url}")
            
            response = urllib.request.urlopen(encoded_url)
            content = response.read().decode('utf-8')
            
            self.logger.debug(f"Successfully fetched {len(content)} characters from {url}")
            return content
            
        except Exception as e:
            self.logger.error(f"Failed to fetch content from {url}: {e}")
            raise
    
    def sanitize_filename(self, filename: str, max_length: int = 100) -> str:
        """
        Sanitize filename by removing invalid characters and limiting length.
        
        Args:
            filename: Original filename
            max_length: Maximum allowed length
            
        Returns:
            Sanitized filename safe for filesystem
        """
        # Remove or replace invalid characters for Windows filesystem
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Replace multiple spaces with single space and strip
        filename = re.sub(r'\s+', ' ', filename).strip()
        
        # Limit filename length
        if len(filename) > max_length:
            filename = filename[:max_length].rsplit(' ', 1)[0]  # Cut at word boundary
        
        return filename
    
    def save_content_to_file(self, content: str, filepath: str) -> bool:
        """
        Save content to a file with proper error handling.
        
        Args:
            content: Content to save
            filepath: Full path to the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.debug(f"Saved content to: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save content to {filepath}: {e}")
            return False
    
    def load_processed_items(self, tracking_file: str) -> set:
        """
        Load previously processed items from tracking file.
        
        Args:
            tracking_file: Path to tracking file
            
        Returns:
            Set of processed item identifiers
        """
        if not os.path.exists(tracking_file):
            self.logger.info(f"No tracking file found: {tracking_file}")
            return set()
        
        try:
            with open(tracking_file, 'r', encoding='utf-8') as f:
                items = {line.strip() for line in f if line.strip()}
            
            self.logger.info(f"Loaded {len(items)} processed items from {tracking_file}")
            return items
            
        except Exception as e:
            self.logger.error(f"Failed to load tracking file {tracking_file}: {e}")
            return set()
    
    def save_processed_item(self, tracking_file: str, item: str) -> bool:
        """
        Save a processed item to tracking file.
        
        Args:
            tracking_file: Path to tracking file
            item: Item identifier to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(tracking_file), exist_ok=True)
            
            with open(tracking_file, 'a', encoding='utf-8') as f:
                f.write(f"{item}\n")
            
            self.logger.debug(f"Saved processed item: {item}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save to tracking file {tracking_file}: {e}")
            return False
    
    @abstractmethod
    def crawl(self, **kwargs) -> dict:
        """
        Main crawling method to be implemented by subclasses.
        
        Args:
            **kwargs: Crawler-specific parameters
            
        Returns:
            Dictionary with crawling results and statistics
        """
        pass
    
    @abstractmethod
    def should_include_content(self, title: str, **kwargs) -> bool:
        """
        Determine if content should be included based on filtering rules.
        
        Args:
            title: Content title to check
            **kwargs: Additional parameters for filtering
            
        Returns:
            True if content should be included, False otherwise
        """
        pass
    
    def get_statistics(self) -> dict:
        """
        Get crawler statistics.
        
        Returns:
            Dictionary with crawler statistics
        """
        return {
            'name': self.name,
            'base_url': self.base_url,
            'output_dir': self.output_dir
        }
