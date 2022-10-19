import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


URL = "https://www.uwindsor.ca/science/computerscience/event-calendar/month"
page = requests.get(URL)

# print(page.text)
soup = BeautifulSoup(page.content, "html.parser")

tables = soup.find_all('table')
cal = soup.find('table',class_="full").tbody

print(cal.prettify())
