from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

# Set up the Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'summer-monument-465306-e7-1de3af74c67d.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

# Replace with your folder ID
folder_id = '1aw0OYYvgUgVx2XJjQPRrN0X8x5TsPG0c'

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
