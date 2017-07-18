#2017年7月17日23点18分

#添加代理功能
#2017年7月18日21点32分，加入下载限速功能
import urllib2
def download(url,user_agent="wswp",proxy=None,num_retries=2):
	print('Download:',url)
	headers={'User-agent':user_agent}
	request=urllib2.Request(url,headers=headers)#返回请求信息，包含url，header，post等信息,构造请求头
	#proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})null_proxy_handler = urllib2.ProxyHandler({})
	#一般我们直接调用urlopen()就是表示去调用build_opener()方法，然后用build_opener()方法返回的类对象去调用该对象的open方法
	opener=urllib2.build_opener()
	if proxy:
		proxy_params={urlparse.urlparse(url).scheme:proxy}#模式为代理？
		opener.add_handler(urllib2.ProxyHandler(proxy_params))#加入代理信息
	try:
		html=urllib2.urlopen(request).read()
	except urllib2.URLError as e:
		print('Download error:',e.reason)
		html=None
		if num_retries>0:
			if hasattr(e,'code') and 500<=e.code<600:
				return download(url,user_agent,num_retries-1)
	return html
#下载限速
import datetime
import time
class Throttle:
	'''在两次访问相同域名时加一个访问时间限制'''
	def __init__(self,delay):
		#限制的时间
		self.delay=delay
		#最后一次访问的时间
		self.domains={}

	def wait(self,url):
		domain=urlparse.urlparse(url).netloc
		last_accessed=self.domains.get(domain)
		if self.delay>0 and last_accessed is not None:
			sleep_secs= self.delay - (datetime.datetime.now()-last_accessed).seconds
			if sleep_secs>0 :
				#需要休眠
				time.sleep(sleep_secs)
		self.domains[domain]=datetime.datetime.now()#更新上次访问时间





#避免重复下载
#解析robots.txt文件，以避免瞎子啊禁止爬取的URL
import robotparser
rp=robotparser.RobotFileParser()
rp.set_url('')
rp.read()
url="http;//"
user_agent="BadCrawer"


#链接爬虫
import re
import urlparse
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