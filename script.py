import pickle
import re
import requests as req
from bs4 import BeautifulSoup
import xlsxwriter
import time
import sys


with open("street_dict.pickle", "rb") as f:
	street_dict = pickle.load(f)
f.close()

keys = street_dict.keys()

row = 1
workbook = xlsxwriter.Workbook('moscow_houses.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})
worksheet.set_column('A:A', 30)
worksheet.set_column('B:C', 12)
worksheet.set_column('D:E', 15)
worksheet.set_column('F:G', 10)
worksheet.set_column('H:H', 30)


worksheet.write('A1', 'Улица', bold)
worksheet.write('B1', 'Номер дома', bold)
worksheet.write('C1', 'Корпус/строение', bold)
worksheet.write('D1', 'Город', bold)
worksheet.write('E1', 'Стены', bold)
worksheet.write('F1', 'Этажей', bold)
worksheet.write('G1', 'Год', bold)
worksheet.write('H1', 'Серия или ЖК', bold) 
row += 1

for i in keys:
	url = "http://tipdoma.ru/search_bld.php"
	street = str(street_dict[i])
	street = street[0:-1]
	r = req.get(url, {'id' : i, 'value' : street})
	r.encoding = "UTF-8"
	S = r.text
	if S.find("Не найдено") != -1:
		continue
	soup = BeautifulSoup(r.text, "lxml")
	tbody = soup.tbody
	trs = tbody.find_all("tr")
	for j in trs:
		tds = j.find_all("td")
		address = str(tds[1].a.contents[0])
		walls = str(tds[2].contents[0])
		floors = str(tds[3].contents[0])
		year = str(tds[4].contents[0])

		series = tds[5]
		if series.a == None:
			series = str(series.contents[0])
		else:
			series = str(series.a.contents[0])

		city = re.findall(r'\(.*\)', address)
		if len(city) != 0:
			city = city[0].strip("() ")
			city = city.strip(", ")
		else:
			city = "г. Москва"
		house = re.findall(r',\s\d+\/{0,1}\d*\S*', address)
		address = re.sub(r'\(.*\)', '', address)

		street = re.findall(r'^.*,', address)

		street = street[0].strip(", ")

		if len(house) != 0:
			house = house[0]
		else:
			house = re.findall(r',.*$', address)
			house = house[0]

		house = house.strip(", ")
		housing = address.partition(house)
		housing = housing[2]
	
		worksheet.write('A'+str(row), street)
		worksheet.write('B'+str(row), house)
		worksheet.write('C'+str(row), housing)
		worksheet.write('D'+str(row), city)
		worksheet.write('E'+str(row), walls)
		worksheet.write('F'+str(row), floors)
		worksheet.write('G'+str(row), year)
		worksheet.write('H'+str(row), series)
		row += 1
		print("{0} {1} {2} {3} {4} {5} {6} {7}".format(street, house, housing, city, walls, floors, year, series))
	

workbook.close()