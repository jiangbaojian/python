__author__ = 'qingdaopijui'
from bs4 import BeautifulSoup
broken_html='<ul class=country><li>Area<li>Population</ul>'
soup=BeautifulSoup(broken_html,'html.parser')
fixed_html=soup.prettify()
print fixed_html
#beautifulsoup能够正确的解析确实的html标签，并补齐