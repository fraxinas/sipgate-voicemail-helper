#!/usr/bin/env python3

# This script can run daily and activate the next date's voicemail greeting
# The greetings need to already be uploaded to the sipgate account using
# sipgate-upload-greeting.py with fileformat AB_YYYY-MM-DD.mp3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys

# Constants
BEARER_TOKEN = "Your_Bearer_Token_Here"
EVENT_URL = "https://rcab.de"
SIPGATE_VOICEMAIL_API = "https://api.sipgate.com/v2/w0/phonelines/p0/voicemails/v0/greetings"

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

def get_voicemail_greetings(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(SIPGATE_VOICEMAIL_API, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err}")
    return None

def set_active_greeting(token, greeting_id):
    url = f"{SIPGATE_VOICEMAIL_API}/{greeting_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"active": True}
    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 204

def main():
    table = fetch_and_parse_table(EVENT_URL)
    next_event_date = find_next_event_date(table)

    if not next_event_date:
        print("No upcoming events found.")
        sys.exit(1)

    greetings = get_voicemail_greetings(BEARER_TOKEN)
    if greetings:
        for item in greetings.get('items', []):
            if item.get('alias') == f"AB {next_event_date}":
                if item.get('active'):
                    print(f"Greeting for {next_event_date} is already active.")
                    sys.exit(0)
                else:
                    if set_active_greeting(BEARER_TOKEN, item['id']):
                        print(f"Successfully activated greeting for {next_event_date}.")
                        sys.exit(0)
                    else:
                        print(f"Failed to activate greeting for {next_event_date}.")
                        sys.exit(1)

    print(f"No greeting found for {next_event_date}.")
    sys.exit(1)

if __name__ == "__main__":
    main()
