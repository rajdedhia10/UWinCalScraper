from __future__ import print_function
import requests
from bs4 import BeautifulSoup
from datetime import *
import base64

import os.path
import config

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Convert time from 12 hrs to RFC3339 standard
def time_convert(t):
    t = datetime.strptime(t, '%I:%M%p')
    return(t.time())

# To insert the events to Calendar via API v3
def inserter(dict,creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Template to Insert an event

        # Added base32hexencode as id to avoid creating duplicate events. Hopefully it works
        event = {
        'id':base64.b32hexencode(dict.get('event_title').encode("UTF-8")).decode("UTF-8").lower()[:-6],
        'summary': 'CS Dept Event - '+ dict.get('event_date'),
        'description': dict.get('event_title') + ',' + dict.get('event_link'),
        'start': {
            'dateTime': dict.get('event_date')+'T'+dict.get('start_time')+'-04:00',
            'timeZone': 'Canada/Eastern',
        },
        'end': {
            'dateTime': dict.get('event_date')+'T'+dict.get('end_time')+'-04:00',
            'timeZone': 'Canada/Eastern',
        },
        'reminders': {
            'useDefault': True,
        },
        }

        # Call the Calendar Insert API

        event = service.events().insert(calendarId=config.Cal_ID, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


# To scrape the website and get the events
def scraper(creds):
    URL = "https://www.uwindsor.ca/science/computerscience/event-calendar/month"
    page = requests.get(URL)

    # print(page.text)
    soup = BeautifulSoup(page.content, "html.parser")

    # To add past events change class_="single-day past"
    cal3 = soup.find_all(class_="single-day future")
    # cal3 is for future events

    dict = {
        'event_title':'',
        'event_date':'',
        'event_link':'',
        'event_time':'',
        'start_time':'',
        'end_time':''
    }

    for i in range (len(cal3)):
        event_title = cal3[i].find_all(class_="event-title")
        event_link = cal3[i].find_all('a', href=True)
        event_time = cal3[i].find_all(class_="event-date")
        for k in range(len(event_time)):
            event_time[k] = event_time[k].text.strip()

        for j in range(len(event_title)):
            dict.update({'event_title': event_title[j].text.strip()})
            dict.update({'event_date': cal3[i]["data-date"]})
            dict.update({'event_link':"www.uwindsor.ca"+ event_link[j]['href']})
            dict.update({'event_time': event_time[j]})

            start_time = event_time[j][:event_time[j].find(' ')]
            end_time = event_time[j][event_time[j].rfind(' ')+1:]

            dict.update({'start_time': str(time_convert(start_time))})
            dict.update({'end_time': str(time_convert(end_time))})
        
            inserter(dict,creds)


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
        # service = build('calendar', 'v3', credentials=creds)
        # calendar_list = service.calendarList().list(pageToken=page_token).execute()
        # for calendar_list_entry in calendar_list['items']:
        #     print(calendar_list_entry['summary'])
        scraper(creds)


    except HttpError as error:
        print('An error occurred: %s' % error)




if __name__ == '__main__':
    main()