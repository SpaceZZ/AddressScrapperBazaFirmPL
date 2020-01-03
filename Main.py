import requests
import bs4
import email_scraper
import csv
from pytesseract import pytesseract

import Link
import urllib
from PIL import Image
from urllib.request import urlopen, Request

pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

domain = "https://www.baza-firm.com.pl/wojewodztwo/mazowieckie/strona-"
current_domain = ""
list_of_links = []
list_of_companies = []
last_page = 2808

# def get_links_from_the_file(uri):
# 	with open(uri) as csvfile:
# 		readCSV = csv.reader(csvfile, delimiter=",")
# 		for row in readCSV:
# 			text = row[0]
# 			list_of_links.append(text)

def get_links_to_the_companies(uri, page):
	list_of_companies = []
	site = uri
	hdr = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
	req = requests.get(site, headers = hdr)
	print(req)
	soup = bs4.BeautifulSoup(req.text, 'html.parser')
	# listoflinks = soup.select("a href", class_='tekst_tytul_miejsce')
	listoftitles = soup.findAll('a', class_='wizLnk')
	for item in listoftitles:
		value = item.attrs['href']
		new_value = value.replace("'", "")
		print(value)
		list_of_companies.append(new_value)
	for company in list_of_companies:
		v = Link.Firma(company, page)

for i in range(1, last_page):
	current_domain = domain + str(i)
	print(i)
	get_links_to_the_companies(current_domain, i)





