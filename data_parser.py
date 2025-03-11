import re

def parse_medical_bill(text):
    """Parse medical bill text into structured data."""
    patterns = {
        'patient_name': re.compile(r'Patient:\s*([A-Za-z\s]+)'),
        'provider_name': re.compile(r'Provider:\s*([A-Za-z\s]+)'),
        'date_of_service': re.compile(r'Date of Service:\s*(\d{2}/\d{2}/\d{4})'),
        'total_amount_due': re.compile(r'Total Amount Due:\s*(\$\d+\.\d{2})'),
        'invoice_number': re.compile(r'Invoice #:\s*([A-Z0-9-]+)'),
        'insurance_info': re.compile(r'Insurance:\s*([A-Za-z\s]+)')
    }
    data = {}
    for key, pattern in patterns.items():
        match = pattern.search(text)
        if match:
            data[key] = match.group(1).strip()
        else:
            data[key] = None
    return data