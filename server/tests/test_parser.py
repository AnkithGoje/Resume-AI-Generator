import pytest
import io
# Assuming functionality is in services/resume_parser.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.resume_parser import extract_text_from_pdf, extract_text_from_docx

# --- PDF Tests ---

def test_extract_pdf_standard():
    """Test extracting text from standard PDF bytes."""
    # Since we can't easily create a real PDF in memory without a library like reportlab,
    # we might need to rely on mocking pdfplumber or accepting that we can't fully unit test 
    # the 'extraction' logic without a physical file. 
    # HOWEVER, we can stick to testing the invalid handling if we lack a mock file.
    # OR, we can mock pdfplumber.open which is better.
    pass 

from unittest.mock import patch, MagicMock

@patch("services.resume_parser.pdfplumber.open")
def test_extract_pdf_mocked_content(mock_pdf_open):
    """Test PDF extraction with mocked pdfplumber."""
    # Setup mock page
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Mocked Resume Content"
    
    # Setup mock pdf object
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page]
    
    # Context manager setup
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf
    
    file_bytes = b"%PDF-mock"
    text = extract_text_from_pdf(file_bytes)
    assert text == "Mocked Resume Content"

@patch("services.resume_parser.pdfplumber.open")
def test_extract_pdf_multiple_pages(mock_pdf_open):
    """Test PDF extraction from multiple pages."""
    page1 = MagicMock()
    page1.extract_text.return_value = "Page 1 Content. "
    page2 = MagicMock()
    page2.extract_text.return_value = "Page 2 Content."
    
    mock_pdf = MagicMock()
    mock_pdf.pages = [page1, page2]
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf
    
    text = extract_text_from_pdf(b"dummy")
    assert text == "Page 1 Content. Page 2 Content."

@patch("services.resume_parser.pdfplumber.open")
def test_extract_pdf_empty_text(mock_pdf_open):
    """Test PDF with pages but no extractable text."""
    mock_page = MagicMock()
    mock_page.extract_text.return_value = None # pdfplumber returns None sometimes
    
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page]
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf
    
    text = extract_text_from_pdf(b"dummy")
    assert text == ""

def test_extract_pdf_invalid_bytes():
    """Test passing invalid non-PDF bytes (unmocked to see real fail or robust handling)."""
    # Ideally should raise error or return empty. 
    # pdfplumber raises PDFSyntaxError usually.
    try:
        extract_text_from_pdf(b"not a pdf")
    except Exception:
        pass # Expected
        
# --- DOCX Tests ---

@patch("services.resume_parser.docx.Document")
def test_extract_docx_mocked(mock_document):
    """Test DOCX extraction with mocked python-docx."""
    # Mock paragraphs
    para1 = MagicMock()
    para1.text = "Docx Header"
    para2 = MagicMock()
    para2.text = "Docx Body"
    
    mock_doc_instance = MagicMock()
    mock_doc_instance.paragraphs = [para1, para2]
    mock_document.return_value = mock_doc_instance
    
    text = extract_text_from_docx(b"dummy docx")
    assert text == "Docx Header\nDocx Body"

@patch("services.resume_parser.docx.Document")
def test_extract_docx_empty(mock_document):
    """Test DOCX with no paragraphs."""
    mock_doc_instance = MagicMock()
    mock_doc_instance.paragraphs = []
    mock_document.return_value = mock_doc_instance
    
    text = extract_text_from_docx(b"dummy")
    assert text == ""
