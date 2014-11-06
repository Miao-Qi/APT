import json
import sys
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

dump_file = open("output", "w")

file_name = open("f.dat")
file_data = file_name.read()
soup = BeautifulSoup(file_data)

#data_dict = {"currPrice","dateUrls","optionQuotes"}
data_dict = {}

#get current value
tag = soup.find("span", class_="time_rtq_ticker")
current_value = tag.string
data_dict["currPrice"] = current_value

url_header = "http://finance.yahoo.com/"
data_dict["dateUrls"] = []
#get URL
for link in soup.find_all("a", text=re.compile("[A-Z][a-z][a-z]\s[0-9][0-9]")):
   link_convert = str(link)
   new_link_re = re.search("(?<=href=\")(..*[0-9][-][0-9][0-9])",link_convert)
   new_link = str(new_link_re.group(0))
   url_list = data_dict["dateUrls"]
   url_list.append(url_header+new_link)
   data_dict["dateUrls"] = url_list
link = soup.find("p", text=re.compile("Expand to "))
link_convert = str(link)
new_link_re = re.search("(?<=href=\")(..*[0-9][-][0-9][0-9])",link_convert)
new_link = str(new_link_re.group(0))
url_list = data_dict["dateUrls"]
url_list.append(url_header+new_link)
data_dict["dateUrls"] = url_list
   
data_dict["optionQuotes"] = [] 
contract_tuple = ("Ask","Bid","Change","Date","Last","Open","Strike","Symbol","Type","Vol")
contract_dict = dict.fromkeys(contract_tuple)

#get all header
header_list = []
for tag in soup.find_all(class_="yfnc_tablehead1"):
   new_item = tag.get_text()
   if new_item == "Chg":
      new_item = "Change"
   elif new_item == "Open Int":
      new_item = "Open"
   if new_item not in header_list:
      header_list.append(new_item)
header_tuples = tuple(header_list)

#get all strikes' data
title_tag = []
for tag in soup.find_all("strong", class_="yfi-module-title"):
    title_tag.append(tag)


new_tag = title_tag[0].next_element
new_tag1 = new_tag.next_element
new_tag2 = new_tag1.next_element
c_data_tag = new_tag2.next_element

new_tag = title_tag[1].next_element
new_tag1 = new_tag.next_element
new_tag2 = new_tag1.next_element
p_data_tag = new_tag2.next_element


#save the Call Options into list of dictionary
element_counter = 0
contract_dict["Type"] = "C"
for tag in c_data_tag.find_all("td", class_="yfnc_h"): 
   if element_counter == 1 :
      full_symbol = tag.get_text()
      first_digit_match = re.search("\d", full_symbol)
      first_digit_index = first_digit_match.start()
      contract_dict["Symbol"] = full_symbol[0 : first_digit_index]
      if full_symbol[first_digit_index] == 7 :
	     first_digit_index += 1
      contract_dict["Date"] = full_symbol[first_digit_index : first_digit_index+6]
   else:   
      contract_dict[header_tuples[element_counter]] = tag.get_text()
   element_counter += 1
   if element_counter == 8 :
      all_sets_list = data_dict["optionQuotes"]
      all_sets_list.append(contract_dict)
      data_dict["optionQuotes"] = all_sets_list
      element_counter = 0
	  
#save the Put Options into list of dictionary
element_counter = 0
contract_dict["Type"] = "P"
for tag in p_data_tag.find_all("td", class_="yfnc_h"): 
   if element_counter == 1 :
      full_symbol = tag.get_text()
      first_digit_match = re.search("\d", full_symbol)
      first_digit_index = first_digit_match.start()
      contract_dict["Symbol"] = full_symbol[0 : first_digit_index]
      if full_symbol[first_digit_index] == 7 :
	     first_digit_index += 1
      contract_dict["Date"] = full_symbol[first_digit_index : first_digit_index+6]
   else:   
      contract_dict[header_tuples[element_counter]] = tag.get_text()
   element_counter += 1
   if element_counter == 8 :
      all_sets_list = data_dict["optionQuotes"]
      all_sets_list.append(contract_dict)
      data_dict["optionQuotes"] = all_sets_list
      element_counter = 0	  

json.dump(data_dict, fp=dump_file, indent=4,  sort_keys=True)
	  
'''   
for tag in p_data_tag.find_all("td", class_="yfnc_h"):   
   print tag.get_text()
'''
#print current_value
#print soup.find("span", class_="time_rtq_ticker")
#print type(soup.find("span", class_="time_rtq_ticker"))