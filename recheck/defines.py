#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

from recheck import application

MONGO = MongoClient().workitem

CONFIG = {
	'tables': {
		'workitem': MONGO.recheck_workitem,
		'history': MONGO.recheck_workitem_history,
	},
	'tasks_cls': {
		'assign': application.Assign,
		'follow': application.Follow,
		'ignore': application.Ignore,
		'cancel': application.Cancel,
	},
	'states': [
		'ready',
		'assigned',  # auditing
		'following',
		'successful',
		'failed',
	]
}

TEXTS = {
	'ready': u'待认领',
	'assigned': u'审核中',
	'following': u'跟进中',
	'successful': u'成功',
	'failed': u'失败',
}
