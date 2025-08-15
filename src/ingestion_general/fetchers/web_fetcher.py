"""
Web Fetcher for Phase 8: Real-data ingestion
Handles web content fetching with domain controls and crawl depth management
"""

import logging
import requests
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Any, Set
import trafilatura
from readability import Document
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

class WebFetcher:
    """Web content fetcher with domain controls and crawl depth management"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize web fetcher with configuration"""
        self.config = config
        self.user_agent = config.get("user_agent", "LivingTruthEngine/1.0 (Phase 8)")
        self.request_timeout = config.get("request_timeout", 30)
        self.max_redirects = config.get("max_redirects", 5)
        self.content_type_whitelist = config.get("content_type_whitelist", [
            "text/html", "application/pdf", "text/plain"
        ])
        self.allow_domains = config.get("allow_domains", ["youtube.com", "youtu.be"])
        self.deny_domains = config.get("deny_domains", [])
        self.max_pages_per_run = config.get("max_pages_per_run", 50)
        self.max_pages_per_domain = config.get("max_pages_per_domain", 10)
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        self.session.max_redirects = self.max_redirects
        
    def fetch_url(
        self, 
        url: str, 
        crawl_depth: int = 0,
        max_depth: int = 3,
        visited_urls: Optional[Set[str]] = None,
        domain_counts: Optional[Dict[str, int]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch content from URL with optional crawling
        
        Args:
            url: URL to fetch
            crawl_depth: Current crawl depth
            max_depth: Maximum crawl depth
            visited_urls: Set of already visited URLs
            domain_counts: Count of pages fetched per domain
            
        Returns:
            List of document dictionaries
        """
        if visited_urls is None:
            visited_urls = set()
        if domain_counts is None:
            domain_counts = defaultdict(int)
            
        documents = []
        
        # Check if we've reached limits
        if len(visited_urls) >= self.max_pages_per_run:
            logger.info(f"Reached max pages per run limit ({self.max_pages_per_run})")
            return documents
            
        domain = urlparse(url).netloc
        if domain_counts[domain] >= self.max_pages_per_domain:
            logger.info(f"Reached max pages per domain limit for {domain} ({self.max_pages_per_domain})")
            return documents
            
        # Check domain allow/deny
        if not self._is_domain_allowed(domain):
            logger.warning(f"Domain {domain} not allowed")
            return documents
            
        # Check if already visited
        if url in visited_urls:
            logger.debug(f"URL already visited: {url}")
            return documents
            
        # Fetch the page
        try:
            logger.info(f"Fetching {url} at depth {crawl_depth}")
            document = self._fetch_single_url(url)
            if document:
                document["crawl_depth"] = crawl_depth
                document["crawl_parent"] = None  # Will be set by caller
                documents.append(document)
                visited_urls.add(url)
                domain_counts[domain] += 1
                
                # Crawl to next depth if allowed
                if crawl_depth < max_depth:
                    child_docs = self._crawl_links(
                        url, document.get("links", []), 
                        crawl_depth + 1, max_depth, 
                        visited_urls, domain_counts
                    )
                    documents.extend(child_docs)
                    
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            
        return documents
    
    def _fetch_single_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch content from a single URL"""
        try:
            response = self.session.get(url, timeout=self.request_timeout)
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "").lower()
            
            # Check content type
            if not any(ct in content_type for ct in self.content_type_whitelist):
                logger.warning(f"Content type {content_type} not in whitelist for {url}")
                return None
                
            # Extract text based on content type
            if "text/html" in content_type:
                return self._extract_html_content(url, response.text)
            elif "application/pdf" in content_type:
                return self._extract_pdf_content(url, response.content)
            elif "text/plain" in content_type:
                return self._extract_text_content(url, response.text)
            else:
                logger.warning(f"Unsupported content type {content_type} for {url}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None
    
    def _extract_html_content(self, url: str, html_content: str) -> Dict[str, Any]:
        """Extract text content from HTML"""
        try:
            # Try trafilatura first (better for article extraction)
            extracted_text = trafilatura.extract(html_content)
            
            if not extracted_text:
                # Fallback to readability-lxml
                doc = Document(html_content)
                extracted_text = doc.summary()
                
            # Extract links for crawling
            links = self._extract_links(html_content, url)
            
            return {
                "source_type": "web",
                "uri": url,
                "title": self._extract_title(html_content),
                "text": extracted_text or html_content[:1000],  # Fallback to first 1000 chars
                "meta": {
                    "content_type": "text/html",
                    "extraction_method": "trafilatura" if extracted_text else "readability",
                    "links_count": len(links)
                },
                "links": links
            }
            
        except Exception as e:
            logger.error(f"Error extracting HTML content from {url}: {e}")
            return {
                "source_type": "web",
                "uri": url,
                "title": f"Error extracting content from {url}",
                "text": f"[Error extracting content: {e}]",
                "meta": {"content_type": "text/html", "extraction_method": "error"}
            }
    
    def _extract_pdf_content(self, url: str, pdf_content: bytes) -> Dict[str, Any]:
        """Extract text content from PDF"""
        try:
            # For now, return a placeholder
            # Task: PDF Processing - See TASKS.md for details
            return {
                "source_type": "web",
                "uri": url,
                "title": f"PDF Document: {url}",
                "text": f"[PDF content extraction not yet implemented for {url}]",
                "meta": {
                    "content_type": "application/pdf",
                    "extraction_method": "placeholder",
                    "size_bytes": len(pdf_content)
                }
            }
        except Exception as e:
            logger.error(f"Error extracting PDF content from {url}: {e}")
            return {
                "source_type": "web",
                "uri": url,
                "title": f"Error extracting PDF from {url}",
                "text": f"[Error extracting PDF: {e}]",
                "meta": {"content_type": "application/pdf", "extraction_method": "error"}
            }
    
    def _extract_text_content(self, url: str, text_content: str) -> Dict[str, Any]:
        """Extract content from plain text"""
        return {
            "source_type": "web",
            "uri": url,
            "title": f"Text Document: {url}",
            "text": text_content,
            "meta": {
                "content_type": "text/plain",
                "extraction_method": "direct",
                "size_chars": len(text_content)
            }
        }
    
    def _extract_title(self, html_content: str) -> str:
        """Extract title from HTML"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            return title_tag.get_text().strip() if title_tag else "Untitled"
        except Exception:
            return "Untitled"
    
    def _extract_links(self, html_content: str, base_url: str) -> List[str]:
        """Extract links from HTML for crawling"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(base_url, href)
                
                # Only include HTTP/HTTPS links
                if absolute_url.startswith(('http://', 'https://')):
                    links.append(absolute_url)
                    
            return links[:20]  # Limit to first 20 links
            
        except Exception as e:
            logger.warning(f"Error extracting links from {base_url}: {e}")
            return []
    
    def _crawl_links(
        self, 
        parent_url: str, 
        links: List[str], 
        crawl_depth: int, 
        max_depth: int,
        visited_urls: Set[str],
        domain_counts: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """Crawl links from a page"""
        documents = []
        
        for link in links:
            # Check limits
            if len(visited_urls) >= self.max_pages_per_run:
                break
                
            domain = urlparse(link).netloc
            if domain_counts[domain] >= self.max_pages_per_domain:
                continue
                
            # Check if already visited
            if link in visited_urls:
                continue
                
            # Check domain allow/deny
            if not self._is_domain_allowed(domain):
                continue
                
            try:
                logger.debug(f"Crawling link {link} at depth {crawl_depth}")
                document = self._fetch_single_url(link)
                if document:
                    document["crawl_depth"] = crawl_depth
                    document["crawl_parent"] = parent_url
                    documents.append(document)
                    visited_urls.add(link)
                    domain_counts[domain] += 1
                    
                    # Add small delay to be respectful
                    time.sleep(0.1)
                    
            except Exception as e:
                logger.warning(f"Error crawling link {link}: {e}")
                
        return documents
    
    def _is_domain_allowed(self, domain: str) -> bool:
        """Check if domain is allowed based on allow/deny lists"""
        # Check deny list first
        for deny_domain in self.deny_domains:
            if deny_domain in domain:
                return False
                
        # Check allow list
        if not self.allow_domains:  # Empty allow list means all allowed
            return True
            
        for allow_domain in self.allow_domains:
            if allow_domain in domain:
                return True
                
        return False
    
    def close(self):
        """Close the session"""
        self.session.close()
