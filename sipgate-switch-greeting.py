#!/usr/bin/env python3

# This script can run daily and activate the next date's voicemail greeting
# The greetings need to already be uploaded to the sipgate account using
# sipgate-upload-greeting.py with fileformat AB_YYYY-MM-DD.mp3
# For Authentication, create a https://app.sipgate.com/personal-access-token

import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os


SIPGATE_VOICEMAIL_API = os.environ.get("SIPGATE_VOICEMAIL_API","https://api.sipgate.com/v2/w0/phonelines/p0/voicemails/v0/greetings")
SIPGATE_USERNAME = os.environ.get("SIPGATE_TOKEN_ID")
SIPGATE_PASSWORD = os.environ.get("SIPGATE_TOKEN")
EVENT_URL = os.environ.get("EVENT_URL")

def fetch_and_parse_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', id='termine-tabelle')
    return table

def find_next_event_date(table):
    rows = table.find_all('tr')
    today = datetime.now().date()

    for row in rows:
        date_str = row.find('td', class_='termin-date').text.strip()
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if event_date >= today:
            return date_str
    return None

def get_voicemail_greetings():
    try:
        response = requests.get(
            SIPGATE_VOICEMAIL_API,
            auth=HTTPBasicAuth(SIPGATE_USERNAME, SIPGATE_PASSWORD)
        )
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err}")
    return None

def set_active_greeting(greeting_id):
    url = f"{SIPGATE_VOICEMAIL_API}/{greeting_id}"
    try:
        response = requests.put(
            url,
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(SIPGATE_USERNAME, SIPGATE_PASSWORD),
            json={"active": True}
        )
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
    return False

def main():
    if not EVENT_URL:
        print("No Event URL specified, please define EVENT_URL environmental variable!")
        sys.exit(1)

    if not SIPGATE_USERNAME or not SIPGATE_PASSWORD:
        print("No Sipgate Authentication specified, please define SIPGATE_TOKEN_ID and SIPGATE_TOKEN.\nPersonal Access Token can be created on https://app.sipgate.com/personal-access-token")
        sys.exit(1)

    table = fetch_and_parse_table(EVENT_URL)
    next_event_date = find_next_event_date(table)

    if not next_event_date:
        print("No upcoming events found.")
        sys.exit(1)

    greetings = get_voicemail_greetings()
    if greetings:
        for item in greetings.get('items', []):
            if item.get('alias') == f"AB {next_event_date}":
                if item.get('active'):
                    print(f"Greeting for {next_event_date} is already active.")
                    sys.exit(0)
                else:
                    if set_active_greeting(item['id']):
                        print(f"Successfully activated greeting for {next_event_date}.")
                        sys.exit(0)
                    else:
                        print(f"Failed to activate greeting for {next_event_date}.")
                        sys.exit(1)

    print(f"No greeting found for {next_event_date}.")
    sys.exit(1)

if __name__ == "__main__":
    main()
