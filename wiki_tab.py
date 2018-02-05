#! /usr/bin/python


data = open("tell_data.csv", "r")
table = open("wiki_table.txt", "w")

for line in data:
	nline = line.replace(',', ' || ')
	name = nline.split()[0]
	print '|', name
	print '|', nline[13:]
	print '|-'

	table.write('| ' + str(name) + '\n')
	table.write('| ' + str(nline[13:]) + '\n')
	table.write('|-' + '\n')

data.close()
table.close()
