#!/usr/bin/env python

#-*- coding: utf-8 -*-
import re
from django.http import HttpResponse, HttpResponseNotFound,Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from cyclope import settings as cyc_settings

from cyclope import models

# nothing here yet
