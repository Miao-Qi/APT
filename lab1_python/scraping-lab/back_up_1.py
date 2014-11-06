import json
import sys
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

file_name = open("f.dat")
file_data = file_name.read()
soup = BeautifulSoup(file_data)

#get current value
tag = soup.find("span", class_="time_rtq_ticker")
current_value = tag.string

#get URL
for link in soup.find_all("a", text=re.compile("[A-Z][a-z][a-z]\s[0-9][0-9]")):
    print link

#get all header
header_list = []
for tag in soup.find_all(class_="yfnc_tablehead1"):
   if tag.get_text() not in header_list:
      header_list.append(tag.get_text())
header_tuples = tuple(header_list)

print current_value
print soup.find("span", class_="time_rtq_ticker")
print type(soup.find("span", class_="time_rtq_ticker"))