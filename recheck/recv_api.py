#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from utils.workitem import make_std_record
from recheck.defines import MONGO

NOW = datetime.datetime.now


def push_data():
	""" 推送复检数据
	"""
	now = NOW()

	detail = {
		'recheck_type': 'Vulnerability',
		'issue_description': 'The url is not safe',
		'issue_urls': [],
		'cert_type': 'id',
		'confirmed': 'none',
		'recheck_from': 'anquan',
		'recheck_time': now,
	}

	raw_order_data = {
		'url': 'www.baidu.com/index.html',
		'domain': 'www.baidu.com',
		'details': [detail],
	}

	record = make_std_record(raw_order_data)

	MONGO.recheck_workitem.insert(record)


def clear_data():
	""" 清除数据库表
	"""
	MONGO.recheck_workitem.remove()
	MONGO.recheck_workitem_history.remove()


if __name__ == '__main__':
	import sys
	if len(sys.argv) != 2 or sys.argv[1] not in ('push_data', 'clear_data'):
		sys.stderr.write('Usage: python dc_api.py <push_data|clear_data>\n')
		sys.exit(1)

	globals()[sys.argv[1]]()
