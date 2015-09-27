from django.shortcuts import render
from getRecommendations import Categories
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Constants import *
from Gifts.getRecommendations.RS import Users
import json

# Create your views here.


def add_user(request):
    if 'userProfile' not in request:
        return JsonResponse({'result': 'error', 'message': 'userProfile do not presented'})
    if request['userProfile']['sex'] not in ['Female', 'Male']:
        return JsonResponse({'result': 'error', 'message': request['userProfile']['sex'] +
                                                           ' is not a valid sex'})
    if 'alreadyGifted' not in request['userProfile']:
        request['userProfile']['alreadyGifted'] = []
    if 'lovedCategories' not in request['userProfile']:
        request['userProfile']['lovedCategories'] = []
    try:
        user_id = Users.add_user(request['userProfile'])

    except Exception as e:
        print e
        return JsonResponse({'result': 'error', 'message': 'error while adding user'})

    return JsonResponse({'result': 'Success', 'data': {'userId': user_id}})


def use_filter(request):
    pass


def get_suggestions(request):
    pass


def rate_item(request):
    pass


@csrf_exempt
def home(request):
    if request.method == "POST":
        print request
        try:
            request_dict = json.loads(request.body)
            print(request_dict)
            if 'task' not in request_dict:
                return JsonResponse({'result': 'error', 'message': 'task do not presented'})
            if 'data' not in request_dict:
                return JsonResponse({'result': 'error', 'message': 'data do not presented'})
            if request_dict['task'] == 'addUser':
                return add_user(request_dict['data'])
            if request_dict['task'] == 'useFilter':
                return use_filter(request_dict['data'])
            if request_dict['task'] == 'getSuggestions':
                return get_suggestions(request_dict['data'])
            if request_dict['task'] == 'rateItem':
                return rate_item(request_dict['data'])
            return JsonResponse({'result': 'error', 'message':
                request_dict['task'] + " is not a valid task"})
        except Exception as e:
            print e
            return JsonResponse({'result': 'error', 'message': "strange error"})

    return HttpResponse('''
        <h1>Welcome on GRS</h1>
    ''')



