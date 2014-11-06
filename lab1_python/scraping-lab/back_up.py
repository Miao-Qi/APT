from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def is_short_string(string):
    return len(string) < 50

file_name = open(filename)

file_data = file_name.read()

soup = BeautifulSoup(file_data)

find_data = soup.find_all('td', class_="yfnc_tabledata1")

text = soup.string

only_short_strings = SoupStrainer(text=is_short_string)

soup_text = BeautifulSoup(file_data, "html.parser", parse_only=only_short_strings).prettify()


#print file_data
print soup_text
