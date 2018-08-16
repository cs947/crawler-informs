import requests
from bs4 import BeautifulSoup
import pdb

links = [
    "http://www.biomedreports.com/articles/latest-news/1904-richard-staelin-phd-duke-university-professor-will-lead-board-of-directors.html",
    "https://asq.org/about-asq/honorary-members/box",
    "https://www.jstor.org/stable/167358"
    # "https://www.informs-sim.org/wsc17papers/includes/files/005.pdf",
    # "http://www.econlib.org/library/Enc/bios/Allais.html",
    # "https://ise.usc.edu/directory/faculty/profile/?lname=Settles&fname=Frank",
    # "http://www.biomedreports.com/articles/latest-news/1904-richard-staelin-phd-duke-university-professor-will-lead-board-of-directors.html",
    # "https://ioe.engin.umich.edu/people/marlin-thomas/",
    # "https://www.asme.org/about-asme/get-involved/honors-awards/achievement-awards/rufus-oldenburger-medal"
#    "http://cpms.section.informs.org",
    # "https://www.stoprog.org/sites/default/files/Pioneers/Robinson.pdf",
    # "math.ucdenver.edu/~hgreenbe/vita.shtml",
    # "http://math.ucdenver.edu/~hgreenbe/vita.shtml",
    # "https://www.informs-sim.org/wsc17papers/includes/files/013.pdf"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

for x in links:
    print(x)
    try:
      experimental = requests.get(x, verify=False).status_code
      print(experimental)
      sourcecode = requests.get(x)
      print("time elapsed is: " + str(sourcecode.elapsed.total_seconds()))
      print("try " + str(sourcecode.status_code))
      code = sourcecode.status_code
      #pdb.set_trace()
      if code == 200:
          print("caught by if statement")
    except requests.exceptions.SSLError as s:
        code = "SSLError"
        print(code)
    except Exception as e:
      print("Exception is" + e)
      code = sourcecode.status_code
      print("except " + str(code))
      if code != 200:
          print('code does not equal 200')
          code = "Error"
