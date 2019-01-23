import requests
from bs4 import BeautifulSoup
import pdb
import re

links = [
    # "https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Stidham-Jr.-Shaler"
    "https://web.archive.org/web/20121026123636/http://www.princeton.edu/~mudd/finding_aids/mathoral/pmc03.htm"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

for x in links:
    print(x)
    try:
      experimental = requests.get(x, verify=False).status_code
      print(experimental)

      sourcecode = requests.get(x, headers = headers)
      text = sourcecode.content
      soup = BeautifulSoup(text, "html.parser")
      body = soup.find("div", {"class": "body"})


      print("time elapsed is: " + str(sourcecode.elapsed.total_seconds()))
      print("try " + str(sourcecode.status_code))
      #print(sourcecode.text)
      code = sourcecode.status_code
      #print(sourcecode.text)
      #pdb.set_trace()

      


      '''
      var = soup.find('h3', text="Image Gallery")
      print("this is var: ")
      print(var)
      print("this is next sibling")
      print(var.next_sibling)
      print("this is child of var")
      print(var.children)
      print("this is next element")
      i = 5
      while i>0:
          next = var.next_element
          print(next)
          i = i -1

      print(var.next_element)

      print("be")
      x = var.findAll('img', {'class': 'right dropshadow'})
      print(x)
      print("after")
      i = 5
      # while i>0:
      #     next = var.find_next_sibling
      #     print(next)
      #     i = i -1
      #     print("next is:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
      it = iter(x)
      print("----------------------------------------------------------------------------------next is")
      #print(next(it))
      print("next was")
      var.find_next_sibling
      nextt = var.next_sibling
      print(nextt[0])
      print(nextt[1])
      if nextt[0] == "content-view-block block-slideshow_child_featured":
          print("TRUE")
      for _ in var.findAll('img', {'class': 'right dropshadow'}):
          print("asdf")
          indicator = 'Present'
      '''








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
