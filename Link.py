import os

import requests
import bs4
import email_scraper
import re
import csv
import urllib.request
from PIL import Image
import pytesseract
import pandas


# # noinspection SpellCheckingInspection
# class Firma:
# 	domain = "https://epoznan.pl"
# 	url = ""
# 	address = ""
# 	email = ""
# 	strona = ""
# 	name = ""
# 	type = ""
# 	processed = False
#
# 	def __init__(self, url):
# 		self.url = self.domain + '/' + url
# 		self.getaddress()
# 		self.print_to_file()
#
# 	def getaddress(self):
# 		page = requests.get(self.url)
# 		if page.status_code == 200:
# 			self.get_contents(page)
#
# 	def get_contents(self, page):
# 		try:
# 			soup = bs4.BeautifulSoup(page.content, 'html.parser')
# 			name = soup.find('div', class_='m_name')
# 			self.name = name.text
# 			type = soup.find('div', class_='m_type')
# 			self.type = type.text
# 			address = soup.find('div', class_='m_address')
# 			self.address = address.text
# 			strona = soup.find('a', class_='m_link')
# 			self.strona = strona.text
# 			content_extracted_for_email = soup.find('table', class_='miejsce')
# 			test = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", str(content_extracted_for_email))
# 			self.email = test[0]
# 		except:
# 			print()
# 		self.processed = True
#
# 		try:
# 			soup = bs4.BeautifulSoup(page.content, 'html.parser')
# 			address = soup.find('div', class_='m_address')
# 			if self.email == '':
# 				email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", str(address))
# 				self.email = email[0]
# 			elif self.strona == '':
# 				strona = re.findall('www?://(?:[-\w.]|(?:%[\da-fA-F]{2,3}))+', str(address))
# 				self.strona = strona[0]
# 		except:
# 			print()
#
# 	def print_to_file(self):
# 		if self.processed is True:
# 			list_to_print = [self.name, self.url, self.strona, self.type, self.address, self.email]
# 			with open('data_scrapped_for_Szczur.csv', 'a', newline='', encoding='UTF-8') as csvfile:
# 				writer = csv.writer(csvfile, delimiter=',')
# 				writer.writerow(list_to_print)
# 			# print("Source " + self.domain+self.url)
# 			# print("Name " + self.name)
# 			# print("Address " + self.address)
# 			# print("Strona " + self.strona)
# 			# print("Typ" + self.type)
# 			# print("E-mail "+ self.email)


#### SECOND PAGE

class Firma:
	hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
	page_number = 0
	domain = "https://www.baza-firm.com.pl"
	url = ""
	name = ""
	address_street = ""
	address_postal_code = ""
	address_city = ""
	email = ''
	wojewodztwo = ""
	powiat = ""
	www = ""
	type = []
	tel = []
	processed = False
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]

	def __init__(self, url, page):
		self.address_street = ""
		self.address_postal_code = ""
		self.address_city = ""
		self.email = ''
		self.wojewodztwo = ""
		self.powiat = ""
		self.www = ""
		self.type = []
		self.tel = []
		self.url = url
		self.page_number = page
		self.getaddress()
		self.print_to_file()

	def getaddress(self):
		page = requests.get(self.url, headers = self.hdr)
		if page.status_code == 200:
			self.get_contents(page)

	def get_email_from_image(self, uri):
		try:
			urllib.request.install_opener(self.opener)
			urllib.request.urlretrieve(uri, 'email.jpg')
			self.email = pytesseract.image_to_string(Image.open('email.jpg'))

		except:
			print("There was a problem with email from" + self.url)
		finally:
			os.remove('email.jpg')
			self.email = self.email.replace(" ", "")
			print(self.email)

	def get_contents(self, page):
		try:
			soup = bs4.BeautifulSoup(page.text, 'html.parser')

			#name
			result = soup.find('h1', itemprop='name')
			self.name = result.text
			#branze
			type1 = soup.find('div', id='brBox')
			type_extracted = type1.findAll('li')
			for item in type_extracted:
				self.type.append(item.span.text)
			# if  len(type_extracted) > 1 :
			# 	for item in type_extracted[1:] :
			# 		self.type.append(item.text)

			# somethingelse = type_extracted.findAll('a')
			# for link in somethingelse:
			# 	# links = link.a['href'].text
			# 	self.type += " " + link.text

			#adres
			self.address_street = soup.find('span', itemprop='streetAddress').text
			self.address_postal_code = soup.find('span', itemprop='postalCode').text
			self.address_city = soup.find('span', itemprop='addressLocality').text
			self.wojewodztwo = soup.find('span', itemprop = 'addressRegion').text
			#powiat
			i_tag = soup.find('span', class_='marginTop10 fontSize14 grayColor mainLabFnt')
			self.powiat = i_tag.nextSibling
			#telephone
			tel_list = soup.findAll('span', itemprop='telephone')
			for item in tel_list:
				self.tel.append(item.text)

			www_raw = soup.find('div', id="wwwAddrBox")
			self.www = www_raw.a.attrs['href']

			link_to_image = soup.find('div', id='emlAddrBox')
			link_to_image = link_to_image.img.attrs['src']
			link_to_image +='.jpg'
			full_link = self.domain + link_to_image
			self.get_email_from_image(full_link)

		except:
			print("Issue with " + self.url)
		self.processed = True
		print(self.url + " processed")

		# try:
		# 	soup = bs4.BeautifulSoup(page.content, 'html.parser')
		# 	address = soup.find('div', class_='m_address')
		# 	if self.email == '':
		# 		email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", str(address))
		# 		self.email = email[0]
		# 	elif self.strona == '':
		# 		strona = re.findall('www?://(?:[-\w.]|(?:%[\da-fA-F]{2,3}))+', str(address))
		# 		self.strona = strona[0]
		# except:
		# 	print()

	def print_to_file(self):
		if self.processed is True:
			list_to_print = [self.page_number, self.name, self.url, self.email, self.tel, self.www, self.type, self.address_city, self.address_street, self.address_postal_code, self.wojewodztwo, self.powiat, ]
			with open('data_scrapped.csv', 'a', newline='', encoding='UTF-8') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				writer.writerow(list_to_print)
			# print("Source " + self.domain+self.url)
			# print("Name " + self.name)
			# print("Address " + self.address)
			# print("Strona " + self.strona)
			# print("Typ" + self.type)
			# print("E-mail "+ self.email)
