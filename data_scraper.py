import urllib2
import re

cafes = 'http://dining.umd.edu/locations/'
page = urllib2.urlopen(cafes)

from bs4 import BeautifulSoup

soup = BeautifulSoup(page, 'html.parser')


#takes each table entry 
all_entries = soup.find_all('td')
#takes the names of all dining locations
all_h3 = soup.find_all('h3', class_ = 'colored')

#list to store days and times of operation
tables = []
times = []

for x in all_entries:
    schedule = x.text
    #gets rid of colon, am, pm from times
    schedule = re.sub('[ampPMA.:]', '', schedule)
    times.append(schedule)


#gets rid of the day labels
hours = times[1::2]

#creates lists that has the hours that all stores are open on monday, etc.
#list hours are in the same order as locations 
Monday = hours[0::7]
Tuesday = hours[1::7]
Wednesday = hours[2::7]
Thursday = hours[3::7]
Friday = hours[4::7]
Saturday = hours[5::7]
Sunday = hours[6::7]
#==========================================================
#function that splits up the time strings into integer values
#for open and close times
def day_splitter(day): 

    day_open = []
    day_close  = []
    counter = 0

    for i in day:
        time_list = []
        #locations that aren't open recieve null values
        if i in ['Closed', 'Closed ', 'Colsed', 'Under construction', 'Closed;Closed']:
            day[counter] = '0 - 0'
        if i in ['Oen 24 hours', '24 hours']:
            day[counter] = '0 - 1200'
        #Separates open and close time
        time_list = (day[counter]).split('-')
        
        counter += 1
        #idnight is used bc capital M was removed earlier
        if len(time_list) == 2:
            if time_list[1] == ' idnight':
                time_list[1] = 1200
        if time_list[0] == 'Noon ':
            time_list[0] = 1200
        x = int(time_list[0])
        y = int(time_list[1])
        #converts to 24 hour time
        if y != 0:
            if y == 100:
                pass
            else:
                y += 1200
        day_open.append(x)
        day_close.append(y)
        print x
        print y
    #returns open and close time lists
    return day_open, day_close

#creates the lists specific to each day by calling the function for each day
monday_open, monday_close = day_splitter(Monday)
tuesday_open, tuesday_close = day_splitter(Tuesday)
wednesday_open, wednesday_close = day_splitter(Wednesday)
thursday_open, thursday_close = day_splitter(Thursday)
friday_open, friday_close = day_splitter(Friday)
saturday_open, saturday_close = day_splitter(Saturday)
sunday_open, sunday_close = day_splitter(Sunday)

#============================================================
location = []

for x in all_h3:
    individual = x.text
    #Amazing line that gets rid of html crap
    individual = individual.encode('ascii', 'ignore').decode('ascii')
    #deals with individual discrepancies between name on website
    #and name in location gdb
    if individual == 'Samovar Ramen Noodle Bar':
        individual = 'Samovar'
    if individual == "The Union":
        individual = "Union"
    if individual == "Rudys":
        individual = "Rudy's"
    if individual == "Off the Record":
        individual = "Off The Record"    
    if individual == "North Convenience Shop":
        individual = "North Convenience"
    if individual == 'Sneakers Smoothies':
        individual = 'Sneaker\'s Smoothies'
    if individual == 'Auntie Annes':
        individual = 'Auntie Anne\'s'
    if individual == 'McDonalds':
        individual = 'McDonald\'s'
    if individual == 'Chick-fil-A':
        individual = 'Chik-Fil-A'
    if individual == 'South Commons':
        individual = 'South Commons Shop'
    if individual == '24Shop':
        individual = '24 Shop'
    

    location.append(individual)
#==========================================================
#defining which locations have coffee and are accessible
#to the general public
coffeeLocations = []
for x in location:
    if x not in ['The Diner', 'South Campus Dining Hall', '251 North',
                 'Maryland Hillel', 'Mulligans Grill and Pub', 'Sneaker\'s Smoothies'
                 'Auntie Annes', 'Moby Dick', 'Panda Express', 'Saladworks',
                 'Sbarro', 'Hibachi San', 'Green Tidings Mobile Dining',
                 'Maryland Dairy' ]:
        coffeeLocations.append('yes')
    else:
        coffeeLocations.append('no')
    
    

import pandas as pd

#creates columns based on previously filled lists
df=pd.DataFrame(location,columns=['Location'])
df['Mon_open'] = monday_open
df['Mon_close'] = monday_close
df['Tue_open'] = tuesday_open
df['Tue_close'] = tuesday_close
df['Wed_open'] = wednesday_open
df['Wed_close'] = wednesday_close
df['Thu_open'] = thursday_open
df['Thu_close'] = thursday_close
df['Fri_open'] = friday_open
df['Fri_close'] = friday_close
df['Sat_open'] = saturday_open
df['Sat_close'] = saturday_close
df['Sun_open'] = sunday_open
df['Sun_close'] = sunday_close
df['coffee'] = coffeeLocations
#creates and writes a csv file
df.to_csv('C:\Users\Devin Simmons\Desktop\ArcGIS\Coffee_Shop_Project\outputs\locations.csv')

