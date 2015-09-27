from django.shortcuts import render
from getRecommendations import Categories
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Constants import *
from Gifts.getRecommendations.RS import Users, Recommendations
import json

# Create your views here.


def add_user(request):
    if 'userProfile' not in request:
        return JsonResponse({'result': 'Error', 'message': 'userProfile do not presented'})
    if request['userProfile']['sex'] not in ['Female', 'Male']:
        return JsonResponse({'result': 'Error', 'message': request['userProfile']['sex'] +
                                                           ' is not a valid sex'})
    if 'alreadyGifted' not in request['userProfile']:
        request['userProfile']['alreadyGifted'] = []
    if 'lovedCategories' not in request['userProfile']:
        request['userProfile']['lovedCategories'] = []
    try:
        user_id = Users.add_user(request['userProfile'])

    except Exception as e:
        print e
        return JsonResponse({'result': 'Error', 'message': 'error while adding user'})

    return JsonResponse({'result': 'Success', 'data': {'userId': user_id}})


def make_list(request):
    for key in request['filter'].keys():
        if key != "minPrice" and key != "maxPrice":
            return JsonResponse({'result': 'Error', 'message': key + ' is not a valid filter field'})
    if 'userId' not in request:
        return JsonResponse({'result': 'Error', 'message': 'userId do not presented'})

    min_price = None
    max_price = None
    if 'filter' in request:
        if 'minPrice' in request['filter']:
            min_price = request['filter']['minPrice']
        if 'maxPrice' in request['filter']:
            max_price = request['filter']['maxPrice']
    try:
        Recommendations.generate_list(request['userId'], min_price, max_price)
    except Exception as e:
        print e
        return JsonResponse({'result': 'error', 'message': 'error while making list'})
    return JsonResponse({'result': 'Success'})






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
                return JsonResponse({'result': 'Error', 'message': 'task do not presented'})
            if 'data' not in request_dict:
                return JsonResponse({'result': 'Error', 'message': 'data do not presented'})
            if request_dict['task'] == 'addUser':
                return add_user(request_dict['data'])
            if request_dict['task'] == 'makeList':
                return make_list(request_dict['data'])
            if request_dict['task'] == 'getSuggestions':
                return get_suggestions(request_dict['data'])
            if request_dict['task'] == 'rateItem':
                return rate_item(request_dict['data'])
            return JsonResponse({'result': 'Error', 'message':
                request_dict['task'] + " is not a valid task"})
        except Exception as e:
            print e
            return JsonResponse({'result': 'Error', 'message': "strange error"})

    return HttpResponse('''
        <h1>Welcome on GRS</h1>
    ''')



