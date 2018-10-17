import requests
from bs4 import BeautifulSoup
import Functions as f
import pandas as pd
import datetime
import os

def find_inst_info(area):

    toWrite = [['Title', 'Description', 'Desc Word Count', 'Links and References',
                        'Oral History Interview in INFORMS Format', 'Oral History Interview - Other - Embedded',
                        'Oral History Interview - Other - Reference',
                        'Memoirs and Autobiographies', 'Library Archives']]
    time = str(datetime.datetime.now())[:-7]
    print(time)
    writer = pd.ExcelWriter('Institutions Analysis ' + time.replace(':', '‘') + '.xlsx', engine='xlsxwriter')

    m_page = ['', '(offset)/20']
    for m in m_page:
        m_links = f.find_m_links(area, m_page)



    for i in m_links:
        source_code = requests.get(i)
        text = source_code.text
        parse = BeautifulSoup(text, "html.parser")
        title = f.find_title(parse)
        desc_word_count = f.desc_word_count(parse)
        interview = f.oral_hist(parse)

        toWrite.append([title, desc_word_count[0], desc_word_count[1], f.linksandrefs(parse),
                        interview[0], interview[1], interview[2],
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
    method.freeze_panes(2, 1)  # Freeze first row and first 2 columns.

    writer.save()
    print("Finished! Excel file generated under", os.getcwd(), "\n")
