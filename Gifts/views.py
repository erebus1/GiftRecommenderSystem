from django.shortcuts import render
from getRecommendations import Categories
# Create your views here.
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('''
        <form action="recommendations">
            <input type="text" name="hobby" value="What is your hobby" />
            <input type="submit" value="Get recommendation">
        </form>
    ''')

def recommendations(request, param):
    hobby = request.GET.get('hobby', '')
    return HttpResponse('''
        <form action="recommendations">
            <input type="text" name="hobby" value="What is your hobby" />
            <input type="submit" value="Get recommendation">
        </form>
    ''' + Categories.get_recommendation(hobby))



def getRecommendation(request):
    return HttpResponse("")