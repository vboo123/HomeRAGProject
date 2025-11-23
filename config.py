"""Configuration settings for the RAG pipeline."""

from dataclasses import dataclass


@dataclass
class CrawlerConfig:
    """
    Configuration for HTML crawler behavior.
    
    Attributes:
        stay_in_domain: If True, crawler only follows links within the same domain
        max_depth: Maximum depth to crawl (0 = only the starting page)
        follow_links: If True, crawler follows links on pages
        max_links_per_page: Maximum number of links to follow per page
    """
    stay_in_domain: bool = True
    max_depth: int = 2
    follow_links: bool = True
    max_links_per_page: int = 10


