#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.workitem import Task


class Assign(Task):
	""" 分配/认领
	"""
	def precondition(self):
		""" 内部前置条件
		"""
		return self._model.status == 'ready'

	def set_input(self, data):
		""" 设置输入数据
		"""
		self._input['owner'] = data['owner']

	def _process(self):
		""" 业务处理
		"""
		self._model.owner = self._input['owner']

		return 'assigned'
