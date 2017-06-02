import pickle
import re
import requests as req
from bs4 import BeautifulSoup
import xlsxwriter


with open("street_dict.pickle", "rb") as f:
	street_dict = pickle.load(f)
f.close()

keys = street_dict.keys()

for i in keys:
	url = "http://tipdoma.ru/search_bld.php?id="+str(i)+"&value="+street_dict[i]
	r = req.get(url)
	r.encoding = "UTF-8"
	S = r.text
	if S.find("Не найдено") == -1:
		print(str(i)+"  "+street_dict[i])
	table = S[S.find("<table"):]
	#print(table)
	soup = BeautifulSoup(r.text, "lxml")
	trs = soup.find_all("tr")
	#for i in trs:
		#tds = trs.findall("td")
		#print(i)

'''
for i in street_dict:
	url = "http://tipdoma.ru/search_bld.php?id="+str(i)+"&value="+street_dict[i]
	#print(url)
	r = req.get(url)
	r.encoding = "UTF-8"
	soup = BeautifulSoup(r.text, "lxml")
	print(r.text)
	break
'''