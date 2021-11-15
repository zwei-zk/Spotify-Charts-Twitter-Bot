import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from time import time
from time import sleep
from random import randint
import pandas as pd
import tweepy
import re
from os import environ

# Twitter Bot Tokens
CONSUMER_API_KEY = 'CONSUMER_API_KEY'
CONSUMER_API_SECRET_KEY = 'CONSUMER_API_SECRET_KEY'
ACCESS_TOKEN = 'ACCESS_TOKEN'
ACCESS_SECRET_TOKEN = 'ACCESS_SECRET_TOKEN'

auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
api = tweepy.API(auth)

# Compile relevant data
url = "https://spotifycharts.com/regional/jp/daily/"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
req = requests.get(url, headers = headers)
sleep(randint(4, 5))
soup = BeautifulSoup(req.text, "html.parser")
chart = soup.find("table", {'class': 'chart-table'})
tbody = chart.find('tbody')
all_rows = []
for tr in tbody.findAll('tr'):
    rank = tr.find('td', {'class': 'chart-table-position'}).text
    artist = tr.find('td', {'class': 'chart-table-track'}).find('span').text
    artist = artist.replace("by ", " ").strip()
    
    # Fix artist names
    if artist == "Kenshi Yonezu":
        artist = "米津玄師"
    if artist == "Official HIGE DANdism":
        artist = "Official髭男dism"
    if artist == "Aimyon":
        artist = "あいみょん"
        
    title = tr.find('td', {'class': 'chart-table-track'}).find("strong").text
    streams = tr.find("td", {"class": "chart-table-streams"}).text
    link = tr.find("td", {"class": "chart-table-image"}).findAll('a', href = True)
    all_rows.append([rank, artist, title, streams, link])

datf = pd.DataFrame(all_rows, columns = ['Rank', 'Artist', "Title", "Streams", "Link"])
print(datf)
    
first = "[1]" + " " + datf['Title'].iloc[0] + " / " + datf['Artist'].iloc[0] + "\n" + datf['Streams'].iloc[0]
second = "[2]" + " " + datf['Title'].iloc[1] + " / " + datf['Artist'].iloc[1] + "\n" + datf['Streams'].iloc[1]
third = "[3]" + " " + datf['Title'].iloc[2] + " / " + datf['Artist'].iloc[2] + "\n" + datf['Streams'].iloc[2]
fourth = "[4]" + " " + datf['Title'].iloc[3] + " / " + datf['Artist'].iloc[3] + "\n" + datf['Streams'].iloc[3]
fifth = "[5]" + " " + datf['Title'].iloc[4] + " / " + datf['Artist'].iloc[4] + "\n" + datf['Streams'].iloc[4]
sixth = "[6]" + " " + datf['Title'].iloc[5] + " / " + datf['Artist'].iloc[5] + "\n" + datf['Streams'].iloc[5]
seventh = "[7]" + " " + datf['Title'].iloc[6] + " / " + datf['Artist'].iloc[6] + "\n" + datf['Streams'].iloc[6]
eighth = "[8]" + " " + datf['Title'].iloc[7] + " / " + datf['Artist'].iloc[7] + "\n" + datf['Streams'].iloc[7]
nineth = "[9]" + " " + datf['Title'].iloc[8] + " / " + datf['Artist'].iloc[8] + "\n" + datf['Streams'].iloc[8]
tenth = "[10]" + " " + datf['Title'].iloc[9] + " / " + datf['Artist'].iloc[9] + "\n" + datf['Streams'].iloc[9]

# Format and update status

first_link = (str(datf['Link'].iloc[0]))[10:63]
sixth_link = (str(datf['Link'].iloc[5]))[10:63]

status = api.update_status(first + '\n' + second + '\n' + third + '\n' + fourth + '\n' + fifth + '\n' + first_link)
status2 = api.update_status(('@PLACEHOLDER' + ' ' + sixth + '\n' + seventh + '\n' + eighth + '\n' + nineth + '\n' + tenth + '\n' + sixth_link), status.id)
