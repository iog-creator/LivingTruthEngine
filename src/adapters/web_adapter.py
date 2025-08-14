"""
Web Adapter for Phase 9.5.0

Production-ready web adapter with deduplication, crawl depth management,
and integration with existing web fetcher implementation.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

from .base_adapter import BaseAdapter, DocumentLike

# Import existing web fetcher
try:
    from ..ingestion_general.fetchers.web_fetcher import WebFetcher as LegacyWebFetcher
    LEGACY_WEB_AVAILABLE = True
except ImportError:
    LEGACY_WEB_AVAILABLE = False
    logging.warning("Legacy web fetcher not available")

logger = logging.getLogger(__name__)

class WebAdapter(BaseAdapter):
    """Web adapter with deduplication and crawl depth management."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize web adapter."""
        super().__init__(config)
        
        # Initialize legacy fetcher if available
        if LEGACY_WEB_AVAILABLE:
            self.legacy_fetcher = LegacyWebFetcher(config)
        else:
            self.legacy_fetcher = None
            logger.warning("Legacy web fetcher not available, using mock implementation")
        
        # Web-specific configuration
        self.default_max_depth = config.get("web_default_max_depth", 2)
        self.default_js_render = config.get("web_default_js_render", False)
        self.request_timeout = config.get("web_request_timeout", 30)
        self.max_pages_per_run = config.get("web_max_pages_per_run", 50)
        
    @property
    def source_type(self) -> str:
        """Return web source type."""
        return "web"
    
    async def fetch_documents(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch web documents using legacy fetcher or mock implementation."""
        if self.legacy_fetcher:
            return await self._fetch_with_legacy_fetcher(params)
        else:
            return await self._fetch_mock_documents(params)
    
    async def _fetch_with_legacy_fetcher(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch documents using internal web fetcher with fallback."""
        try:
            # Extract parameters
            urls = params.get("urls", [])
            if not urls:
                raise ValueError("urls list is required for web adapter")
            
            max_depth = params.get("max_depth", self.default_max_depth)
            js_render = params.get("js_render", self.default_js_render)
            crawl_depth = params.get("crawl_depth", 0)
            
            documents = []
            for url in urls:
                try:
                    # Try internal web fetcher first (primary path)
                    internal_docs = await self._extract_web_internal(url, max_depth, js_render)
                    if internal_docs:
                        documents.extend(internal_docs)
                        logger.info(f"Internal web extraction successful for {url}: {len(internal_docs)} documents")
                        continue
                    
                    # Fallback to enhanced extraction (secondary fallback)
                    logger.warning(f"Internal extraction failed for {url}, trying enhanced extraction")
                    enhanced_doc = await self._extract_web_enhanced(url, js_render)
                    if enhanced_doc:
                        documents.append(enhanced_doc)
                        logger.info(f"Enhanced web extraction successful for {url}")
                        continue
                    
                    # Final fallback to legacy fetcher
                    logger.warning(f"Enhanced extraction failed for {url}, falling back to legacy fetcher")
                    raw_docs = self.legacy_fetcher.fetch_url(
                        url,
                        crawl_depth=crawl_depth,
                        max_depth=max_depth
                    )
                    
                    for raw_doc in raw_docs:
                        try:
                            # Create document
                            doc = {
                                "id": raw_doc.get("id", f"web_{hash(raw_doc.get('url', '')) % 10000}"),
                                "source": "web",
                                "url": raw_doc.get("url", raw_doc.get("uri", "")),
                                "title": raw_doc.get("title", "Untitled Web Page"),
                                "text": raw_doc.get("text", raw_doc.get("content", "")),
                                "metadata": {
                                    "domain": raw_doc.get("meta", {}).get("domain", ""),
                                    "content_type": raw_doc.get("meta", {}).get("content_type", ""),
                                    "crawl_depth": crawl_depth,
                                    "js_render": js_render,
                                    "extraction_method": raw_doc.get("meta", {}).get("extraction_method", "legacy_fallback")
                                }
                            }
                            documents.append(doc)
                            
                        except Exception as e:
                            logger.error(f"Error processing web document: {e}")
                            continue
                    
                except Exception as e:
                    logger.error(f"Error processing URL {url}: {e}")
                    continue
            
            return documents
            
        except Exception as e:
            logger.error(f"Error fetching web documents: {e}")
            raise
    
    async def _extract_web_internal(self, url: str, max_depth: int, js_render: bool) -> List[Dict[str, Any]]:
        """Extract web content using internal web fetcher (primary path)."""
        try:
            # Use internal WebFetcher (proven ingestion pipeline)
            # Note: WebFetcher.fetch_url returns List[Dict[str, Any]]
            raw_docs = self.legacy_fetcher.fetch_url(
                url=url,
                crawl_depth=0,  # Start with single page
                max_depth=max_depth
            )
            
            documents = []
            for raw_doc in raw_docs:
                try:
                    # Convert internal format to adapter format
                    doc = {
                        "id": raw_doc.get("id", f"web_internal_{hash(raw_doc.get('uri', url)) % 10000}"),
                        "source": "web",
                        "url": raw_doc.get("uri", url),
                        "title": raw_doc.get("title", "Untitled Web Page"),
                        "text": raw_doc.get("text", ""),
                        "metadata": {
                            "domain": raw_doc.get("meta", {}).get("domain", ""),
                            "content_type": raw_doc.get("meta", {}).get("content_type", "text/html"),
                            "crawl_depth": 0,
                            "js_render": js_render,
                            "extraction_method": "internal_web_fetcher",
                            "links_count": raw_doc.get("meta", {}).get("links_count", 0),
                            "extraction_method_detail": raw_doc.get("meta", {}).get("extraction_method", "unknown")
                        }
                    }
                    documents.append(doc)
                    
                except Exception as e:
                    logger.error(f"Error processing internal web document: {e}")
                    continue
            
            return documents
            
        except Exception as e:
            logger.debug(f"Internal web extraction failed for {url}: {e}")
            return []
    
    async def _extract_web_enhanced(self, url: str, js_render: bool) -> Optional[Dict[str, Any]]:
        """Enhanced web extraction using Trafilatura with optional JS rendering."""
        try:
            import requests
            from urllib.parse import urlparse
            from bs4 import BeautifulSoup
            
            # Fetch content
            headers = {
                "User-Agent": "LivingTruthEngine/1.0 (Phase 9.5.0a Enhanced)"
            }
            
            response = requests.get(url, headers=headers, timeout=self.request_timeout)
            response.raise_for_status()
            
            html_content = response.text
            
            # Try Trafilatura first (best for article extraction)
            try:
                import trafilatura
                
                # Extract text using Trafilatura
                extracted_text = trafilatura.extract(html_content, include_formatting=True)
                
                if extracted_text and len(extracted_text.strip()) >= 100:
                    # Extract metadata
                    metadata = trafilatura.extract_metadata(html_content)
                    
                    return {
                        "id": f"web_enhanced_{hash(url) % 10000}",
                        "source": "web",
                        "url": url,
                        "title": metadata.get("title", urlparse(url).netloc),
                        "text": extracted_text,
                        "metadata": {
                            "domain": urlparse(url).netloc,
                            "content_type": "text/html",
                            "crawl_depth": 0,
                            "js_render": js_render,
                            "extraction_method": "trafilatura_enhanced",
                            "author": metadata.get("author"),
                            "date": metadata.get("date"),
                            "categories": metadata.get("categories"),
                            "tags": metadata.get("tags"),
                            "char_count": len(extracted_text)
                        }
                    }
            except Exception as e:
                logger.debug(f"Trafilatura extraction failed for {url}: {e}")
            
            # Try readability-lxml as fallback
            try:
                from readability import Document
                
                doc = Document(html_content)
                extracted_text = doc.summary()
                
                if extracted_text and len(extracted_text.strip()) >= 100:
                    # Clean HTML tags
                    soup = BeautifulSoup(extracted_text, 'html.parser')
                    clean_text = soup.get_text()
                    
                    return {
                        "id": f"web_enhanced_{hash(url) % 10000}",
                        "source": "web",
                        "url": url,
                        "title": doc.title() or urlparse(url).netloc,
                        "text": clean_text,
                        "metadata": {
                            "domain": urlparse(url).netloc,
                            "content_type": "text/html",
                            "crawl_depth": 0,
                            "js_render": js_render,
                            "extraction_method": "readability_enhanced",
                            "char_count": len(clean_text)
                        }
                    }
            except Exception as e:
                logger.debug(f"readability-lxml extraction failed for {url}: {e}")
            
            # If JS rendering is requested, try with Playwright
            if js_render:
                try:
                    js_doc = await self._extract_web_js(url)
                    if js_doc:
                        return js_doc
                except Exception as e:
                    logger.debug(f"JS rendering failed for {url}: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Enhanced web extraction failed for {url}: {e}")
            return None
    
    async def _extract_web_js(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract web content with JavaScript rendering using Playwright."""
        try:
            import asyncio
            from playwright.async_api import async_playwright
            from urllib.parse import urlparse
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Set user agent
                await page.set_extra_http_headers({
                    "User-Agent": "LivingTruthEngine/1.0 (Phase 9.5.0a JS Enhanced)"
                })
                
                # Navigate to page and wait for content to load
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Wait a bit more for dynamic content
                await page.wait_for_timeout(2000)
                
                # Extract content
                title = await page.title()
                content = await page.content()
                
                await browser.close()
                
                # Try Trafilatura on the rendered content
                try:
                    import trafilatura
                    extracted_text = trafilatura.extract(content, include_formatting=True)
                    
                    if extracted_text and len(extracted_text.strip()) >= 100:
                        metadata = trafilatura.extract_metadata(content)
                        
                        return {
                            "id": f"web_js_{hash(url) % 10000}",
                            "source": "web",
                            "url": url,
                            "title": metadata.get("title", title),
                            "text": extracted_text,
                            "metadata": {
                                "domain": urlparse(url).netloc,
                                "content_type": "text/html",
                                "crawl_depth": 0,
                                "js_render": True,
                                "extraction_method": "trafilatura_js_rendered",
                                "author": metadata.get("author"),
                                "date": metadata.get("date"),
                                "char_count": len(extracted_text)
                            }
                        }
                except Exception as e:
                    logger.debug(f"Trafilatura on JS content failed for {url}: {e}")
                
                # Fallback to basic text extraction
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    if len(text.strip()) >= 100:
                        return {
                            "id": f"web_js_{hash(url) % 10000}",
                            "source": "web",
                            "url": url,
                            "title": title,
                            "text": text,
                            "metadata": {
                                "domain": urlparse(url).netloc,
                                "content_type": "text/html",
                                "crawl_depth": 0,
                                "js_render": True,
                                "extraction_method": "beautifulsoup_js_rendered",
                                "char_count": len(text)
                            }
                        }
                except Exception as e:
                    logger.debug(f"BeautifulSoup on JS content failed for {url}: {e}")
                
                return None
                
        except Exception as e:
            logger.error(f"JS rendering extraction failed for {url}: {e}")
            return None
    
    async def _fetch_mock_documents(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch mock web documents for testing."""
        import uuid
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        urls = params.get("urls", ["https://example.com"])
        max_depth = params.get("max_depth", self.default_max_depth)
        js_render = params.get("js_render", self.default_js_render)
        
        documents = []
        for i, url in enumerate(urls[:3]):  # Max 3 mock documents
            try:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc or "example.com"
                
                doc = {
                    "id": f"web_mock_{uuid.uuid4().hex[:8]}",
                    "source": "web",
                    "url": url,
                    "title": f"Mock Web Page {i+1} from {domain}",
                    "text": f"This is mock content from {domain}. It contains sample text that would normally be extracted from a web page using {'JavaScript rendering' if js_render else 'static HTML parsing'} with crawl depth {max_depth}.",
                    "metadata": {
                        "domain": domain,
                        "content_type": "text/html",
                        "crawl_depth": 0,
                        "js_render": js_render,
                        "extraction_method": "mock"
                    }
                }
                documents.append(doc)
                
            except Exception as e:
                logger.error(f"Error creating mock web document for {url}: {e}")
                continue
        
        return documents
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format and allowed domains."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Check against allowed domains if configured
            allowed_domains = self.config.get("allowed_domains", [])
            if allowed_domains:
                return any(domain in parsed.netloc for domain in allowed_domains)
            
            return True
        except Exception:
            return False
    
    def _extract_domain(self, url: str) -> Optional[str]:
        """Extract domain from URL."""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return None
