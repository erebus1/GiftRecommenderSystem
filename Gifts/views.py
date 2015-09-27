from django.shortcuts import render
from getRecommendations import Categories
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Constants import *

# Create your views here.

def add_user(request):
    pass


def use_filter(request):
    pass


def get_suggestions(request):
    pass


def rate_item(request):
    pass


@csrf_exempt
def home(request):
    if request.POST:
        print request
        try:
            request_dict = dict(request.POST)
            if 'task' not in request_dict:
                return error_response
            if request_dict['task'] == 'add user':
                return add_user(request_dict['data'])
            if request_dict['task'] == 'use filter':
                return use_filter(request_dict['data'])
            if request_dict['task'] == 'get suggestions':
                return get_suggestions(request_dict['data'])
            if request_dict['task'] == 'rate item':
                return rate_item(request_dict['data'])
        except:
            return error_response

        return JsonResponse({'result': 'success', 'response': [{'foo': 'bar'}]})
    return HttpResponse('''
        <h1>Welcome on GRS</h1>
    ''')



