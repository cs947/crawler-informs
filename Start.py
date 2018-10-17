from Crawler import find_info
from methodCrawler import find_method_info
from Links import find_internal_links, generate_link_dataframe
from institutions import find_inst_info

control = "continue"
info = "Choose command from following list\n"\
       "-- binfo : Generate a spreadsheet of biographical profiles Approx. 15 mins\n" \
       "-- ainfo : Generate a spreadsheet of Academic Institutions links info Approx 5 mins\n" \
       "-- noainfo : Generate a spreadsheet of Non Academic Institutions links info Approx 5 mins\n" \
       "-- appinfo : Generate a spreadsheet of Application Areas links info Approx 5 mins\n" \
       "-- minfo : Generate a spreadsheet of Methodologies links info Approx 5 mins\n" \
       "-- find : Find all the pages under informs. Approx. 10 mins\n" \
       "-- link : Output dead links after 'find' is excuted. Approx. 4 hrs\n" \
       "-- exit : Exit the program\n"

print(info)

while True:

    control = input("Please input command\n")

    if control == "exit":
        print("Exited the program\n")
        break

    elif control == "binfo":
        find_info()
    elif control == "find":
        find_internal_links()
    elif control == "link":
        generate_link_dataframe()
    elif control == "minfo" or control == "ainfo" or control == "noainfo" or control == "appinfo" :
        find_method_info(control)
    else:
        print("Command not recognized\n")

    print(info)
