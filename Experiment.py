import requests
from bs4 import BeautifulSoup
import pdb
import re

links = [
    "https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Arnett"
    # "http://informs.beaconfire.us/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Muckstadt-John-A"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

for x in links:
    print(x)
    try:
      experimental = requests.get(x, verify=False).status_code
      print(experimental)

      sourcecode = requests.get(x, headers = headers)
      txt = sourcecode.text
      soup = BeautifulSoup(txt, "html.parser")
      body = soup.find("div", {"class": "body"})
      # for link in body.findAll('a'):
      #     print(link)

      print("time elapsed is: " + str(sourcecode.elapsed.total_seconds()))
      print("try " + str(sourcecode.status_code))
      #print(sourcecode.text)
      code = sourcecode.status_code
      #print(sourcecode.text)
      #pdb.set_trace()



      if code == 200:
          print("caught by if statement")
    except requests.exceptions.SSLError as s:
        code = "SSLError"
        print(code)
    except Exception as e:
      print("Exception is" + str(e))
      code = "Exception is" + str(e)
      print("except " + str(code))
      if code != 200:
          print('code does not equal 200')
          code = "Error"
