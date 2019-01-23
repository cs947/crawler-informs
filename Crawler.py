import requests
from bs4 import BeautifulSoup
import Functions as f
import pandas as pd
import datetime
import os


def find_info():
    # creates the excel spreadsheet of biographical profiles
    group_letters = ['A', 'C', 'F', 'I', 'M', 'O', 'S', 'V'] #comment for testing
    personal_links = f.bfind_links(group_letters)
    time = str(datetime.datetime.now())[:-7]
    print(time)
    toWrite = [['Last Name', 'First Name', 'Year', 'Birth Date', 'Death Date', 'Main Photo', 'Brief Bio Word Count',
                        'Other Bio', 'Wikipedia', 'Education', 'Mathematics Genealogy',
                        'Historic Academic Institutions',
                        'Additional Academic Institutions', 'Historic Non-Academic Institutions',
                        'Additional Non-Academic Institutions', 'Historic Methodologies', 'Other Methodologies',
                        'Historic Application Areas', 'Other Application Areas', 'Image Gallery', 'Image Count', 'Resumes',
                        'Oral History Interview in INFORMS Format', 'Oral History Interview - Other - Embedded',
                        'Oral History Interview - Other - Reference', 'Memoir', 'Obituaries', 'Awards and Honors',
                        'Professional Service', 'Library Archives', 'Selected Publications', 'Additional Resources']]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    j = 0
    for i in personal_links:
        print()
        try:
            source_code = requests.get(i, headers = headers)
            text = source_code.text
            parse = BeautifulSoup(text, "html.parser")
            nameDate = f.find_date(parse)
            acaIns = f.academic_ins(parse)
            nonAcaIns = f.non_academic_ins(parse)
            meth = f.methodologies(parse)
            appl = f.app_areas(parse)
            img_gal = f.if_img_gall(parse)
            # image = f.image_gall(parse)
            interview = f.oral_hist(parse)

            final = [nameDate[0], nameDate[1], nameDate[2], nameDate[3], nameDate[4],
                            f.if_biophoto(parse), f.bio_word_count(parse),
                            f.other_bio(parse), f.wiki_link(parse), f.education(parse), f.genealogy(parse), acaIns[0],
                            acaIns[1],
                            nonAcaIns[0], nonAcaIns[1], meth[0], meth[1], appl[0], appl[1], img_gal, 'hold', f.resume(parse),
                            interview[0], interview[1], interview[2], f.memoirs(parse), f.obituaries(parse),
                            f.awards(parse),
                            f.prof_service(parse), f.archives(parse), f.pub_no(parse), f.add_resources(parse)]
            toWrite.append(final)
        except AttributeError as a:
            print(a)
            print(final)
            print("acaIns " + str(acaIns))
            print("nonacaIns " + str(nonAcaIns))
            print("meth " + str(meth))
            print("appl " + str(appl))
            print("images " + str(image))
            print("oralhist " + str(interview))
            j = j + 1
            personal_links.append(i)

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

    worksheet.set_row(1, None, title_format)
    worksheet.set_column('A:X', 16, text_format)
    # worksheet.set_column('E:E', 8, text_format)
    # worksheet.set_column('F:F', 8, text_format)
    # worksheet.set_column('G:G', 50, text_format)
    # worksheet.set_column('H:H', 40, text_format)
    # worksheet.set_column('I:I', 50, text_format)
    # worksheet.set_column('J:J', 50, text_format)
    # worksheet.set_column('K:K', 50, text_format)
    # worksheet.set_column('L:L', 50, text_format)
    # worksheet.set_column('M:M', 20, text_format)
    # worksheet.set_column('N:N', 35, text_format)
    # worksheet.set_column('O:O', 35, text_format)
    # worksheet.set_column('P:P', 8, text_format)
    # worksheet.set_column('Q:Q', 30, text_format)
    # worksheet.set_column('R:R', 8, text_format)
    # worksheet.set_column('S:S', 8, text_format)
    # worksheet.set_column('T:T', 8, text_format)
    # worksheet.set_column('U:U', 8, text_format)
    # worksheet.set_column('V:V', 8, text_format)
    # worksheet.set_column('W:W', 20, text_format)
    # worksheet.set_column('X:X', 50, text_format)
    #worksheet.set_column('W:Z', 20, text_format)
    worksheet.set_column('W:AF', 20, text_format)
    worksheet.freeze_panes(1, 1)  # Freeze first row and first column.

    writer.save()
    print("Finished! Excel file generated under", os.getcwd(), "\n")
