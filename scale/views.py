# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import ScaleRecords, RemoteUser
from manager.models import Harvest, Lot
from django.http import HttpResponse


from .utils import read_scale_csv


def read_records(request):
	create_harvest_record()

	return HttpResponse('Import completed')

def create_harvest_record():
	records = read_scale_csv()
	entries=[]
	harvests=[]

	for record in records:
		error = ''
		if ScaleRecords.objects.filter(sheet_id=record['sheet_id'], time_stamp=record['timestamp']).exists():
			continue
		else:
			try:
				lot = Lot.objects.get(lot_name=record['lot'])
				crop = lot.crop
			except:
				lot = None
				crop = None
				error+="lot not in database: "+record['lot']+' \n'
			try:
				userid= RemoteUser.objects.get(remote_user_code=record['employee'])
			except:
				userid = None
				error += 'User not in database:'+ record['employee']+' \n'

			entries.append(ScaleRecords(sheet_id=record['sheet_id'], displayed_weight=record['weight'],
			                            time_stamp=record['timestamp'], user=userid,
			                            lot=lot, crop=crop, error_log=error))

	ScaleRecords.objects.bulk_create(entries)



