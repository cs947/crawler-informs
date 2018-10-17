from Crawler import find_info
from methodCrawler import find_method_info
from Links import find_internal_links, generate_link_dataframe
from institutions import find_inst_info

control = "continue"
info = "Choose command from following list\n"\
       "-- binfo : Generate a spreadsheet of personal information Approx. 15 min\n" \
       "-- minfo : Generate a spreadsheet of Methodologies links info\n" \
       "-- find : Find all the pages under informs. Approx. 10 min\n" \
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
    elif control == "minfo":
        find_method_info()
    elif control == "ainfo":
        find_inst_info(control)
    else:
        print("Command not recognized\n")

    print(info)
