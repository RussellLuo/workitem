#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import redis

REDIS = redis.Redis()

NOW = datetime.datetime.now


class Model(object):
	""" 工单模型

	工单数据的访问接口
	"""
	def __init__(self, tables, record_id):
		self.tables = tables
		self.record_id = get_objectid(record_id)
		self.lock_key = '%s:lock:%s' % (self.tables['workitem'].name, str(record_id))

		self.checkout()

	@property
	def lock(self):
		""" 从Redis数据库实时获取工单锁
		"""
		return REDIS.get(self.lock_key) == 'True'

	@lock.setter
	def lock(self, value, timeout=60):
		""" 往Redis数据库实时设置工单锁
		"""
		REDIS.set(self.lock_key, value)
		if value:  # 如果是占用锁，默认timeout秒后自动释放锁
			REDIS.expire(self.lock_key, timeout)

	@property
	def owner(self):
		return self.record['owner']

	@owner.setter
	def owner(self, value):
		self.record['owner'] = value

	@property
	def status(self):
		return self.record['status']

	@status.setter
	def status(self, value):
		self._transfer(value)

	@property
	def raw_order_data(self):
		return self.record['order_data']['raw']

	@property
	def modified_order_data(self):
		return self.record['order_data']['modified']

	def update_order_data(self, new):
		self.record['order_data']['modified'].update(new)

	@property
	def business_data(self):
		return self.record['business_data']

	def update_business_data(self, new):
		self.record['business_data'].update(new)
		self.record['business_data']['update_time'] = NOW()

	@property
	def create_time(self):
		return self.record['create_time']

	def _transfer(self, target):
		""" 转移状态

		为了维护transfer的前后关系(from, to)，会涉及多次数据同步修改，考虑是否去掉？
		"""
		_id = self._backup()

		# 修改前一条历史工单的transfer_to
		prev_id = self.record['transfer']['from']
		self.tables['history'].update({'_id': prev_id}, {'$set': {'transfer.to': _id}})

		# 修改当前工单的转移信息
		self.record['status'] = target
		self.record['transfer']['from'] = _id
		self.record['transfer']['time'] = NOW()

	def _backup(self):
		""" 备份当前工单记录到历史工单表
		"""
		snap = self.tables['workitem'].find_one({'_id': self.record_id})
		snap.pop('_id')
		snap['transfer']['to'] = self.record_id
		return self.tables['history'].insert(snap)

	def checkout(self):
		""" 检出数据库到暂存区

		直接从数据库载入数据到暂存区，之前对暂存区的所有修改都会被覆盖
		"""
		self.record = self.tables['workitem'].find_one({'_id': self.record_id})

	def commit(self):
		""" 提交暂存区到数据库
		"""
		self.tables['workitem'].save(self.record)


def get_objectid(_id):
	import bson

	if isinstance(_id, basestring):
		return bson.ObjectId(_id)
	return _id


def make_std_record(raw_order_data):
	""" 生成一条标准的工单记录
	"""
	now = NOW()
	record = {
		'owner': 'none',
		'status': 'ready',
		'transfer': {
			'from': 'none',
			'to': 'none',
			'time': now
		},
		'order_data': {
			'raw': raw_order_data,
			'modified': {}
		},
		'business_data': {},
		'create_time': now
	}
	return record
