import json
import sys
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def is_short_string(string):
    return len(string) < 50
only_short_strings = SoupStrainer(text=is_short_string)

file_name = open("f.dat")

file_data = file_name.read()

soup = BeautifulSoup(file_data)

data_title = soup.title.name

#file_data_text = soup.get_text()

'''

tag = soup.find("span", class_="time_rtq_ticker")

current_value = tag.string

print current_value
print soup.find("span", class_="time_rtq_ticker")
print type(soup.find("span", class_="time_rtq_ticker"))
'''

#try = soup.find(class="time_rtq_ticker")

#print try


#print data_title
#print type(data_title)

#find_data = soup.find_all('td', class_="yfnc_tabledata1")

#text = soup.string

soup_text = BeautifulSoup(file_data, "html.parser", parse_only=only_short_strings).prettify()


call_options_i = soup_text.find("Call Options")
put_options_i = soup_text.find("Put Options")
open_int_i = soup_text.find("Open Int")
call_options = soup_text[call_options_i:put_options_i]
put_options = soup_text[put_options_i:]
call_options_data = soup_text[open_int_i+9:put_options_i]
header = soup_text[call_options_i:open_int_i+9]

#get all header
header_list = []
for tag in soup.find_all(class_="yfnc_tablehead1"):
   if tag.get_text() not in header_list:
      header_list.append(tag.get_text())

header_tuples = tuple(header_list) 

print header_tuples
#for link in soup.find_all("td", class_="yfnc_h"):
    #print link

#print soup_text
#print call_options_data
#print file_data
#print soup_text
