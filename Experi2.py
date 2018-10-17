import requests
from bs4 import BeautifulSoup
import pdb

links = [
    "https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Derman-Cyrus"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

for x in links:
    sourcecode = requests.get(x, headers = headers)
    text = sourcecode.text
    soup = BeautifulSoup(text, "html.parser")
    title = soup.find('title')
    print(title.string)
    print(title.text)
    print("soup.title " + str(soup.title))
    print("soup.title.string " + soup.title.string)
