#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf.urls import patterns, url
from recheck.views import index, review

urlpatterns = patterns('',
    url(r'^$', index, {'template': 'recheck/index.html'}, name='recheck_index'),
    url(r'^(?P<record_id>\w+)/$', review, {'template': 'recheck/review.html'}, name='recheck_review'),
)
