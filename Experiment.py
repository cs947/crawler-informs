import requests
from bs4 import BeautifulSoup
import pdb

links = [
    "https://findingaids.princeton.edu/collections/AC391",
    "http://www.anziam.org.au/The+1995+ANZIAM+Medal",
    #"http://connect.informs.org/sola/solaawards"
    "http://news.wharton.upenn.edu/feature-stories/2012/09/in-memoriam-paul-r-kleindorfer/"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

for x in links:
    print(x)
    try:
      experimental = requests.get(x, verify=False).status_code
      print(experimental)
      sourcecode = requests.get(x, headers = headers)
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
