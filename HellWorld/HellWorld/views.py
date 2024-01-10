#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/1/5 9:57
# @Author : Genesis Ai
# @File : views.py

from django.shortcuts import render

def index(request):
    context = {}
    context["name"] = "Hello World"

    return  render(request,"index.html",context)
