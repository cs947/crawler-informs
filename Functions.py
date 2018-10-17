import requests
from bs4 import BeautifulSoup
import re


def find_links(all_letters):
    # returns a list of all the Briographical Profile links on INFORMS
    links = []
    for letter in all_letters:
        url = 'https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/(alpha)/' + letter
        # print(url)
        sourcecode = requests.get(url)
        txt = sourcecode.text
        soup = BeautifulSoup(txt, "html.parser")
        for link in soup.findAll('a'):
            href = link.get('href')
            string = str(href)
            # print(string)
            if len(string) < 54:
                continue
            if string.startswith('/Explore/History-of-O.R.-Excellence/Biographical-Profiles/') and \
                    string[58].isalpha():
                links.append('https://www.informs.org' + href)
    #print(links)
    return links

def find_m_links(area, m_page):
    # returns a list of links in O.R. Methodologies
    links = []
    for page in m_page:
        url = 'https://www.informs.org/Explore/History-of-O.R.-Excellence/' + area + page
        # print(url)
        sourcecode = requests.get(url)
        txt = sourcecode.text
        soup = BeautifulSoup(txt, "html.parser")
        for link in soup.findAll('a'):
            href = link.get('href')
            string = str(href)
            if len(string) < 54:
                continue
            if string.startswith('/Explore/History-of-O.R.-Excellence/O.R.-Methodologies/') and \
                string.find('(') == -1:
                links.append('https://www.informs.org' + href)
    print(links)
    return links

# def find_m_links(page):
#     # returns a list of links in O.R. Methodologies
#     links = []
#     # for area in contentarea:
#     #for page in m_page:
#     url = 'https://www.informs.org/Explore/History-of-O.R.-Excellence/O.R.-Application-Areas' + page
#     # print(url)
#     sourcecode = requests.get(url)
#     txt = sourcecode.text
#     soup = BeautifulSoup(txt, "html.parser")
#     for link in soup.findAll('a'):
#         href = link.get('href')
#         string = str(href)
#         # print(string)
#         if len(string) < 54:
#             continue
#         if string.startswith('/Explore/History-of-O.R.-Excellence/O.R.-Application-Areas/'):
#             links.append('https://www.informs.org' + href)
#     #print(links)
#     return links

def find_title(soup):
    title = soup.find('h1').text
    print('title is ' + title)
    return title

def find_date(soup):
    #print("in find_date and this is soup: " + str(soup))
    print('souptitlesstrin010' + soup.title.string[0:-10])
    name = soup.title.string[0:-10]
    name = name.split(',')
    print(name)
    if len(name) > 2:
        name = [name[0], ','.join(name[1:])]
    birth_date = ['N/A']
    death_date = ['N/A']
    year = ['N/A']
    for date in soup.findAll('div', {'id': 'lifespan'}):
        space = ' '
        print(date.count(space))
        for d_string in date.stripped_strings:
            date_str = repr(d_string)
            i_dash = d_string.find('–') #this is a special dash that I copied from the website
            dash = d_string[15:16] # .decode('utf-8')
            print(dash)
            if i_dash >= 0:
                death_date = [d_string[i_dash+1:].strip()]
                birth_date = d_string[:i_dash-1]
                comma = birth_date.find(',')
                print(birth_date)
                comma = birth_date.find(',')

                print("comma is " + str(comma))
                year = birth_date[comma+2:]

                year = [year]
                birth_date = [birth_date.strip()]

                print(year)
            else:
                birth_date = d_string
                birth_date = birth_date.strip()
                print(birth_date)
                comma = birth_date.find(',')
                print("comma is " + str(comma))
                year = birth_date[comma+2:]
                birth_date = [birth_date]
                year = [year]
                print(year)

    return name + year + birth_date + death_date


def if_photos(soup):
    # returns 'Absent' if there is not a photo
    # returns 'Present' if there is a photo
    indicator = 'Absent'
    for _ in soup.findAll('img', {'class': 'right dropshadow'}):
        indicator = 'Present'
    # print(indicator)
    return indicator

def desc_word_count(soup):
    description_ = ''
    body = soup.find("div", {"class": "body"})
    ptags = body.findAll(True)
    for tag in ptags:
        if tag.name == "p":
            description_ += tag.text + ' '
            # print("Tag's next sibling is: " + str(tag.next_sibling.name))
        if tag.name == "h3":
            print("foundh3")
            break
    description_ = re.sub('[(){}<>]', '', description_)
    count = len(description_.replace('\n', ' ').rstrip('?:!.,;()').split())
    print([description_, count])
    return[description_, count]


def bio_word_count(soup):
    # returns the number of words in the "Brief Biography" section of a Biographical
    # Profile
    brief_bio = ' '
    for string in soup.find('div', {'id': 'bio_header'}).strings:
        brief_bio += string + ' '
    brief_bio = re.sub('[(){}<>]', '', brief_bio)
    word_count = len(brief_bio.replace('\n', ' ').rstrip('?:!.,;()').split())
    # print(word_count)
    return word_count


