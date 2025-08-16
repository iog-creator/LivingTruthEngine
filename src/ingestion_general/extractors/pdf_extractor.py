"""
PDF Extractor for Phase 8: Real-data ingestion
Handles PDF text extraction with OCR fallback and suspect detection
"""

import logging
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from typing import Dict, List, Optional, Any, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class PDFExtractor:
    """PDF text extraction with OCR fallback and suspect detection"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize PDF extractor with configuration"""
        self.config = config
        self.suspect_min_chars = config.get("suspect_min_chars", 800)
        self.auto_retry_attempts = config.get("auto_retry_attempts", 2)
        self.tesseract_langs = config.get("tesseract_langs", "eng")

        # Check if tesseract is available
        try:
            pytesseract.get_tesseract_version()
            self.tesseract_available = True
        except Exception:
            self.tesseract_available = False
            logger.warning("Tesseract not available, OCR features disabled")

    def extract_text(
        self, pdf_content: bytes, ocr_mode: str = "off", filename: str = "unknown.pdf"
    ) -> Dict[str, Any]:
        """
        Extract text from PDF with optional OCR

        Args:
            pdf_content: PDF file content as bytes
            ocr_mode: OCR mode (off|auto|manual|auto_retry)
            filename: Original filename for logging

        Returns:
            Dictionary with extracted text and metadata
        """
        logger.info(f"Extracting text from PDF: {filename}")

        try:
            # Try PyMuPDF text extraction first
            text_content, extraction_method = self._extract_text_pymupdf(pdf_content)

            # Check if text extraction was successful
            if len(text_content.strip()) >= self.suspect_min_chars:
                logger.info(
                    f"Successfully extracted {len(text_content)} characters from {filename}"  # noqa: E501
                )
                return {
                    "text": text_content,
                    "extraction_method": extraction_method,
                    "needs_ocr": False,
                    "ocr_attempts": 0,
                    "char_count": len(text_content),
                }

            # Text extraction yielded insufficient content
            logger.warning(
                f"Text extraction yielded only {len(text_content)} characters from {filename}"  # noqa: E501
            )

            # Handle OCR based on mode
            if ocr_mode == "off":
                return {
                    "text": text_content,
                    "extraction_method": extraction_method,
                    "needs_ocr": True,
                    "ocr_attempts": 0,
                    "char_count": len(text_content),
                }

            elif ocr_mode in ["auto", "auto_retry"]:
                # Try OCR automatically
                ocr_result = self._perform_ocr(
                    pdf_content, max_attempts=self.auto_retry_attempts
                )
                return {
                    "text": ocr_result["text"],
                    "extraction_method": "ocr",
                    "needs_ocr": False,
                    "ocr_attempts": ocr_result["attempts"],
                    "char_count": len(ocr_result["text"]),
                }

            elif ocr_mode == "manual":
                # Mark for manual OCR
                return {
                    "text": text_content,
                    "extraction_method": extraction_method,
                    "needs_ocr": True,
                    "ocr_attempts": 0,
                    "char_count": len(text_content),
                }

        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {e}")
            return {
                "text": f"[Error extracting PDF: {e}]",
                "extraction_method": "error",
                "needs_ocr": False,
                "ocr_attempts": 0,
                "char_count": 0,
            }

    def _extract_text_pymupdf(self, pdf_content: bytes) -> Tuple[str, str]:
        """Extract text using PyMuPDF"""
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            text_content = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += page.get_text()

            doc.close()

            return text_content.strip(), "pymupdf"

        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            return "", "error"

    def _perform_ocr(self, pdf_content: bytes, max_attempts: int = 2) -> Dict[str, Any]:
        """Perform OCR on PDF pages"""
        if not self.tesseract_available:
            logger.warning("Tesseract not available, cannot perform OCR")
            return {
                "text": "[OCR not available - Tesseract not installed]",
                "attempts": 0,
            }

        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            all_text = []
            total_attempts = 0

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)

                # Convert page to image
                mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")

                # Perform OCR with multiple attempts
                page_text = ""
                for attempt in range(max_attempts):
                    try:
                        # Convert bytes to PIL Image
                        img = Image.open(io.BytesIO(img_data))

                        # Configure tesseract
                        custom_config = f"-l {self.tesseract_langs} --oem 3 --psm 6"

                        # Perform OCR
                        page_text = pytesseract.image_to_string(
                            img, config=custom_config
                        )
                        total_attempts += 1

                        if page_text.strip():
                            break

                    except Exception as e:
                        logger.warning(
                            f"OCR attempt {attempt + 1} failed for page {page_num}: {e}"
                        )
                        total_attempts += 1

                if page_text.strip():
                    all_text.append(page_text.strip())

            doc.close()

            final_text = "\n\n".join(all_text)
            logger.info(
                f"OCR completed with {total_attempts} attempts, extracted {len(final_text)} characters"  # noqa: E501
            )

            return {"text": final_text, "attempts": total_attempts}

        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return {"text": f"[OCR failed: {e}]", "attempts": 0}

    def extract_text_from_file(
        self, file_path: str, ocr_mode: str = "off"
    ) -> Dict[str, Any]:
        """Extract text from PDF file"""
        try:
            with open(file_path, "rb") as f:
                pdf_content = f.read()

            return self.extract_text(pdf_content, ocr_mode, file_path)

        except Exception as e:
            logger.error(f"Error reading PDF file {file_path}: {e}")
            return {
                "text": f"[Error reading PDF file: {e}]",
                "extraction_method": "error",
                "needs_ocr": False,
                "ocr_attempts": 0,
                "char_count": 0,
            }

    def is_suspect_pdf(self, text_content: str) -> bool:
        """Check if PDF is suspect (insufficient text content)"""
        return len(text_content.strip()) < self.suspect_min_chars

    def get_pdf_info(self, pdf_content: bytes) -> Dict[str, Any]:
        """Get PDF metadata and information"""
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")

            info = {
                "page_count": len(doc),
                "metadata": doc.metadata,
                "file_size": len(pdf_content),
            }

            # Get page dimensions
            if len(doc) > 0:
                page = doc.load_page(0)
                rect = page.rect
                info["page_width"] = rect.width
                info["page_height"] = rect.height

            doc.close()
            return info

        except Exception as e:
            logger.error(f"Error getting PDF info: {e}")
            return {
                "page_count": 0,
                "metadata": {},
                "file_size": len(pdf_content),
                "error": str(e),
            }
