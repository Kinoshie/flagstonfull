
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up the Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Load credentials from Render environment variable
SERVICE_ACCOUNT_INFO = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])

creds = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

service = build('drive', 'v3', credentials=creds)

# Your folder ID
folder_id = '1w_Pjc4PZikkGgsF-aDn_aFZPrllXsUJj'

# Get list of image files
results = service.files().list(
    q=f"'{folder_id}' in parents and (mimeType='image/png' or mimeType='image/jpeg')",
    fields="nextPageToken, files(id, name)",
    orderBy="name"
).execute()
items = results.get('files', [])

POSTED_FILE_LOG = 'posted_files.txt'

# Load previously posted file IDs
if os.path.exists(POSTED_FILE_LOG):
    with open(POSTED_FILE_LOG, 'r') as f:
        posted_ids = set(f.read().splitlines())
else:
    posted_ids = set()

for idx, item in enumerate(items, 1):
    file_id = item['id']
    file_name = item['name']

    if file_id in posted_ids:
        continue  # Skip if already posted

    # Build image URL
    image_url = f"https://drive.google.com/uc?id={file_id}"

    # Create caption from file name (cleaned)
    base_name = os.path.splitext(file_name)[0]  # Remove extension
    caption = f"Motivational Post #{idx}: {base_name} ✨ #inspiration #dailyquote"

    # Output to console (or send via webhook here)
    print(f"{file_name}: {image_url}")
    print(f"Caption: {caption}\n")

    # Save this file ID to log
    with open(POSTED_FILE_LOG, 'a') as f:
        f.write(file_id + '\n')

    #break  # Optional: remove this if you want to process all images

# flagstonefullscriptwithcaption.py

def run_my_script(input_text: str = "") -> dict:
    # Your original script logic goes here
    # Use input_text if needed

    return {
        "status": "success",
        "message": "Script executed successfully!",
        "input": input_text
    }
