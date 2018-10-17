import requests
from bs4 import BeautifulSoup
import Functions as f
import pandas as pd
import datetime
import os
import unicodedata

#group_letters = ['A', 'C', 'F', 'I', 'M', 'O', 'S', 'V'] #comment for testing
#personal_links = f.find_links(group_letters)
personal_links = [
    "https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Avriel-Mordecai",
    "https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Nash-Jr.-John-F"
    ]
for i in personal_links:
    source_code = requests.get(i)
    text = source_code.text
    soup = BeautifulSoup(text, "html.parser")
    name = soup.title.string[0:-10]
    name = name.split(',')
    print(name)
    if len(name) > 2:
        name = [name[0], ','.join(name[1:])]

    for date in soup.findAll('div', {'id': 'lifespan'}):
        for d_string in date.stripped_strings:
            print(d_string)
            print(type(d_string))
            date_str = repr(d_string)
            i_dash = d_string.find('–') #this is a special dash that I copied from the website
            print("i_dash is " + str(i_dash))
            dash = d_string[15:16] # .decode('utf-8')
            print(dash)
            if i_dash >= 0:
                death_date = d_string[i_dash+1:].strip()
                #death_date.strip()
                #death_date = death_date.strip()
                #print("death date two " + death_date)
                print(death_date)
                born_date = d_string[:i_dash]
                born_date = born_date.strip()
                print("born date is " + born_date)
            else:
                born_date = d_string
                born_date = born_date.strip()
                print(born_date)
                death_date = 'N/A'
        #if len(date.contents) == 1:



def find_date(soup):
    name = soup.title.string[0:-10]
    name = name.split(',')
    print(name)
    if len(name) > 2:
        name = [name[0], ','.join(name[1:])]
    for date in soup.findAll('div', {'id': 'lifespan'}):
        # print('So we have to split here')
        print(date.contents)
        print(len(date.contents))
        i_dash = date.index('-')
        if i_dash >= 0: #there is a death date
            death_date = date[i_dash:]
            birth_date = date[:i_dash].strip()
            print(date[:i_dash])
            print(birth_date)

    return name + date


#copied from Functions
def find_date(soup):
    name = soup.title.string[0:-10]
    name = name.split(',')
    print(name)
    if len(name) > 2:
        name = [name[0], ','.join(name[1:])]
    for date in soup.findAll('div', {'id': 'lifespan'}):
        # print('So we have to split here')
        # print(date.contents)
        # print(len(date.contents))
        if len(date.contents) == 1:
            if len(date.string) > 5:
                date = str(date.string).strip()
                i_dash = date.index('–')
                if i_dash < 5: born_date = 'N/A'
                else:
                    born_date = date[0:i_dash-9]
                    # i_born = born_date.index(',')
                    # born_date = born_date[0:i_born] + born_date[i_born+1:]
                die_date = date[i_dash+2:]
                # i_die = die_date.index(',')
                # die_date = die_date[0:i_die] + die_date[i_die+1:]
                date = [born_date, die_date]
            else: date = ['N/A', 'N/A']
        else:
            born_date = str(date.contents[2].string).strip()
            # i_born = born_date.index(',')
            # born_date = born_date[0:i_born] + born_date[i_born+1:]
            date = [born_date, 'N/A']
    # print(name + ',' + date)
    return name + date
