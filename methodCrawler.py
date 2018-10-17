import requests
from bs4 import BeautifulSoup
import Functions as f
import pandas as pd
import datetime
import os

def find_method_info():

    toWrite = [['Title', 'Description', 'Desc Word Count', 'Links and References', 'Indivs. Count',
                        'Oral History Interview in INFORMS Format', 'Oral History Interview - Other - Embedded',
                        'Oral History Interview - Other - Reference',
                        'Memoirs and Autobiographies', 'Library Archives']]
    time = str(datetime.datetime.now())[:-7]
    print(time)
    writer = pd.ExcelWriter('Content Analysis ' + time.replace(':', '‘') + '.xlsx', engine='xlsxwriter')
    contentarea = ['Academic-Institutions/', 'Non-Academic-Institutions/' ,
                    'O.R.-Application-Areas', 'O.R.-Methodologies/']

    thisdict =	{
        "minfo": 'O.R.-Methodologies/',
        "model": "Mustang",
        "year": 1964
        }
    # m_page = ['', '(offset)/20']
    m_page = ['', '(offset)/20']
    m_links = f.find_m_links(thisdict["minfo"], m_page)
    print(m_links)
    for i in m_links:
        print(i)
        source_code = requests.get(i)
        text = source_code.text
        parse = BeautifulSoup(text, "html.parser")
        body = parse.find("div", {"class": "body"})
        title = f.find_title(parse)
        print(title)
        desc_word_count = f.desc_word_count(parse)
        indiv_count = f.indiv_count(body)
        interview = f.oral_hist(parse)

        toWrite.append([title, desc_word_count[0], desc_word_count[1], f.linksandrefs(parse),
                        indiv_count, interview[0], interview[1], interview[2],
                        f.memoirs3(parse),
                        f.archives(parse)])

    df = pd.DataFrame(toWrite)

    df.to_excel(writer, header=False, index=False, sheet_name='methodologies')

    workbook = writer.book
    method = writer.sheets['methodologies']

    text_format = workbook.add_format({'text_wrap': True})
    text_format.set_align('top')

    title_format = workbook.add_format({'text_wrap': True})
    title_format.set_bold()  # Turns bold on.
    title_format.set_align('top')
    method.freeze_panes(1, 1)  # Freeze first row and first 2 columns.

    writer.save()
    print("Finished! Excel file generated under", os.getcwd(), "\n")
