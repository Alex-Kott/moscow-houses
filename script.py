import pickle
import re
import requests as req
from bs4 import BeautifulSoup
import xlsxwriter
import time


with open("street_dict.pickle", "rb") as f:
	street_dict = pickle.load(f)
f.close()

keys = street_dict.keys()

for i in keys:
	url = "http://tipdoma.ru/search_bld.php"
	print(url)
	#print(str(i)+"   "+street_dict[i])
	r = req.get(url, {'id' : i, 'value' : street_dict[i]})
	print(r.url)
	r.encoding = "UTF-8"
	S = r.text
	#print(S)
	if S.find("Не найдено") != -1:
		continue
	soup = BeautifulSoup(r.text, "lxml")
	print(r.text)
	'''table = soup.table
	trs = table.tr
	print(table)'''
	time.sleep(1)


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