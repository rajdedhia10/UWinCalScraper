from __future__ import print_function
import requests
from bs4 import BeautifulSoup

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def scraper():
    URL = "https://www.uwindsor.ca/science/computerscience/event-calendar/month"
    page = requests.get(URL)

    # print(page.text)
    soup = BeautifulSoup(page.content, "html.parser")

    # cal2 = soup.find_all(class_="single-day past")
# cal2 is for past events
# disabling cal2 as future events need not be added to the calendar

cal3 = soup.find_all(class_="single-day future")
# cal3 is for future events

# for i in range (len(cal2)):
#     print("\n\n")
#     event_title = cal2[i].find(class_="event-title").text.strip()
#     print(event_title)
#     event_date = cal2[i]["data-date"]
#     print(event_date)
#     event_link = "www.uwindsor.ca"+ cal2[i].find('a', href=True)['href']
#     print(event_link)
#     event_time = cal2[i].find(class_="event-date").text.strip()
#     print(event_time)

for i in range (len(cal3)):
    print("\n\n")
    event_title = cal3[i].find(class_="event-title").text.strip()
    print(event_title)
    event_date = cal3[i]["data-date"]
    print(event_date)
    event_link = "www.uwindsor.ca"+ cal3[i].find('a', href=True)['href']
    print(event_link)
    event_time = cal3[i].find(class_="event-date").text.strip()
    print(event_time)

def inserter(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

    except HttpError as error:
        print('An error occurred: %s' % error)

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        page_token = None
        service = build('calendar', 'v3', credentials=creds)
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary'])


    except HttpError as error:
        print('An error occurred: %s' % error)




if __name__ == '__main__':
    main()