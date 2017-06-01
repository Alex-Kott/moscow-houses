import requests as req
import re
from bs4 import BeautifulSoup
import time
import pickle
import sys
sys.setrecursionlimit(10000)

scraps = set()
scraps = {"улица", "проезд", "бульвар", "площадь", "проспект", "аллея", "шоссе", "набережная", "тупик", "переулок"} 
streets = []

def parse_streets(page):
	soup = BeautifulSoup(page, "lxml")
	tabs = soup.find_all("div", "tab")
	for i in tabs:
		a = i.find_all("a")
		street = a[0].contents[0]
		streets.append(street)
		


url = "http://www.street-viewer.ru/moscow/street/"

r = req.get(url)
soup = BeautifulSoup(r.text, "lxml")
pagination = soup.find_all("ul", "pagination")
nav = pagination[0]
a = nav.find_all("a")[-1]
last_page = a.contents[0]

for i in range(int(last_page)):
	r = req.get(url+str((i+1)))
	parse_streets(r.text)
	time.sleep(1)


with open("streets.pickle", "wb") as f:
	pickle.dump(streets, f)
