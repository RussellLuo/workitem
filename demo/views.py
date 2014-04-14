#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render


def index(request, template):
	return render(request, template)
