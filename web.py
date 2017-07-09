import urllib2
def download(url,user_agent="wswp",num_retries=2):
	print('Download:',url)
	headers={'User-agent':user_agent}
	request=urllib2.Request(url,headers=headers)
	try:
		html=urllib2.urlopen(request).read()
	except urllib2.URLError as e:
		print('Download error:',e.reason)
		html=None
		if num_retries>0:
			if hasattr(e,'code') and 500<=e.code<600:
				return download(url,user_agent,num_retries-1)
	return html

	
#解析robots.txt文件，以避免瞎子啊禁止爬取的URL
import robotparser
rp=robotparser.RobotFileParser()
rp.set_url('')
rp.read()
url="http;//"
user_agent="BadCrawer"


#链接爬虫
import re
def link_craw(seed_url,link_regex):
	craw_queue=[seed_url]
	seen=set(craw_queue)
	while craw_queue:
		url=craw_queue.pop()
		html=download(url)
		for	link in get_links(html):
			if re.match(link_regex,link):
				link=urlparse.urljoin(seed_url,link)
				if link not in seen:
					seen.add(link)
					craw_queue.append(link)

					
def get_links(html):
	webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
	return webpage_regex.findall(html)