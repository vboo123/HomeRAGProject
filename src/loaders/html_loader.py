"""HTML loader implementation with basic web crawler functionality."""

from typing import List, Set, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

from .base_loader import AbstractDataLoader
from ..models.document import Document

# Import config from project root
# Note: This assumes config.py is at the project root level
try:
    from config import CrawlerConfig
except ImportError:
    # Fallback: create a simple config class if import fails
    from dataclasses import dataclass
    
    @dataclass
    class CrawlerConfig:
        stay_in_domain: bool = True
        max_depth: int = 2
        follow_links: bool = True
        max_links_per_page: int = 10


class HTMLLoader(AbstractDataLoader):
    """
    Loader for HTML content with basic web crawler functionality.
    
    Can crawl a single URL or follow links within the same domain.
    Extracts main content from HTML pages, discarding navigation and boilerplate.
    """
    
    def __init__(self, config: Optional[CrawlerConfig] = None):
        """
        Initialize the HTML loader.
        
        Args:
            config: CrawlerConfig object with settings for domain restriction,
                   max depth, etc. If None, uses default config.
        """
        self.config = config or CrawlerConfig()
        self.visited_urls: Set[str] = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def load(self, source_path: str) -> List[Document]:
        """
        Load HTML content from a URL or crawl multiple pages.
        
        Args:
            source_path: Starting URL to crawl
            
        Returns:
            List of Document objects, one per crawled page
            
        Raises:
            ValueError: If the URL is invalid or cannot be accessed
        """
        if not source_path.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL: {source_path}. Must start with http:// or https://")
        
        documents = []
        self.visited_urls.clear()
        
        # Parse the starting URL to get the base domain
        parsed_url = urlparse(source_path)
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Crawl starting from the source URL
        self._crawl_url(source_path, base_domain, documents, depth=0)
        
        if not documents:
            raise ValueError(f"No content extracted from {source_path}")
        
        return documents
    
    def _crawl_url(self, url: str, base_domain: str, documents: List[Document], depth: int):
        """
        Recursively crawl a URL and its links.
        
        Args:
            url: URL to crawl
            base_domain: Base domain to restrict crawling to
            documents: List to append extracted documents to
            depth: Current crawling depth
        """
        # Check depth limit
        if depth > self.config.max_depth:
            return
        
        # Check if already visited
        if url in self.visited_urls:
            return
        
        # Check domain restriction
        if self.config.stay_in_domain:
            parsed_url = urlparse(url)
            url_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
            if url_domain != base_domain:
                return
        
        try:
            # Fetch the page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract main content (remove scripts, styles, nav, footer, etc.)
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Get main content - try to find article, main, or body
            main_content = (
                soup.find('article') or
                soup.find('main') or
                soup.find('body') or
                soup
            )
            
            # Extract text
            content = main_content.get_text(separator='\n', strip=True)
            
            # Get title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else "Untitled"
            
            # Mark as visited
            self.visited_urls.add(url)
            
            # Extract metadata
            metadata = self.extract_metadata(
                url,
                title=title_text,
                depth=depth,
                content_length=len(content)
            )
            
            # Create document
            documents.append(Document(
                content=content,
                source_uri=url,
                doc_type="html",
                metadata=metadata
            ))
            
            # If we should follow links and haven't exceeded depth
            if self.config.follow_links and depth < self.config.max_depth:
                # Find all links on the page
                links = main_content.find_all('a', href=True)
                for link in links[:self.config.max_links_per_page]:  # Limit links per page
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    
                    # Recursively crawl (will check domain and visited in the method)
                    self._crawl_url(absolute_url, base_domain, documents, depth + 1)
                    
        except requests.RequestException as e:
            print(f"Warning: Could not fetch {url}: {str(e)}")
        except Exception as e:
            print(f"Warning: Error processing {url}: {str(e)}")
    
    def extract_metadata(self, source_path: str, **kwargs) -> dict:
        """Extract metadata from HTML source."""
        return {
            "source_path": source_path,
            **kwargs
        }

