#!/usr/bin/env python3

# This script uploads an audio file as a new greeting to sipgate
# requires an app token and the permissions for the phonelines scope

import requests
from requests.auth import HTTPBasicAuth
import base64
import sys
import glob
import os

def encode_file_to_base64(filepath):
    with open(filepath, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

def update_sipgate_voicemail(token_id, token, base64_content, filename):
    url = "https://api.sipgate.com/v2/w0/phonelines/p0/voicemails/v0/greetings"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "filename": filename,
        "base64Content": base64_content
    }
    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(token_id, token), json=data)
    return response

def process_files(file_pattern, sipgate_token_id, sipgate_token):
    for filepath in glob.glob(file_pattern):
        try:
            base64_content = encode_file_to_base64(filepath)
            response = update_sipgate_voicemail(sipgate_token_id, sipgate_token, base64_content, filepath.split("/")[-1])
            print(f"Processed {filepath} - Response Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: sipgate-upload-greeting.py '<audio_file_pattern>' <sipgate_token_id> <sipgate_token>")
        sys.exit(1)

    file_pattern = sys.argv[1]
    sipgate_token_id = sys.argv[2]
    sipgate_token = sys.argv[3]

    process_files(file_pattern, sipgate_token_id, sipgate_token)

if __name__ == "__main__":
    main()
