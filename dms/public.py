# -*- coding: utf-8 -*-
# Pagination
from django.core.paginator import Paginator

"""
Global public functions
"""


"""
pagination_creator()
Create Paginator instance with given request, data instance (e.g. QuerySet instance) and number of objects per page

Return the data instance

"""
def pagination_creator(request, instance, num_per_page):
    paginator = Paginator(instance, num_per_page)
    
    if request.GET:
        page = request.GET.get('page',1)
    else:
        page = 1

    instance = paginator.page(page)
    #except PageNotAnInteger:
        #instance = paginator.page(1)
    #except EmptyPage:
        #instance = paginator.page(paginator.num_pages)         
    return instance


"""
dailyPeriod2list()
Convert a daily period (integer) into a 16-element list, each representing a status with 0 or 1
"""
def dailyPeriod2list(daily_period):
    bstring = bin(daily_period)
    string = bstring[2:]
    
    # Make sure the string is 16-digit, padding with 0
    string = string.zfill(16)
    list = [int(i) for i in string]
    return list