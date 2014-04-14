#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .model import Model
from .view import View
from .task import TaskLockError


class Workitem(object):
	""" 工单实体

	view:  工单数据窗口
	tasks: 可执行的任务集
	"""
	def __init__(self, record_id, config):
		model = Model(config['tables'], record_id)
		self.view = View(model)
		self.tasks = {
			task_name: task_cls(model, config['states'])
			for task_name, task_cls in config['tasks_cls'].items()
		}

	def do(self, name, data):
		if name not in self.tasks:
			return ('task_missing', None)

		task = self.tasks[name]
		task.set_input(data)
		if not task.precondition():
			return ('task_refused', None)

		try:
			task.execute()
			return ('task_successful', task.output)
		except TaskLockError:
			return ('task_failed', None)
