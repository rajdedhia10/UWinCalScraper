import requests
from bs4 import BeautifulSoup

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


