#!/usr/bin/env python3
# coding: utf-8
"""
MyKBMiner - Knowledge Base Mining Tool

A unified command-line interface for crawling technical content from various sources.
Currently supports MySQL-related content from ActionTech and Alibaba sources.
"""
import sys
import argparse
import logging
from typing import Dict, Any

from crawlers import MySQLCrawler


def setup_logging(level: str = "INFO") -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog='miner',
        description='MyKBMiner - Knowledge Base Mining Tool for Technical Content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  miner --source mysql                    # Crawl all MySQL sources
  miner --source MySQL --incremental     # Incremental MySQL crawl
  miner --source mysql --download         # Crawl and download content
  miner --source mysql --test             # Test crawl with sample data
  
Supported Sources:
  MySQL - Crawls ActionTech and Alibaba database content
        """
    )
    
    # Main arguments
    parser.add_argument(
        '--source', '-s',
        type=str,
        required=True,
        choices=['mysql', 'MySQL', 'MYSQL'],
        help='Source to crawl (case-insensitive). Currently supports: MySQL'
    )
    
    # Crawling mode options
    parser.add_argument(
        '--incremental', '-i',
        action='store_true',
        help='Run incremental crawl (only process new content)'
    )
    
    parser.add_argument(
        '--full', '-f',
        action='store_true',
        help='Force full crawl (process all content, ignore existing)'
    )
    
    # Content options
    parser.add_argument(
        '--download', '-d',
        action='store_true',
        help='Download full article content in addition to creating index'
    )
    
    parser.add_argument(
        '--download-only',
        action='store_true',
        help='Only download content for existing articles (no new crawling)'
    )
    
    # Testing options
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Run in test mode with limited content for validation'
    )
    
    parser.add_argument(
        '--test-articles',
        action='store_true',
        help='Test article download functionality with sample articles'
    )
    
    # Output and logging options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Reduce output (WARNING level and above only)'
    )
    
    # Source-specific options
    parser.add_argument(
        '--sources',
        nargs='+',
        choices=['actiontech', 'alibaba', 'all'],
        default=['all'],
        help='Specific sources to crawl within the selected category'
    )
    
    return parser


def validate_arguments(args: argparse.Namespace) -> bool:
    """
    Validate command line arguments for consistency.
    
    Args:
        args: Parsed arguments
        
    Returns:
        True if arguments are valid, False otherwise
    """
    if args.full and args.incremental:
        print("Error: --full and --incremental options are mutually exclusive")
        return False
    
    if args.download_only and (args.incremental or args.full):
        print("Error: --download-only cannot be used with --incremental or --full")
        return False
    
    if args.verbose and args.quiet:
        print("Error: --verbose and --quiet options are mutually exclusive")
        return False
    
    return True


def determine_log_level(args: argparse.Namespace) -> str:
    """
    Determine appropriate logging level based on arguments.
    
    Args:
        args: Parsed arguments
        
    Returns:
        Logging level string
    """
    if args.verbose:
        return "DEBUG"
    elif args.quiet:
        return "WARNING"
    else:
        return "INFO"


def crawl_mysql_sources(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Crawl MySQL sources based on provided arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Dictionary with crawling results
    """
    crawler = MySQLCrawler()
    
    # Prepare crawler parameters
    crawler_params = {
        'incremental': args.incremental and not args.full,
        'download_content': args.download,
        'download_only': args.download_only,
        'test_articles': args.test_articles,
        'download_articles': args.download or args.test_articles
    }
    
    # If testing, limit to specific behavior
    if args.test:
        crawler_params['test_mode'] = True
        crawler_params['incremental'] = True  # Safer for testing
    
    # Determine which sources to crawl
    sources = args.sources if 'all' not in args.sources else ['actiontech', 'alibaba']
    
    return crawler.crawl(sources=sources, **crawler_params)


def print_results_summary(results: Dict[str, Any]) -> None:
    """
    Print a formatted summary of crawling results.
    
    Args:
        results: Dictionary with crawling results
    """
    print("\n" + "="*60)
    print("CRAWLING RESULTS SUMMARY")
    print("="*60)
    
    summary = results.get('summary', {})
    total_articles = summary.get('total_articles', 0)
    sources_count = summary.get('total_sources', 0)
    
    print(f"Total Articles Processed: {total_articles}")
    print(f"Sources Successfully Crawled: {sources_count}")
    print(f"Sources: {', '.join(summary.get('sources_crawled', []))}")
    
    # Print individual source results
    for source, source_results in results.items():
        if source == 'summary':
            continue
            
        print(f"\n{source.upper()} Results:")
        if 'error' in source_results:
            print(f"  ❌ Error: {source_results['error']}")
        else:
            articles = source_results.get('articles_processed', 0) or \
                      source_results.get('filtered_articles', 0)
            print(f"  ✅ Articles: {articles}")
            
            if 'markdown_file' in source_results:
                print(f"  📄 Output: {source_results['markdown_file']}")
            
            if 'articles_downloaded' in source_results:
                downloaded = source_results['articles_downloaded']
                print(f"  📥 Downloaded: {downloaded}")
    
    print("\n" + "="*60)


def main() -> int:
    """
    Main entry point for the miner application.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Parse command line arguments
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Validate arguments
        if not validate_arguments(args):
            return 1
        
        # Set up logging
        log_level = determine_log_level(args)
        setup_logging(log_level)
        
        logger = logging.getLogger("miner")
        logger.info("Starting MyKBMiner...")
        logger.debug(f"Arguments: {args}")
        
        # Route to appropriate crawler based on source
        source_normalized = args.source.lower()
        
        if source_normalized == 'mysql':
            results = crawl_mysql_sources(args)
        else:
            logger.error(f"Unsupported source: {args.source}")
            return 1
        
        # Print results summary
        print_results_summary(results)
        
        # Check if any source failed
        failed_sources = [s for s, r in results.items() 
                         if s != 'summary' and 'error' in r]
        
        if failed_sources:
            logger.warning(f"Some sources failed: {failed_sources}")
            return 1
        
        logger.info("MyKBMiner completed successfully")
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except Exception as e:
        logger = logging.getLogger("miner")
        logger.error(f"Unexpected error: {e}")
        if log_level == "DEBUG":
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
