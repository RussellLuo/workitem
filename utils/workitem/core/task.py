#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TaskLockError(Exception):
	pass


class Task(object):
	""" 工单任务

	工单模型setter

	DynamicTask（动态任务）：
		特征：
			必然会转移状态
			可能会修改数据

		标识：
			_process返回目标状态

	StaticTask（静态任务）：
		特征：
			不会转移状态
			只会修改数据

		标识：
			_process返回None
	"""
	def __init__(self, model, states):
		self._model = model
		self._states = states
		self._input = {}
		self._output = None

	def set_input(self, data):
		""" 设置输入数据
		"""
		pass

	@property
	def output(self):
		return self._output

	def precondition(self):
		""" 内部前置条件

		内部前置条件：当前业务中，执行当前task需要的固定前置条件，在本函数中指定
		外部前置条件：特定状态下，执行当前task额外需要的特定前置条件，在执行task前附加指定
		"""
		return True

	def execute(self):
		""" 任务处理
		"""
		self._preprocess()

		state = self._process()
		if state is not None:
			assert (state in self._states and
					state != self._model.status), u'转移的目标状态不合法'
			self._model.status = state

		self._postprocess()

	def _preprocess(self):
		""" 前置处理
		"""
		if self._model.lock:
			raise TaskLockError('Lock has been taken by another task.')

		self._model.lock = True
		self._model.checkout()

	def _process(self):
		""" 业务处理
		"""
		raise NotImplementedError

	def _postprocess(self):
		""" 后置处理
		"""
		self._model.commit()
		self._model.lock = False
