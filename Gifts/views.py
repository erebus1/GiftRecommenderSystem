from django.shortcuts import render
from getRecommendations import Categories
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def home(request):
    hobby = request.GET.get('hobby', '')
    if request.POST:
        print request
    return HttpResponse('''
        <form action="recommendations">
            <input type="text" name="hobby" value="What is your hobby" />
            <input type="submit" value="Get recommendation">
        </form>
    ''')



