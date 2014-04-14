#!/usr/bin/env python
# -*- coding: utf-8 -*-


class View(object):
	""" 工单视图

	工单模型getter
	"""
	def __init__(self, model):
		self._model = model

	@property
	def owner(self):
		return self._model.owner

	@property
	def status(self):
		return self._model.status

	@property
	def raw_order_data(self):
		return self._model.raw_order_data

	@property
	def modified_order_data(self):
		return self._model.modified_order_data

	@property
	def business_data(self):
		return self._model.business_data

	@property
	def create_time(self):
		return self._model.create_time
