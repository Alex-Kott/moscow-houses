import pickle
import re
import requests as req
from bs4 import BeautifulSoup

#скрипт формирует словарь, где ключ - id улицы, а значение -- название улицы

with open("sorted_streets.pickle", "rb") as f:
	streets = pickle.load(f)
f.close()

street_ids = dict()
for i in streets:
	r = req.get("http://tipdoma.ru/search_str.php?value="+i)
	r.encoding = "UTF-8"
	soup = BeautifulSoup(r.text, "lxml")
	links = soup.find_all("a")
	for j in links:
		street_id = re.findall(r'\d+', str(j))
		street_name = j.contents[0]
		street_id = street_id[0]
		street_ids[street_id] = street_name
		print(street_ids[street_id])

street_dict = street_ids

with open("street_dict.pickle", "wb") as f:
	pickle.dump(street_dict, f)
f.close()
