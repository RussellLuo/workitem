#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.shortcuts import render

from utils.workitem import Workitem
from .defines import CONFIG, TEXTS, MONGO


def index(request, template):
	def make_items(records):
		return [
			{
				'id': w['_id'],
				'owner': w['owner'],
				'my_data': w['business_data'].get('my_data', u'无'),
				'status': TEXTS[w['status']],
				'transfer_from': w['transfer']['from'],
				'transfer_to': w['transfer']['to'],
				'transfer_time': w['transfer']['time'],
				'create_time': w['create_time']
			}
			for w in records
		]

	workitems = MONGO.recheck_workitem.find() or {}
	histories = MONGO.recheck_workitem_history.find() or {}

	return render(
		request,
		template,
		{
			'workitems': make_items(workitems),
			'histories': make_items(histories)
		}
	)


def review(request, record_id, template):
	action = request.GET.get('action')
	owner = request.GET.get('owner')

	workitem = Workitem(record_id, CONFIG)

	result, output = None, None
	if action:
		result, output = workitem.do(action, {'owner': owner})
	status = workitem.view.status

	return render(
		request,
		template,
		{'status': TEXTS.get(status), 'result': result, 'output': output}
	)
