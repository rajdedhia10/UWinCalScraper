from re import T
import requests
from bs4 import BeautifulSoup
from datetime import *
import base64

URL = "https://www.uwindsor.ca/science/computerscience/event-calendar/month"
page = requests.get(URL)

# print(page.text)
soup = BeautifulSoup(page.content, "html.parser")

# cal2 = soup.find_all(class_="single-day past")
# cal2 is for past events
# disabling cal2 as future events need not be added to the calendar

cal3 = soup.find_all(class_="single-day today")
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

def time_convert(t):
    # Set the time in 12-hour format
    # current_time = '2:00PM'
    # print("Time = ",t)

    # Convert 12 hour time to 24 hour format
    t = datetime.strptime(t, '%I:%M%p')
    return(t.time())


dict = {
        'event_title':'',
        'event_date':'',
        'event_link':'',
        'event_time':'',
        'start_time':'',
        'end_time':''
    }

for i in range (len(cal3)):
    # print("\n\n")
    # event_title = cal3[i].find(class_="event-title").text.strip()
    # print(event_title)
    # event_date = cal3[i]["data-date"]
    # print(event_date)
    # event_link = "www.uwindsor.ca"+ cal3[i].find('a', href=True)['href']
    # print(event_link)
    # event_time = cal3[i].find(class_="event-date").text.strip()
    # print(event_time)

    print("\n\n")
    dict.update({'event_title': cal3[i].find(class_="event-title").text.strip()})
    # print(event_title)
    dict.update({'event_date': cal3[i]["data-date"]})
    # print(event_date)
    dict.update({'event_link':"www.uwindsor.ca"+ cal3[i].find('a', href=True)['href']})
    # print(event_link)
    dict.update({'event_time': cal3[i].find(class_="event-date").text.strip()})
    event_time = cal3[i].find(class_="event-date").text.strip()
    # print(event_time)

    start_time = event_time[:event_time.find(' ')]
    end_time = event_time[event_time.rfind(' ')+1:]

    x = (base64.b32hexencode(dict.get('event_title').encode("UTF-8")))
    print(x.decode("UTF-8").lower()[:-6])
    print(base64.b32hexdecode(x).decode("UTF-8"))

    dict.update({'start_time': str(time_convert(start_time))})
    dict.update({'end_time': str(time_convert(end_time))})
    # print(time_convert(start_time))
    # print(time_convert(end_time))
    # print(dict)


    # print(dict.get('event_date')+'T'+dict.get('start_time')+'-04:00')
    # print(dict.get('event_date')+'T'+dict.get('end_time')+'-04:00')

    # start_time = event_time[:event_time.find(' ')]
    # end_time = event_time[event_time.rfind(' ')+1:]
    # print(time_convert(start_time))
    # print(time_convert(end_time))