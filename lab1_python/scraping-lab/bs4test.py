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
data_dict = {}

'''
#get current value
tag = soup.find("span", class_="time_rtq_ticker")
current_value = tag.string
data_dict['currPrice'] = current_value
print data_dict
'''

'''
url_header = "http://finance.yahoo.com/"
data_dict["dateUrls"] = []
#get URL
for link in soup.find_all("a", text=re.compile("[A-Z][a-z][a-z]\s[0-9][0-9]")):
   link_convert = str(link)
   new_link_re = re.search("(?<=href=\")(..*[0-9][-][0-9][0-9])",link_convert)
   new_link = str(new_link_re.group(0))
   #print new_link
   url_list = data_dict["dateUrls"]
   url_list.append(url_header+new_link)
   data_dict["dateUrls"] = url_list

#print data_dict

link = soup.find("p", text=re.compile("Expand to "))
link_convert = str(link)
new_link_re = re.search("(?<=href=\")(..*[0-9][-][0-9][0-9])",link_convert)
new_link = str(new_link_re.group(0))
url_list = data_dict["dateUrls"]
url_list.append(url_header+new_link)
data_dict["dateUrls"] = url_list

print data_dict
'''

'''
#for tag in soup.find_all("strong", class_="yfi-module-title"):
#for tag in (soup.find_all("td", class_="yfnc_h") or soup.find_all("strong", class_="yfi-module-title")):    
   #print tag.get_text()
tag = soup.find("strong", class_="yfi-module-title")
new_tag = tag.next_element
new_tag1 = new_tag.next_element
new_tag2 = new_tag1.next_element
data_tag = new_tag2.next_element
print tag, type(tag)
print new_tag, type(new_tag)
print new_tag1, type(new_tag1)
print new_tag2, type(new_tag1)

for tag in data_tag.find_all("td", class_="yfnc_h"):
#for tag in (soup.find_all("td", class_="yfnc_h") or soup.find_all("strong", class_="yfi-module-title")):    
   print tag.get_text()
#print new_tag4, type(new_tag1)
'''

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

for tag in c_data_tag.find_all("td", class_="yfnc_h"):   
   print tag.get_text()


'''    
#for tag in (soup.find_all("td", class_="yfnc_h") or soup.find_all("strong", class_="yfi-module-title")):    
   #print tag.get_text()
tag = soup.find("strong", class_="yfi-module-title")
new_tag = tag.next_element
new_tag1 = new_tag.next_element
new_tag2 = new_tag1.next_element
data_tag = new_tag2.next_element
print tag, type(tag)
print new_tag, type(new_tag)
print new_tag1, type(new_tag1)
print new_tag2, type(new_tag1)

for tag in data_tag.find_all("td", class_="yfnc_h"):
#for tag in (soup.find_all("td", class_="yfnc_h") or soup.find_all("strong", class_="yfi-module-title")):    
   print tag.get_text()
#print new_tag4, type(new_tag1)  
'''
#print soup_text
#print call_options_data
#print file_data
#print soup_text
