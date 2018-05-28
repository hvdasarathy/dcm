import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

# def highlight_closed(s):
#
#     is_closed = s == 'Closed: Check @DCM_Lines for Venue Options'
#     return ['background-color: red' if v else '' for v in is_closed]

time_vector_start = datetime(2018, 6, 29, 16, 0, 0)
time_vector_end = datetime(2018, 7, 2, 0, 0, 0)
step = timedelta(minutes=10)
time_vector = []

# Create vector associated with all the times we will be checking for
# Every 10 minutes from 4pm on Friday to Midnight on Sunday.
dt = time_vector_start
while dt < time_vector_end:
    time_vector.append(dt)
    dt += step

base_df = pd.DataFrame(index=time_vector

# lookup references from dcm website,
location_ref = {133: "Hell\'s Kitchen",
                136: "All Stars Project - Grunebaum",
                138: "All Stars Project - Castillo",
                137: "All Stars Project - Demo",
                134: "The Griffin",
                114: "Magnet",
                93: "UCBT - East Village",
                115: "TNC - Cabaret",
                126: "TNC - Cino",
                122: "TNC - Community",
                118: "TNC - Johnson"}

day_ref = {'Fri': 'June 29 2018',
           'Sat': 'June 30 2018',
           'Sun': 'July 01 2018'}

# pull html from website
dcm_html = requests.get('http://delclosemarathon.com/calendar')
soup = BeautifulSoup(dcm_html.text, "html.parser")

# find the specific div that contains all the shows
dcm_schedule = soup.find(name='div', attrs={'class': 'tab-content'})
for loc in location_ref.keys():
    # theatre specific information/shows and show times
    theatre_schedule = dcm_schedule.find(name='div', attrs={'id': 'loc' + str(loc)})
    theatre_shows = theatre_schedule.find_all(name='div')
    theatre_times = [
        datetime.strptime(day_ref[i['data-start'].split(' ')[0]] + i['data-start'].split(' ')[1], "%B %d %Y%I:%M%p") for
        i in theatre_shows]
    theatre_names = [i['data-title'] for i in theatre_shows]
    df = pd.DataFrame(theatre_names, theatre_times, columns=[location_ref[loc]])

    # fit new dataframe into original base dataframe to fill in show info
    df = df.reindex(base_df.index, method='pad')
    base_df=base_df.join(df)

# save data to excel file
base_df.to_excel('dcm_schedule.xlsx',index_label='Time')