from Crawler import find_info
from methodCrawler import find_method_info
from Links import find_internal_links, generate_link_dataframe
from institutions import find_inst_info

control = "continue"
info = "Choose command from following list\n"\
       "-- all : Executes all of the below commands\n" \
       "-- binfo : Generate a spreadsheet of biographical profiles Approx. 5 mins\n" \
       "-- ainfo : Generate a spreadsheet of Academic Institutions links info Approx. 5 mins\n" \
       "-- noainfo : Generate a spreadsheet of Non Academic Institutions links info Approx. 5 mins\n" \
       "-- appinfo : Generate a spreadsheet of Application Areas links info Approx. 5 mins\n" \
       "-- minfo : Generate a spreadsheet of Methodologies links info Approx. 5 mins\n" \
       "-- find : Find all the pages under informs. Approx. 10 mins\n" \
       "-- link : Output dead links after 'find' is excuted. Approx. 4 hrs\n" \
       "-- exit : Exit the program\n"

print(info)

while True:

    control = input("Please input command\n")

    if control == "exit":
        print("Exited the program\n")
        break
    elif control == "all":
        find_info()
        find_internal_links()
        generate_link_dataframe()
        find_method_info("minfo")
        find_method_info("ainfo")
        find_method_info("noainfo")
        find_method_info("appinfo")
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
