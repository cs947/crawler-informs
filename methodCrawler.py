import requests
from bs4 import BeautifulSoup
import Functions as f
import pandas as pd
import datetime
import os

def find_method_info(info):
    thisdict =	{
        "ainfo": 'Academic-Institutions/',
        "noainfo": 'Non-Academic-Institutions/',
        "appinfo": 'O.R.-Application-Areas/',
        "minfo": 'O.R.-Methodologies/',
    }

    toWrite = [['Title', 'Logo', 'Description', 'Desc Word Count', 'Links and References', 'Indivs. Count',
                        'Oral History Interview in INFORMS Format', 'Oral History Interview - Other - Embedded',
                        'Oral History Interview - Other - Reference',
                        'Memoirs and Autobiographies', 'Library Archives']]
    time = str(datetime.datetime.now())[:-7]
    print(time)
    writer = pd.ExcelWriter(thisdict[info][:-1] + ' ' + time.replace(':', '‘') + '.xlsx', engine='xlsxwriter')


    m_links = f.find_m_links(thisdict[info])
    print(m_links)
    for i in m_links:
        print(i)
        source_code = requests.get(i)
        text = source_code.text
        parse = BeautifulSoup(text, "html.parser")
        body = parse.find("div", {"class": "content-container"})
        title = f.find_title(parse)
        is_logo = f.find_logo(parse)
        desc_word_count = f.desc_word_count(parse)
        indiv_count = f.indiv_count(body)
        interview = f.oral_hist(parse)

        toWrite.append([title, is_logo, desc_word_count[0], desc_word_count[1], f.linksandrefs(parse),
                        indiv_count, interview[0], interview[1], interview[2],
                        f.memoirs3(parse),
                        f.archives(parse)])

    df = pd.DataFrame(toWrite)

    df.to_excel(writer, header=False, index=False, sheet_name='methodologies')

    workbook = writer.book
    method = writer.sheets['methodologies']
    text_format = workbook.add_format({'text_wrap': True})
    text_format.set_align('top')
    # celld2 = workbook.cell('D2')
    # celld2.set_align('right')
    title_format = workbook.add_format({'text_wrap': True})
    title_format.set_bold()  # Turns bold on.
    title_format.set_align('top')

    method.set_column('A:A', 30, text_format)

    method.freeze_panes(1, 1)  # Freeze first row and first 2 columns.
    writer.save()
    print("Finished! Excel file generated under", os.getcwd(), "\n")
