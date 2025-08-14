"""
PDF Adapter for Phase 9.5.0

Production-ready PDF adapter with deduplication, OCR support,
and integration with existing PDF extractor implementation.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path
from urllib.parse import urlparse

from .base_adapter import BaseAdapter, DocumentLike

# Import existing PDF extractor
try:
    from ..ingestion_general.extractors.pdf_extractor import PDFExtractor as LegacyPDFExtractor
    LEGACY_PDF_AVAILABLE = True
except ImportError:
    LEGACY_PDF_AVAILABLE = False
    logging.warning("Legacy PDF extractor not available")

logger = logging.getLogger(__name__)

class PDFAdapter(BaseAdapter):
    """PDF adapter with deduplication and OCR support."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize PDF adapter."""
        super().__init__(config)
        
        # Initialize legacy extractor if available
        if LEGACY_PDF_AVAILABLE:
            self.legacy_extractor = LegacyPDFExtractor(config)
        else:
            self.legacy_extractor = None
            logger.warning("Legacy PDF extractor not available, using mock implementation")
        
        # PDF-specific configuration
        self.default_ocr_required = config.get("pdf_default_ocr_required", True)
        self.ocr_auto_retry = config.get("pdf_ocr_auto_retry", True)
        self.max_pages_per_pdf = config.get("pdf_max_pages_per_pdf", 100)
        self.extraction_timeout = config.get("pdf_extraction_timeout", 120)
        
    @property
    def source_type(self) -> str:
        """Return PDF source type."""
        return "pdf"
    
    async def fetch_documents(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch PDF documents using legacy extractor or mock implementation."""
        if self.legacy_extractor:
            return await self._fetch_with_legacy_extractor(params)
        else:
            return await self._fetch_mock_documents(params)
    
    async def _fetch_with_legacy_extractor(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch documents using internal PDF extraction module with fallback."""
        try:
            # Extract parameters
            urls = params.get("urls", [])
            if not urls:
                raise ValueError("urls list is required for PDF adapter")
            
            ocr_required = params.get("ocr_required", self.default_ocr_required)
            auto_retry = params.get("auto_retry", self.ocr_auto_retry)
            
            documents = []
            for url in urls:
                try:
                    # Try internal PDF extraction module first (primary path)
                    internal_doc = await self._extract_pdf_internal(url, ocr_required)
                    if internal_doc:
                        documents.append(internal_doc)
                        logger.info(f"Internal PDF extraction successful for {url}")
                        continue
                    
                    # Fallback to enhanced extraction (secondary fallback)
                    logger.warning(f"Internal extraction failed for {url}, trying enhanced extraction")
                    enhanced_doc = await self._extract_pdf_enhanced(url, ocr_required)
                    if enhanced_doc:
                        documents.append(enhanced_doc)
                        logger.info(f"Enhanced PDF extraction successful for {url}")
                        continue
                    
                    # Final fallback to legacy extractor
                    logger.warning(f"Enhanced extraction failed for {url}, falling back to legacy extractor")
                    try:
                        # Download PDF content for legacy extractor
                        import requests
                        response = requests.get(url, timeout=self.extraction_timeout)
                        response.raise_for_status()
                        pdf_content = response.content
                        
                        # Use internal extract_text method
                        ocr_mode = "auto" if ocr_required else "off"
                        filename = Path(url).name or "document.pdf"
                        raw_doc = self.legacy_extractor.extract_text(
                            pdf_content=pdf_content,
                            ocr_mode=ocr_mode,
                            filename=filename
                        )
                        
                        # Convert to expected format
                        if raw_doc and raw_doc.get("text"):
                            raw_doc = {
                                "id": f"pdf_legacy_{hash(url) % 10000}",
                                "title": f"PDF Document: {filename}",
                                "text": raw_doc["text"],
                                "file_path": url,
                                "pages": 0,  # Not available from extract_text
                                "ocr_used": raw_doc.get("needs_ocr", False),
                                "extraction_method": raw_doc.get("extraction_method", "legacy_fallback"),
                                "file_size": len(pdf_content)
                            }
                        else:
                            raw_doc = None
                    except Exception as e:
                        logger.error(f"Legacy extractor failed for {url}: {e}")
                        raw_doc = None
                    
                    if raw_doc and raw_doc.get("text"):
                        # Create document
                        doc = {
                            "id": raw_doc.get("id", f"pdf_{hash(url) % 10000}"),
                            "source": "pdf",
                            "url": url,
                            "title": raw_doc.get("title", f"PDF Document: {Path(url).name}"),
                            "text": raw_doc.get("text", ""),
                            "metadata": {
                                "file_path": raw_doc.get("file_path", ""),
                                "pages": raw_doc.get("pages", 0),
                                "ocr_required": ocr_required,
                                "ocr_used": raw_doc.get("ocr_used", False),
                                "extraction_method": raw_doc.get("extraction_method", "legacy_fallback"),
                                "file_size": raw_doc.get("file_size", 0)
                            }
                        }
                        documents.append(doc)
                    else:
                        logger.warning(f"No text extracted from PDF: {url}")
                        
                except Exception as e:
                    logger.error(f"Error processing PDF {url}: {e}")
                    continue
            
            return documents
            
        except Exception as e:
            logger.error(f"Error fetching PDF documents: {e}")
            raise
    
    async def _extract_pdf_internal(self, url: str, ocr_required: bool) -> Optional[Dict[str, Any]]:
        """Extract PDF using internal PDF extraction module (primary path)."""
        try:
            import requests
            from pathlib import Path
            
            # Download PDF content
            response = requests.get(url, timeout=self.extraction_timeout)
            response.raise_for_status()
            pdf_content = response.content
            
            # Use internal PDFExtractor (proven ingestion pipeline)
            ocr_mode = "auto" if ocr_required else "off"
            filename = Path(url).name or "document.pdf"
            
            # Extract text using internal module
            result = self.legacy_extractor.extract_text(
                pdf_content=pdf_content,
                ocr_mode=ocr_mode,
                filename=filename
            )
            
            if result and result.get("text") and len(result["text"].strip()) >= 100:
                return {
                    "id": f"pdf_internal_{hash(url) % 10000}",
                    "source": "pdf",
                    "url": url,
                    "title": f"PDF Document: {filename}",
                    "text": result["text"],
                    "metadata": {
                        "file_path": url,
                        "pages": result.get("pages", 0),
                        "ocr_required": ocr_required,
                        "ocr_used": result.get("needs_ocr", False),
                        "extraction_method": "internal_pdf_extractor",
                        "file_size": len(pdf_content),
                        "char_count": len(result["text"]),
                        "extraction_method_detail": result.get("extraction_method", "unknown")
                    }
                }
            
            return None
            
        except Exception as e:
            logger.debug(f"Internal PDF extraction failed for {url}: {e}")
            return None
    
    async def _extract_pdf_enhanced(self, url: str, ocr_required: bool) -> Optional[Dict[str, Any]]:
        """Enhanced PDF extraction using internal modules."""
        try:
            import requests
            import tempfile
            import os
            from pathlib import Path
            
            # Download PDF content
            response = requests.get(url, timeout=self.extraction_timeout)
            response.raise_for_status()
            pdf_content = response.content
            
            # Try PyMuPDF first (fastest)
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(stream=pdf_content, filetype="pdf")
                text_content = ""
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text_content += page.get_text()
                
                doc.close()
                
                if len(text_content.strip()) >= 100:  # Minimum viable text
                    return {
                        "id": f"pdf_enhanced_{hash(url) % 10000}",
                        "source": "pdf",
                        "url": url,
                        "title": f"PDF Document: {Path(url).name}",
                        "text": text_content,
                        "metadata": {
                            "file_path": url,
                            "pages": len(doc),
                            "ocr_required": ocr_required,
                            "ocr_used": False,
                            "extraction_method": "pymupdf_enhanced",
                            "file_size": len(pdf_content),
                            "char_count": len(text_content)
                        }
                    }
            except Exception as e:
                logger.debug(f"PyMuPDF extraction failed for {url}: {e}")
            
            # Try pdfplumber as fallback (better for structured content)
            try:
                import pdfplumber
                import io
                
                with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                    text_content = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + "\n"
                    
                    if len(text_content.strip()) >= 100:
                        return {
                            "id": f"pdf_enhanced_{hash(url) % 10000}",
                            "source": "pdf",
                            "url": url,
                            "title": f"PDF Document: {Path(url).name}",
                            "text": text_content,
                            "metadata": {
                                "file_path": url,
                                "pages": len(pdf.pages),
                                "ocr_required": ocr_required,
                                "ocr_used": False,
                                "extraction_method": "pdfplumber_enhanced",
                                "file_size": len(pdf_content),
                                "char_count": len(text_content)
                            }
                        }
            except Exception as e:
                logger.debug(f"pdfplumber extraction failed for {url}: {e}")
            
            # If OCR is required, try OCR extraction
            if ocr_required:
                try:
                    ocr_doc = await self._extract_pdf_ocr(pdf_content, url)
                    if ocr_doc:
                        return ocr_doc
                except Exception as e:
                    logger.debug(f"OCR extraction failed for {url}: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Enhanced PDF extraction failed for {url}: {e}")
            return None
    
    async def _extract_pdf_ocr(self, pdf_content: bytes, url: str) -> Optional[Dict[str, Any]]:
        """Extract text from PDF using OCR."""
        try:
            import fitz  # PyMuPDF
            import pytesseract
            from PIL import Image
            import io
            
            # Check if tesseract is available
            try:
                pytesseract.get_tesseract_version()
            except Exception:
                logger.warning("Tesseract not available for OCR")
                return None
            
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            text_content = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Convert page to image
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Extract text using OCR
                page_text = pytesseract.image_to_string(img)
                text_content += page_text + "\n"
            
            doc.close()
            
            if len(text_content.strip()) >= 100:
                return {
                    "id": f"pdf_ocr_{hash(url) % 10000}",
                    "source": "pdf",
                    "url": url,
                    "title": f"PDF Document: {Path(url).name}",
                    "text": text_content,
                    "metadata": {
                        "file_path": url,
                        "pages": len(doc),
                        "ocr_required": True,
                        "ocr_used": True,
                        "extraction_method": "tesseract_ocr",
                        "file_size": len(pdf_content),
                        "char_count": len(text_content)
                    }
                }
            
            return None
            
        except Exception as e:
            logger.error(f"OCR extraction failed for {url}: {e}")
            return None
    
    async def _fetch_mock_documents(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch mock PDF documents for testing."""
        import uuid
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        urls = params.get("urls", ["https://example.com/sample.pdf"])
        ocr_required = params.get("ocr_required", self.default_ocr_required)
        
        documents = []
        for i, url in enumerate(urls[:3]):  # Max 3 mock documents
            try:
                filename = Path(url).name or f"document_{i+1}.pdf"
                
                doc = {
                    "id": f"pdf_mock_{uuid.uuid4().hex[:8]}",
                    "source": "pdf",
                    "url": url,
                    "title": f"Mock PDF Document: {filename}",
                    "text": f"This is mock content extracted from {filename}. It contains sample text that would normally be extracted from a PDF document using {'OCR processing' if ocr_required else 'direct text extraction'}.",
                    "metadata": {
                        "file_path": f"/tmp/mock_{filename}",
                        "pages": 5,
                        "ocr_required": ocr_required,
                        "ocr_used": ocr_required,
                        "extraction_method": "mock",
                        "file_size": 1024000
                    }
                }
                documents.append(doc)
                
            except Exception as e:
                logger.error(f"Error creating mock PDF document for {url}: {e}")
                continue
        
        return documents
    
    def _validate_pdf_url(self, url: str) -> bool:
        """Validate PDF URL format."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Check if it's a PDF file
            path = Path(parsed.path)
            if path.suffix.lower() != '.pdf':
                return False
            
            return True
        except Exception:
            return False
    
    def _extract_filename(self, url: str) -> Optional[str]:
        """Extract filename from PDF URL."""
        try:
            parsed = urlparse(url)
            path = Path(parsed.path)
            return path.name
        except Exception:
            return None
