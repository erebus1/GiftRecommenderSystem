__author__ = 'user'
from Requests import tradingApi
from Requests import findingApi

from additionalStaff import *


def gen_HTML(items):
    HTML = ""
    for item in items:
        HTML += "\n <div> <H3>"+item['title']+'</H3><p></p><img src='+\
            item['galleryURL'] +"/><p>"+item['price']['value']+item['price']['_currencyId']+"</p>"
    return HTML




def get_recommendation(hobby):
    hobby += " accessories"
    response_categories = tradingApi.run("GetSuggestedCategories", {'query':hobby})
    items = []
    for category in response_categories['SuggestedCategoryArray']['SuggestedCategory']:
        response_items = findingApi.get_list_of_items("findItemsAdvanced",
                                                {'categoryId': category['Category']['CategoryID'],
                                                 'paginationInput': {'entriesPerPage': 3}})

        for item in response_items['searchResult']['item']:
            items.append({'title': item['title']+'('+category['Category']['CategoryName']+')',
                          'galleryURL': item['galleryURL'], 'itemURL':item['viewItemURL'], 'price':item['sellingStatus']['convertedCurrentPrice']})
    return gen_HTML(items)

