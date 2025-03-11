import cv2
import pytesseract

def load_image(image_path):
    """Load and preprocess the image."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for better OCR
    return gray

def extract_text(image):
    """Extract text from the image using Tesseract OCR."""
    text = pytesseract.image_to_string(image)
    return text