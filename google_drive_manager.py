import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from spreadsheet_manager import load_spreadsheet, save_spreadsheet, is_duplicate
from utils import ensure_folder_exists

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    """Authenticate and create a Google Drive service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)
def check_new_file(service, drive_folder_id, seen_files):
    """Check for new files in the Google Drive folder."""
    new_file = []
    query = f"'{drive_folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    for file in files:
        if file['id'] not in seen_files:
            seen_files.add(file['id'])
            new_file.append(file)

    return new_file

def process_folder(input_folder, output_folder, drive_folder_id=None):
    """Process all medical bills in the input folder."""
    # Authenticate with Google Drive
    service = authenticate_google_drive() if drive_folder_id else None

    # Ensure the output folder exists
    ensure_folder_exists(output_folder)

    # Define the output spreadsheet path
    output_spreadsheet_path = os.path.join(output_folder, 'scan.xlsx')

    # Download the existing spreadsheet from Google Drive (if it exists)
    if drive_folder_id and service:
        try:
            # Search for the file in Google Drive
            results = service.files().list(q=f"scans.xlsx' and '{drive_folder_id}' in parents",
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