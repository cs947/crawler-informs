import requests
from bs4 import BeautifulSoup
import Functions as f
import pandas as pd
import datetime
import os


m_links = ['https://www.informs.org/Explore/History-of-O.R.-Excellence/O.R.-Methodologies/Mathematical-Programming']
time = str(datetime.datetime.now())[:-7]
print(time)
toWrite = [['Title', 'Description', 'Desc Word Count', 'Links and References',
                    'Oral History Interview in INFORMS Format', 'Oral History Interview - Other - Embedded',
                    'Oral History Interview - Other - Reference',
                    'Memoirs and Autobiographies', 'Library Archives']]
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
writer = pd.ExcelWriter('inform bio ' + time.replace(':', '‘') + '.xlsx', engine='xlsxwriter')
df.to_excel(writer, header=False, index=False, sheet_name='inform')
workbook = writer.book
worksheet = writer.sheets['inform']
text_format = workbook.add_format({'text_wrap': True})
text_format.set_align('top')

title_format = workbook.add_format({'text_wrap': True})
title_format.set_bold()  # Turns bold on.
title_format.set_align('top')
worksheet.freeze_panes(2, 2)  # Freeze first row and first 2 columns.

writer.save()
print("Finished! Excel file generated under", os.getcwd(), "\n")
