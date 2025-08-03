# coding: utf-8
"""
MySQL crawler that coordinates both ActionTech and Alibaba crawlers.
"""
import logging
from typing import Dict, Any, Optional

from .actiontech_crawler import ActionTechCrawler
from .ali_crawler import AliCrawler


class MySQLCrawler:
    """
    Meta-crawler that coordinates MySQL-related crawling from multiple sources.
    
    This class manages both ActionTech and Alibaba crawlers to provide
    a unified interface for MySQL content crawling.
    """
    
    def __init__(self):
        """Initialize MySQL crawler with sub-crawlers."""
        self.logger = logging.getLogger("crawler.MySQL")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - MySQL - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # Initialize sub-crawlers
        self.actiontech_crawler = ActionTechCrawler()
        self.ali_crawler = AliCrawler()
        
        self.logger.info("MySQL crawler initialized with ActionTech and Alibaba sources")
    
    def crawl(self, sources: Optional[list] = None, **kwargs) -> Dict[str, Any]:
        """
        Crawl MySQL content from specified sources.
        
        Args:
            sources: List of sources to crawl ('actiontech', 'alibaba', or 'all')
            **kwargs: Additional parameters passed to individual crawlers
            
        Returns:
            Dictionary with results from all crawled sources
        """
        if sources is None:
            sources = ['actiontech', 'alibaba']
        elif 'all' in sources:
            sources = ['actiontech', 'alibaba']
        
        results = {}
        
        # Crawl ActionTech if requested
        if 'actiontech' in sources:
            try:
                self.logger.info("Starting ActionTech crawl...")
                actiontech_results = self.actiontech_crawler.crawl(**kwargs)
                results['actiontech'] = actiontech_results
                self.logger.info("ActionTech crawl completed successfully")
            except Exception as e:
                self.logger.error(f"ActionTech crawl failed: {e}")
                results['actiontech'] = {'error': str(e)}
        
        # Crawl Alibaba if requested
        if 'alibaba' in sources:
            try:
                self.logger.info("Starting Alibaba crawl...")
                alibaba_results = self.ali_crawler.crawl(**kwargs)
                results['alibaba'] = alibaba_results
                self.logger.info("Alibaba crawl completed successfully")
            except Exception as e:
                self.logger.error(f"Alibaba crawl failed: {e}")
                results['alibaba'] = {'error': str(e)}
        
        # Generate summary
        total_articles = 0
        for source, source_results in results.items():
            if 'error' not in source_results:
                articles_processed = source_results.get('articles_processed', 0)
                filtered_articles = source_results.get('filtered_articles', 0)
                articles = articles_processed or filtered_articles
                total_articles += articles
        
        results['summary'] = {
            'total_sources': len([s for s in results if 'error' not in results[s]]),
            'total_articles': total_articles,
            'sources_crawled': list(results.keys())
        }
        
        self.logger.info(f"MySQL crawl completed: {total_articles} articles from {len(results)-1} sources")
        return results
    
    def get_available_sources(self) -> list:
        """Get list of available crawler sources."""
        return ['actiontech', 'alibaba']
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics from all crawlers."""
        return {
            'actiontech': self.actiontech_crawler.get_statistics(),
            'alibaba': self.ali_crawler.get_statistics()
        }
