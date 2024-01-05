#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/1/5 9:57
# @Author : Genesis Ai
# @File : views.py

from django.http import HttpResponse

def Hello(request):
    return HttpResponse('Hello World')
