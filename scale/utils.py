import os
import csv

DIR='/Users/aitorarronte/PycharmProjects/gmail-app/csv/'

def read_scale_csv():
	csv_data=[]
	files = os.listdir(DIR)
	for f in files:
		if '.csv' in f:
			filename = f.split('.csv')[0]
			with open(DIR+f, 'r') as file:
				reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
				next(reader, None)
				for row in reader:
					csv_dict={'sheet_id': filename,'weight': row[0], 'timestamp': row[2], 'employee': row[5].split(':')[1],
				          'lot': row[6].split(':')[1]}
					csv_data.append(csv_dict)

	return csv_data
