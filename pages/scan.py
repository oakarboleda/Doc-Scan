"""
Extract text from PDF pages using EasyOCR.

This script processes PDF documents to extract text content,
handling both regular text and areas requiring OCR processing.
It outputs structured data including recognized text and metadata.

Dependencies:
- easyocr
- fitz (PyMuPDF)
- numpy
"""
import pymupdf # imports the pymupdf library
import easyocr
import numpy as np
from PIL import Image
import time

# Initialize EasyOCR reader for English language
easyocr_reader = easyocr.Reader(['en'])

mat = pymupdf.Matrix(4, 4)  # high resolution matrix
ocr_time = 0
pix_time = 0


def extract_text_with_ocr(page, bbox):
    """Extract text from a specific area using EasyOCR.

    Args:
        page: fitz.Page object
        bbox: tuple of coordinates defining the area to process
    Returns:
        dict containing extracted text and confidence score
    """
    # Create high-resolution image of the area
    pix = page.get_pixmap(
        colorspace=pymupdf.csGRAY,
        matrix=pymupdf.Matrix(2, 2),
        clip=bbox
    )

    # Convert to PIL Image
    img = Image.frombytes("L", [pix.width, pix.height], pix.samples)
    img_array = np.array(img)

    # Perform OCR
    result = easyocr_reader.readtext(img_array)

    if result:
        return {
            'text': result[0][1],
            'confidence': result[0][2]
        }
    return {
        'text': '',
        'confidence': 0.0
    }


def process_pdf(pdf_path):
    """Process PDF document and extract text content.

    Args:
        pdf_path: str, path to PDF file
    Returns:
        list of dicts containing structured data for each page
    """
    doc = pymupdf.open(pdf_path)
    pages_data = []

    for page_num, page in enumerate(doc):
        page_data = {
            'page_number': page_num + 1,
            'blocks': []
        }

        text_blocks = page.get_text("dict", flags=0)["blocks"]
        for block in text_blocks:
            block_data = {
                'bbox': block['bbox'],
                'lines': []
            }

            for line in block["lines"]:
                line_text = []
                for span in line["spans"]:
                    text = span["text"]
                    if chr(65533) in text:  # Process unrecognized characters
                        ocr_result = extract_text_with_ocr(page, span["bbox"])
                        line_text.append(ocr_result['text'])
                    else:
                        line_text.append(text)

                block_data['lines'].append(' '.join(line_text))

            page_data['blocks'].append(block_data)

        pages_data.append(page_data)

    doc.close()
    return pages_data
