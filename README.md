# UWinCalScraper 📅

Python script to scrape [UWindsor Computer Science Events](https://www.uwindsor.ca/science/computerscience/event-calendar/month) website, parse the information about upcoming Events, their date and timings and add it to Google Calendar using Google Calendar API v3.

## Why does this exist? 🤔

Because I am a very lazy person and to visit the site regularly to get the updates and manually add them to my calendar was very boring.

## Steps to self host 💻

0. Star ⭐ the project
1. Generate your Google Calendar API credetials from [here](https://console.cloud.google.com/apis/credentials) and save it as credentials.json
2. Create a calendar in Google Calendars and save its Calendar ID as config.py
3. Run Scraper.py and autheticate the OAuth popup
4. Enjoy the automation

## Libraries used 📂

1. python 3.10 (older versions will not work)
2. google-api-python-client
3. BeautifulSoup
4. requests
5. base64