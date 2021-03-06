#!/usr/bin/python
########################################################
# Collect contents of given issue list
# and export them to the HTML file.
#
# sMiLo / 2014.08.14
########################################################

from bs4 import BeautifulSoup
from urllib2 import urlopen, URLError
import mechanize
from ClientForm import ParseResponse

########################################################
USER_ID = 'ID_HERE'
USER_PW = 'PW_HERE'

ISSUE_LIST = [1,2,3,4,5]

URL_LOGIN = 'https://LOGIN_URL_HERE/redmine/login'
URL_ISSUE = 'https://ISSUE_URL_HERE/redmine/issues/'

RESULT_FILE = "RedmineIssueCrawlingResult.html"

########################################################
def loginRedmine():
	forms = ParseResponse(urlopen(URL_LOGIN))
	form = forms[0]
	form['username'] = USER_ID
	form['password'] = USER_PW
	request = form.click()
	mechanize.urlopen(request)

########################################################
def generateIndex(soup, i):
	for item in  soup.findAll('div', attrs={'class':'subject'}):
		subject = item.get_text().encode('utf-8')
	print subject
	return ('<li><a href=#' + str(i) + '>' + str(i) + '.' + subject + '</a></li>')

########################################################
def generateList(soup, i):
	# Remove useless items
	for item in soup.find_all('div', attrs={'class':'contextual'}):
		item.decompose()
	for item in soup.find_all('a', attrs={'class':'delete'}):
		item.decompose()
	for item in soup.find_all('p', attrs={'class':'other-formats'}):
		item.decompose()
	for item in soup.find_all('script'):
		item.decompose()
	for item in soup.find_all('td', attrs={'class':'buttons'}):
		item.decompose()
	
	article = str( soup('div', {'id':'content',}) )
	return ('<a name=' + str(i) + '></a>' + article)

########################################################
if __name__ == '__main__':
	
	loginRedmine()

	htmlHead = "<!DOCTYPE HTML><html lang=ko><head><meta http-equiv=Content-Type content=text/html; charset=utf-8></head><body>"
	htmlBodyIndex = ""
	htmlBodyList = ""
	htmlFoot = "</body></html>"
	
        for i in ISSUE_LIST:
		# Parse given html file using BeautifulSoup
		url = URL_ISSUE + str(i)
		try:
			response = mechanize.urlopen(url)
		except URLError, e:
			if hasattr(e, 'code'):
				if e.code==408:
					print 'Timeout ', url
				elif e.code==404:
					print 'File Not Found ', url
				continue
		data = response.read()
		soup = BeautifulSoup(data)
		print url
		
		# Generate index of subjects
		htmlBodyIndex += generateIndex(soup, i)
		
		# Generate issue list
		htmlBodyList += generateList(soup, i)
		
		# Close Client cookie
		response.close()
	
	f = open(RESULT_FILE, 'w')
	f.write(htmlHead)
	f.write(htmlBodyIndex)
	f.write(htmlBodyList)
	f.write(htmlFoot)
	f.close()

