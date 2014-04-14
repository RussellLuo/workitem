#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.workitem import Task
from utils.workitem.shared_tasks import Assign


Assign = Assign


class Follow(Task):
	""" 跟进
	"""
	def precondition(self):
		""" 内部前置条件
		"""
		return (self._model.status == 'assigned')

	def _process(self):
		""" 业务处理
		"""
		self._model.update_business_data({'my_data': u'跟进数据'})

		return 'following'


class Ignore(Task):
	""" 忽略
	"""
	def precondition(self):
		""" 内部前置条件
		"""
		return (self._model.status == 'assigned')

	def _process(self):
		""" 业务处理
		"""
		self._model.update_business_data({'my_data': u'忽略数据'})

		return 'successful'


class Cancel(Task):
	""" 撤销
	"""
	def precondition(self):
		""" 内部前置条件
		"""
		return (self._model.status == 'assigned')

	def _process(self):
		""" 业务处理
		"""
		self._model.update_business_data({'my_data': u'撤销数据'})

		return 'failed'
