import os
from ocr_processor import load_image, extract_text
from data_parser import parse_medical_bill
from spreadsheet_manager import load_spreadsheet, save_spreadsheet, is_duplicate
from google_drive_manager import authenticate_google_drive, download_from_google_drive, upload_to_google_drive
from utils import ensure_folder_exists

def process_folder(input_folder, output_folder, drive_folder_id=None):
    """Process all medical bills in the input folder."""
    # Authenticate with Google Drive
    service = authenticate_google_drive() if drive_folder_id else None

    # Ensure the output folder exists
    ensure_folder_exists(output_folder)

    # Define the output spreadsheet path
    output_spreadsheet_path = os.path.join(output_folder, 'medical_bills.xlsx')

    # Download the existing spreadsheet from Google Drive (if it exists)
    if drive_folder_id and service:
        try:
            # Search for the file in Google Drive
            results = service.files().list(q=f"name='medical_bills.xlsx' and '{drive_folder_id}' in parents",
                                          fields="files(id, name)").execute()
            files = results.get('files', [])
            if files:
                file_id = files[0]['id']
                download_from_google_drive(service, file_id, output_spreadsheet_path)
        except Exception as e:
            print(f"Error downloading spreadsheet from Google Drive: {e}")

    # Load the existing spreadsheet (if it exists)
    df = load_spreadsheet(output_spreadsheet_path)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(input_folder, filename)
            print(f"Processing file: {filename}")

            # Step 1: Load and preprocess the image
            image = load_image(image_path)

            # Step 2: Extract text using OCR
            text = extract_text(image)
            print("Extracted Text:\n", text)  # For debugging

            # Step 3: Parse the text for key information
            bill_data = parse_medical_bill(text)
            print("Parsed Data:\n", bill_data)  # For debugging

            # Step 4: Check for duplicates
            if is_duplicate(df, bill_data['invoice_number']):
                print(f"Skipping duplicate bill with Invoice Number: {bill_data['invoice_number']}")
                continue

            # Step 5: Append the new data to the DataFrame
            df = pd.concat([df, pd.DataFrame([bill_data])], ignore_index=True)

    # Step 6: Save the updated spreadsheet
    save_spreadsheet(df, output_spreadsheet_path)

    # Step 7: Upload the updated spreadsheet to Google Drive
    if drive_folder_id and service:
        upload_to_google_drive(service, output_spreadsheet_path, drive_folder_id)

# Example usage
if __name__ == "__main__":
    input_folder = '/Volumes/Mine/Scans/Health Bills/'
    output_folder = 'output_spreadsheets'
    drive_folder_id = '1g-PvUQ-IIITvbkuWWKb4L9LZHgSfa5WK'  # Optional: Specify a folder ID
    process_folder(input_folder, output_folder, drive_folder_id)