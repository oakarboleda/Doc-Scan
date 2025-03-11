import pandas as pd

def load_spreadsheet(file_path):
    """Load an existing spreadsheet or create a new DataFrame."""
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError:
        return pd.DataFrame()

def save_spreadsheet(df, file_path):
    """Save the DataFrame to a spreadsheet."""
    df.to_excel(file_path, index=False)
    print(f"Spreadsheet saved to {file_path}")

def is_duplicate(df, invoice_number):
    """Check if a bill with the given invoice number already exists."""
    if df is not None and 'invoice_number' in df.columns:
        return invoice_number in df['invoice_number'].values
    return False