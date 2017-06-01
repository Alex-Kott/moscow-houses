import pickle
import re

scraps = set()
scraps = {"улица", "проезд", "бульвар", "площадь", "проспект", "аллея", "шоссе", "набережная", "тупик", "переулок", "горка", "просек", "линия", "улицы", "Центральный"} 
reduce_streets = []

with open("streets.pickle", "rb") as f:
	streets = pickle.load(f)

for i in streets:
	flag = False
	for j in scraps:
		if i.find(j) != -1:
			street = i.replace(j, '')
			flag = True
	street = re.sub('\s*\S*\d+\S*\s*', '', street)
	reduce_streets.append(street)

with open("reduce_streets.pickle", "wb") as f:
	pickle.dump(reduce_streets, f)

j = 0
for i in reduce_streets:
	j += 1
	print(i)
	if j == 50:
		break



f.close()