def wiki_link(soup):
    # returns the link of the wikipedia link if there is one
    wiki = 'Absent'
    for link in soup.findAll('a'):
        href = str(link.get('href'))
        if href.startswith('http://en.wikipedia.org/wiki/'):
            wiki = href
    if ',' in wiki:
        wiki = wiki[0:wiki.find(',')]
    # print(wiki)
    return wiki


def contents_after(soup, name, tag_string):
    element = soup.find(name, string = tag_string)
    if element is None: return 'N/A'
    else:
        result = []
        while True:
            element = element.next_sibling
            if element is None: break
            if len(str(element)) < 5:
                continue
            if element.name != 'p': break
            result += [element.text]
    result = ';'.join(result)
    result = " ".join(result.split())
    result = result.replace(',', '')
    result = result.replace(';', '\n')
    # print(result)
    return result


def education(soup):
    return contents_after(soup, 'h3', 'Education')


def other_bio(soup):
    # print(contents_after(soup, 'h5', 'Other Biographies'))
    return contents_after(soup, 'h5', 'Other Biographies')


def awards(soup):
    return contents_after(soup, 'h3', 'Awards and Honors')


def prof_service(soup):
    return contents_after(soup, 'h3', 'Professional Service')


def archives(soup):
    return contents_after(soup, 'h3', 'Archives')


def add_resources(soup):
    return contents_after(soup, 'h3', 'Additional Resources')

def memoirs3(soup):
    return contents_after(soup, 'h3', 'Memoirs')

def memoirs(soup):
    return contents_after(soup, 'h5', 'Memoirs')


def counts_after(soup, name, tag_string):
    element = soup.find(name, string = tag_string)
    if element is None: return 0
    else:
        result = 0
        while True:
            element = element.next_sibling
            if element is None: break
            if len(str(element)) < 5:
                continue
            if element.name != 'p': break
            result += 1
    return result


def resume(soup):
    return counts_after(soup, 'h5', 'Résumé')


## for METHODOLOGIES
def linksandrefs(soup):
    # returns a count of the number of links and references on the page
    element = soup.find('h3', string = 'Links and References')
    if element is None: return 'N/A'
    else:
        result = 0
        while True:
            print(element)
            element = element.next_sibling
            if element is None: break
            if len(str(element)) < 5:
                continue
            if element.name != 'p': break
            result += 1
    return result
    # return counts_after(soup, 'h3', 'Links and References')

def indiv_count(soup):
    # returns a count of the associated historic individuals
    indivs = soup.findAll('li')
    result = len(indivs)
    return result

## end METHODOLOGIES
def obituaries(soup):
    return counts_after(soup, 'h3', 'Obituaries')


def publications(soup):
    return counts_after(soup, 'h3', 'Selected Publications')


def h5_match(soup, h5_string):
    lists = soup.find('h5', string = h5_string)
    if lists is None:
        return ['N/A', 'N/A']
    lists = lists.find_next_sibling('ul')
    hist = []
    add = []
    # print(lists.contents)
    lists = [a for a in lists.contents if a != '\n']
    # print(len(lists))
    for element in lists:
        # print(element)
        # print(s for s in element.stripped_strings)
        if len(str(element)) < 5: continue
        if element.find('a') is not None:
            hist += [a for a in element.strings if len(a) > 1]
        else:
            add += [a for a in element.strings if len(a) > 1]
    # print(hist)
    # print(add)
    hist = '\n'.join(hist)
    hist = hist.replace(',', '')
    if hist == '': hist = 'N/A'
    add = '\n'.join(add)
    add = add.replace(',', '')
    if add == '': add = 'N/A'
    return [hist, add]


def academic_ins(soup):
    return h5_match(soup, 'Academic Affiliations')


def non_academic_ins(soup):
    return h5_match(soup, 'Non-Academic Affiliations')


def methodologies(soup):
    return h5_match(soup, 'Methodologies')


def app_areas(soup):
    return h5_match(soup, 'Application Areas')


def pub_no(soup):
    pub = soup.find('h3', text = 'Selected Publications')
    if pub is None:
        return 0
    pub = pub.next_sibling.next_sibling
    count = 0
    while len(str(pub)) > 30:
        #print(str(pub))
        count += 1
        pub = pub.next_sibling
    return count


def oral_hist(soup):
    tag = soup.find('div', {'id': 'oral_hist_block'})
    if tag is None: return ['Absent', 0, 0]
    result = []
    tag_1 = tag.find('h3', string = 'Jump to Chapters')
    if tag_1 is None: result += ['Absent']
    else:  result += ['Present']
    tag_2 = tag.findAll('p')
    num = len(tag_2)
    if result[0] == 'Present': num -= 2
    check = [a.text for a in tag_2]
    num_embedded = sum(['YouTube' in a for a in check])
    result += [num_embedded, num - num_embedded]
    return result


def image(soup):
    tag = soup.find('h3', string = 'Image Gallery')
    if tag is None: return 'Absent'
    else: return 'Present'


def genealogy(soup):
    tag = soup.find('a', string = re.compile('^Mathematics Genealogy'))
    if tag is None: return 'N/A'
    else: return str(tag.get('href'))


def h3_h5(soup):
    tag = soup.findAll('h3')
    tag += soup.findAll('h5')
    result = [a.string for a in tag]
    print(result)
