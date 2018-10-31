import requests
from bs4 import BeautifulSoup
import pdb
import re

links = [
    # "https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Sargent-Robert-G"
    "https://www.informs.org/Explore/History-of-O.R.-Excellence/Academic-Institutions/Cornell-University"
    # "https://www.informs.org/Explore/History-of-O.R.-Excellence/Academic-Institutions/Case-Western-Reserve-University-Case-Institute-of-Technology"
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

      description_ = ''
      body = soup.find("div", {"class": "content-container"})
      ptags = body.findAll(True)
      print(ptags)
      for tag in ptags:
          print("tag is ")
          print(tag)
          if tag.name == "p":
              description_ += tag.text + ' '
          if tag.name == "h3" and (tag.text == "Links and References" or \
                                  tag.text == "Associated Historic Individuals"):
              break
      description_ = re.sub('[(){}<>]', '', description_)
      count = len(description_.replace('\n', ' ').rstrip('?:!.,;()').split())
      print([description_, count])

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
