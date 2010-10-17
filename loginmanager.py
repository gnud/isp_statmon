#!/usr/bin/python
# -*- coding: utf-8 -*-
# Temporary here, until moved in it's own py module.
import urllib2, logging, sys
from urllib2 import urlopen, Request, HTTPHandler, HTTPSHandler
from urllib import urlencode
from BeautifulSoup import BeautifulSoup
from datetime import datetime

class Login(object):
  def __init__(self):
    '''Constructor'''

    super(Login, self).__init__()
    self.username = ""
    self.password = ""
    self.server = ""
  def set_username(self, user):
    '''Sets the name of the user.
    user : the login name of the user.'''

    self.username = user
  def get_username(self):
    '''Gets the name of the user.'''

    return self.username
  def set_password(self, password):
    '''Sets the content of the password.
    password : the content of the password.'''
    
    self.password = password
  def get_password(self):
    '''Gets the content of the password.'''

    return self.password
  def set_server(self, server):
    '''Sets the url of the server.
    server : the url of the server.'''

    self.server = server
  def get_server(self):
    '''Gets the url of the server.'''

    return self.server

class ThomeLogin(Login):
  def __init__(self):
    '''Constructor'''

    super(ThomeLogin, self).__init__()
    self.socket = None    
    self.get_months_url = 'https://moj.telekom.mk/ADSL.aspx?id_page=0&__EVENTARGUMENT=&__EVENTTARGET=ctl00%24cphMain%24ctl00%24cmbMonth&__EVENTVALIDATION=%2FwEWCwK0%2B%2BOkAQKTkJSmAgK0vOK0AQKZv7y5CwLyv8qeDwKe1ee9AQKe1eu9AQKe1d%2B9AQKe1eO9AQKe1de9AQKe1du9ARlYvLl7hd43rfB8VIM%2BJtzc9UjZ&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwULLTIxMDQ3MDY0NTEPFgIeCkxhc3RMb2FkZWQFH34vVXNlckNvbnRyb2xzL0FEU0xUcmFmZmljLmFzY3gWAmYPZBYCAgMPZBYIAgUPZBYCZg9kFgICAQ9kFgICAQ9kFgJmDxYCHgRUZXh0Bc0BPGxpIGNsYXNzPSJsZWZ0Ij48dWwgY2xhc3M9ImxlZnQiPjxsaSBjbGFzcz0ibGVmdCI%2BPGIgY2xhc3M9InByaW1UYWJfQ0xfT04iPiZuYnNwOzwvYj48YSBocmVmPSJBRFNMLmFzcHg%2FaWRfcGFnZT0wIiBjbGFzcz0icHJpbVRhYl9CR19PTiI%2BTWF4QURTTC9PcHRpYzwvYT48YiBjbGFzcz0icHJpbVRhYl9DUl9PTiI%2BJm5ic3A7PC9iPjwvbGk%2BPC91bD48L2xpPmQCBw9kFgJmD2QWAgIDD2QWAmYPFgIfAQWpATx1bCBjbGFzcz0ibGVmdCB0eHQxMkJCIj48bGkgY2xhc3M9ImxlZnQiPtCc0L7RmCDQotC10LvQtdC60L7QvDwvbGk%2BPGxpIGNsYXNzPSJsZWZ0IHR4dDEyQkIiPiZndDs8L2xpPjxsaSBjbGFzcz0ibGVmdCB0eHQxMkJCIj5NYXhBRFNML09wdGljINCh0L7QvtCx0YDQsNGc0LDRmDwvbGk%2BPC91bD5kAgkPZBYCZg9kFgICAQ9kFgICAQ9kFgJmDxYCHwEFwwI8ZGl2PjxiIGNsYXNzPSJtZW51X3RvcCI%2BJm5ic3A7PC9iPjx1bD48bGkgY2xhc3M9Im1lbnVsdjEiPjxhIGNsYXNzPSJBQ1RJViIgaHJlZj0iaHR0cHM6Ly9tb2oudGVsZWtvbS5tay8vQURTTC5hc3B4P2lkX3BhZ2U9MCI%2BQURTTC9PcHRpYyDRgdC%2B0L7QsdGA0LDRnNCw0Zg8L2E%2BPC9saT48bGkgY2xhc3M9Im1lbnVsdjEiPjxhIGhyZWY9Imh0dHBzOi8vbW9qLnRlbGVrb20ubWsvL0FEU0wuYXNweD9pZF9wYWdlPTEiPtCf0YDQvtC80LXQvdCwINC90LAg0LvQvtC30LjQvdC60LA8L2E%2BPC9saT48L3VsPjxiIGNsYXNzPSJtZW51X2JvdCI%2BJm5ic3A7PC9iPjwvZGl2PmQCCw9kFgICAQ9kFgJmD2QWCgIIDxBkDxYHZgIBAgICAwIEAgUCBhYHEAUO0KLQtdC60L7QstC10L0FCDIwMTAxMDE0ZxAFBjkuMjAxMAUIMjAxMDA5MDFnEAUGOC4yMDEwBQgyMDEwMDgwMWcQBQY3LjIwMTAFCDIwMTAwNzAxZxAFBjYuMjAxMAUIMjAxMDA2MDFnEAUGNS4yMDEwBQgyMDEwMDUwMWcQBQY0LjIwMTAFCDIwMTAwNDAxZxYBAgFkAg4PDxYCHwEFEmRhbWphbi1kQHQtaG9tZS5ta2RkAhIPDxYCHwEFFDAxLjEwLjIwMTAgMDA6MDE6MTY6ZGQCFg8PFgIfAQUcPHN0cm9uZz4yNTczNiw3OCBNQjwvc3Ryb25nPmRkAhgPDxYCHwEFTdCS0LrRg9C%2F0LXQvSDQvtGB0YLQstCw0YDQtdC9INGB0L7QvtCx0YDQsNGc0LDRmCA8c3Ryb25nPjI1NzM2LDc4IE1CPC9zdHJvbmc%2BZGRkelfU2ux%2FbE7V10PuM54dV0Zscoc%3D&ctl00%24cphMain%24ctl00%24cmbMonth={0}'
    self.months = {}    

  def initialize_socket(self):
    hh = HTTPHandler()
    hsh = HTTPSHandler()
    #hh.set_http_debuglevel(1)
    #hsh.set_http_debuglevel(1)

    self.socket = urllib2.build_opener(hh, hsh, urllib2.HTTPCookieProcessor())
    self.socket.addheaders = [('User-Agent', 'Mozilla/9.876 (X11; U; Linux 2.2.12-20 i686, en; rv:2.0) Gecko/25250101 Netscape/5.432b1')]
    #logger = logging.getLogger("cookielib")
    #logger.addHandler(logging.StreamHandler(sys.stdout))
    #logger.setLevel(logging.DEBUG)
    data = self.fetch(self.initial_url)
    error_message = "jAlert('Корисничкото име или Лозинката се погрешно внесени','Грешка');"
    if not error_message in data:
      parsed_month = self.parse(data)
      num = datetime.now().month
      self.months[int(num)] = parsed_month
      return True
    else:
      return False
  def doubleNum(self, num):
    if len(str(num)) < 2:
      return "0%s" % (str(num))
    else:
      return num
  def fetch(self, url):
    response = self.socket.open(url)
    return response.read()
  def login(self):
    '''Log on the server.'''

    self.initial_url = 'https://moj.telekom.mk/MojTelekom.aspx?__EVENTARGUMENT=&__EVENTTARGET=&__EVENTVALIDATION=%2FwEWBQLa6tONCALer42jAQLitbeHAgLKw6LdBQKR%2BN3hBfLRbFZGrhp4ZVCsCTxJHpxFMATA&__VIEWSTATE=%2FwEPDwUJMTYxMjAyODgwZGRRF5G9Qsx4IvD5q4tJyadTp4gWAA%3D%3D&btnVnesi=%D0%92%D0%BD%D0%B5%D1%81%D0%B8&txtPass={0}&txtUserMail={1}&'.format(self.get_password(), self.get_username())
    if self.initialize_socket():
      # TODO: make a parser that reads the combo with the months range.
      for i in xrange(4, 10):
	num = self.doubleNum(i)
	month = "2010%s01" % (num)

	_url = self.get_months_url.format(month)
	parsed_month = self.parse(self.fetch(_url))
	self.months[int(num)] = parsed_month
      return True
    else:
      return False
  def disconnect(self):
    '''Disconnect the user.'''

    self.socket.close()
  def parse(self, data):
    '''Get all the available months.
    data : the data to parse (string).'''

    soup = BeautifulSoup(data)
    total_bandw = 0
    total = soup.findAll('span')
    times = 0
    for i in total:
      try:
	try:
	  if i.get("id") ==  "ctl00_cphMain_ctl00_lblTotal":
	    t = i.first().contents
	    t1 = str(t[0]).split(" ")[0].replace(",", ".")
	    total_bandw = float(t1)
	except TypeError:
	  pass
      except UnicodeEncodeError:
	pass
    return total_bandw
  def get_month(self, month):
      '''Returns the trafic for a month.
      month : the month we seek (integer).'''

      if month in self.months.keys():
	return self.months[month]
      else:
	return False
class LoginManager(object):
  def __init__(self):
    '''Constructor'''

    super(LoginManager, self).__init__()
def main ():
  #lm =  LoginManager()
  th = ThomeLogin()
  th.set_username("")
  th.set_password("")
  th.login()
  for i in range(1, 12):
    print(th.get_month(i))
if __name__ == "__main__":
  main()