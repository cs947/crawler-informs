import requests
import pickle
import datetime
import os
import pandas as pd
from queue import *
from bs4 import BeautifulSoup
import pdb


def find_internal_links():
    root_link = "/Explore/History-of-O.R.-Excellence"
    internal_links = set()
    internal_links.add(root_link)
    queue = Queue()
    queue.put(root_link)

    while queue.qsize() > 0:
        curr_link = queue.get()
        for link in ret_int_link(curr_link):
            if link not in internal_links:
                # print(link)
                print("size of queue: " + str(queue.qsize()) + "; size of set: " + str(len(internal_links)), "\n")
                internal_links.add(link)
                queue.put(link)
                # if len(internal_links) == 20: break # for testing

    with open('internal_list.pkl', 'wb') as output:
        pickle.dump(internal_links, output, pickle.HIGHEST_PROTOCOL)
    print("Finished! Total of ", len(internal_links), " pages are found.\n",
          "Pickle file generated under", os.getcwd(), "\n")


def ret_int_link(link):
    try:
        sourcecode = requests.get("https://www.informs.org" + link, timeout=5)
    except Exception as e:
        print(e)
        return []
    text = sourcecode.text
    soup = BeautifulSoup(text, "html.parser")
    main = soup.main

    children = []
    for url in main.findAll('a'):
        href = url.get('href')
        href_str = str(href)
        if href_str.startswith('/Explore/History-of-O.R.-Excellence') and "?" not in href_str and "#" not in href_str and "pdf" not in href_str:
            children.append(str(href))
    return children

def ret_all_link(link):
    try:
        sourcecode = requests.get("https://www.informs.org" + link, timeout=5)
    except Exception as e:
        print(e)
        return []
    text = sourcecode.text
    soup = BeautifulSoup(text, "html.parser")
    main = soup.main
    children = []
    for url in main.findAll('a'):
        href = url.get('href')
        href_str = str(href)
        # if href_str.startswith('/') and "?" not in href_str and "#" not in href_str:
        #     children.append(["https://www.informs.org" + href_str, url.text.replace('\n', '')])
        if href_str.startswith('http') and "?" not in href_str and "#" not in href_str and "pubsonline" not in href_str and "linkedin" not in href_str and "analytics-magazine.org" not in href_str:
            children.append([href_str, url.text.replace('\n', '')])
    return children


def check(link):
    #returns what goes into a line on the dead links spreadsheet
    #checks if the link is actually dead or not
    '''
    if "pubsonline" in link[1]:
        return [link[0], link[1], 403]
    elif "linkedin" in link[1]:
        return [link[0], link[1], 999]
    '''
    # link[0] is link, link[1] is text
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    code= 0
    error = ""
    try:
        sourcecode = requests.get(link[0], headers = headers)
        code = sourcecode.status_code
        print("time elapsed is: " + str(sourcecode.elapsed.total_seconds()))
#        print(str(code) + " try block " + link[0])
        # if code == 200:
        #     print(link[0] + " caught by if statement")
    except requests.exceptions.SSLError as s:
        print("SSLError")
        sourcecodeSSLError = requests.get(link[0], verify = False, headers = headers)
        code = sourcecodeSSLError.status_code
        error = s
    except Exception as e:
        print("Other Exception occured")
        error = e

    info_list = [link[0], link[1], code, error]
    if code != 200:
        return info_list
    else:
        return []

def find_math_genea(link, link_pair):
    print("link is :" + str(link))
    print("link_pair is: " + str(link_pair))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    parent = "https://www.informs.org" + link
    child = link_pair[0]
    try:
        sourcecode = requests.get(link, headers=headers)
    except Exception as e:
        print(e)
        return []
    code = sourcecode.status_code
    text = sourcecode.text
    soup = BeautifulSoup(text, "html.parser")
    text = soup.find_all(href = link_pair[1])[0].parent.text
    foo = [parent, child, code, text]
    print(foo)
    return foo

def check_list(list_towrite):
    if list_towrite[2] != "link": return list_towrite
    parent = list_towrite[0]
    child = list_towrite[1]
    try:
        sourcecode = requests.get(parent, timeout = 5)
        text = sourcecode.text
    except:
        text = "link"
    soup = BeautifulSoup(text, "html.parser")
    list_towrite[2] = soup.find_all(href = child)[0].parent.text
    print(list_towrite[2])
    return list_towrite

def generate_link_dataframe():
    try:
        with open('internal_list.pkl', 'rb') as output:
            link_set = pickle.load(output)
    except:
        print("Internal links not found. Please run 'find' to generate internal links\n")
        return
    print("Successfully opened list set")
    links_list = [['page', 'link', 'text', 'code', 'error']]
    mglinks_list = [['page', 'link', 'code', 'text']]
    page_num_tot = len(link_set)
    page_num = 0
    link_num = 0
    ultimate_links =[]
    for link in link_set:
        page_num += 1
        # if page_num == 2: break # for testing
        all_links = ret_all_link(link)
        print(all_links)
        try:
            for link_pair in all_links:
                ultimate_links.append(link_pair)
                if link_pair[0].find('www.genealogy.math.ndsu.nodak.edu') >= 0:
                    mglinks_list.append(find_math_genea(link, link_pair))
                pair = check(link_pair)
                if pair:
                    list_towrite = ["https://www.informs.org" + link] + pair
                    list_towrite = check_list(list_towrite)
                    link_num += 1
                    links_list.append(list_towrite)
                    #print(list_towrite)
            print("Page number: " + str(page_num) + "/" + str(page_num_tot) + " Link number: " + str(link_num))
        except TypeError as e:
            pdb.set_trace()
            print("Caught TypeError")

    # links_list.to_pickle("dead_link.pkl")
    links_df = pd.DataFrame(links_list, columns=('page', 'link', 'text', 'code', 'error'))
    mglinks_df = pd.DataFrame(mglinks_list, columns=('page', 'link', 'code', 'text'))
    ultlinks_df = pd.DataFrame(ultimate_links, columns=('all', 'next'))
    # df = links_df[links_df['code'] != 200]
    output_dead_link(links_df, mglinks_df, ultlinks_df)
    print("Finished! Total of", link_num, "dead links are found.\n", "Excel file generated under", os.getcwd())
    return


def output_dead_link(df, mgdf=pd.DataFrame(), ultldf=pd.DataFrame()):
    time = str(datetime.datetime.now())[:-7]
    writer = pd.ExcelWriter('dead links ' + time.replace(':', '‘') + '.xlsx', engine='xlsxwriter')
    df.to_excel(writer, header=False, index=False, sheet_name='inform')
    workbook = writer.book
    worksheet = writer.sheets['inform']
    text_format = workbook.add_format({'text_wrap': False})
    title_format = workbook.add_format({'text_wrap': True})
    title_format.set_bold()  # Turns bold on.
    title_format.set_align('top')
    worksheet.set_row(0, None, title_format)
    worksheet.set_column('A:A', 80, text_format)
    worksheet.set_column('B:B', 80, text_format)
    worksheet.set_column('C:C', 20, text_format)
    worksheet.set_column('D:D', 8, text_format)
    worksheet.set_column('E:E', 80, text_format)
    worksheet.freeze_panes(1, 0)  # Freeze first row and first 2 columns.
    mgdf.to_excel(writer, sheet_name='math genea links')
    mathg = writer.sheets['math genea links']
    ultldf.to_excel(writer, sheet_name='all the links')
    writer.save()
    print("Finished! Excel file generated under", os.getcwd(), "\n")
