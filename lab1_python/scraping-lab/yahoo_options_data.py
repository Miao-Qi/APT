import json
import sys
import re
import urllib 
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def data_save(Option_type, tag_type, class_type, data_tag, set_mod, dest_addr, header_mod):
   element_counter = 0
   set_mod["Type"] = Option_type
   for tag in data_tag.find_all(tag_type, class_=class_type): 
      if element_counter == 1 :
         full_symbol = tag.get_text()
         first_digit_match = re.search("\d", full_symbol)
         first_digit_index = first_digit_match.start()
         if full_symbol[first_digit_index] == "7" :
            first_digit_index += 1
         set_mod["Symbol"] = full_symbol[0 : first_digit_index]
         set_mod["Date"] = full_symbol[first_digit_index : first_digit_index+6]
    	 element_counter += 1
      elif element_counter == 7 :
         set_mod[header_mod[element_counter]] = tag.get_text()
         new_set = set_mod.copy()
         all_sets_list = dest_addr["optionQuotes"]
         all_sets_list.append(new_set)
         dest_addr["optionQuotes"] = all_sets_list
         element_counter = 0
      else:   
         set_mod[header_mod[element_counter]] = tag.get_text()
         element_counter += 1  
  

def contractAsJson(filename):
  jsonQuoteData = "[]"
  file_name = open(filename)
  file_data = file_name.read()
  soup = BeautifulSoup(file_data)
  
  
  # final storage place
  # data_dict = {"currPrice","dateUrls","optionQuotes"}
  data_dict = {}
  
  
  # get current value
  tag = soup.find("span", class_="time_rtq_ticker")
  current_value = unicode(tag.string)
  if "," in current_value:
    new_current_value = current_value[:current_value.index(",")] + current_value[current_value.index(",")+1:]
    current_value = new_current_value  
  if "," in current_value:
    new_current_value = current_value[:current_value.index(",")] + current_value[current_value.index(",")+1:]
    current_value = new_current_value     
  data_dict["currPrice"] = float(current_value.encode('ascii','ignore'))  
  
  
  # get URL
  url_header = "http://finance.yahoo.com"
  data_dict["dateUrls"] = []
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
  
  
  # get Quote Options
  # get all header
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
  
  
  # get all strikes' data
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
  
  data_save(Option_type = "C", tag_type = "td", class_type = "yfnc_h", data_tag = c_data_tag, set_mod = contract_dict, dest_addr = data_dict, header_mod = header_tuples)
  data_save(Option_type = "C", tag_type = "td", class_type = "yfnc_tabledata1", data_tag = c_data_tag, set_mod = contract_dict, dest_addr = data_dict, header_mod = header_tuples)
  data_save(Option_type = "P", tag_type = "td", class_type = "yfnc_h", data_tag = p_data_tag, set_mod = contract_dict, dest_addr = data_dict, header_mod = header_tuples)
  data_save(Option_type = "P", tag_type = "td", class_type = "yfnc_tabledata1", data_tag = p_data_tag, set_mod = contract_dict, dest_addr = data_dict, header_mod = header_tuples)   
   
  
  # sort QuoteOptions	
  def MyKey(s):
    final_s = s["Open"][:]
    if "," in final_s:
      new_s = final_s[:final_s.index(",")] + final_s[final_s.index(",")+1:]
      final_s = new_s
    if "," in final_s:
      new_s = final_s[:final_s.index(",")] + final_s[final_s.index(",")+1:]
      final_s = new_s
    return int(final_s)
	
  all_sets_list = data_dict["optionQuotes"]
  sorted_list_strike = sorted(all_sets_list, key=lambda k: (k['Type'], float(k['Strike'])))
  sorted_list = sorted(sorted_list_strike, key = MyKey, reverse = True)
  data_dict["optionQuotes"] = sorted_list  	 

  
  # dump to json format
  jsonQuoteData = json.dumps(data_dict, indent=4, sort_keys=True) 
  return jsonQuoteData

